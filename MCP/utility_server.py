import os
import sys
import json
import hashlib
import re
import platform
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("UtilityServer")

@mcp.tool()
def read_file(path: str, encoding: str = "utf-8") -> str:
    """读取文件内容

    Args:
        path: 文件绝对路径
        encoding: 文件编码，默认utf-8
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except UnicodeDecodeError:
        with open(path, 'r', encoding='gbk') as f:
            return f.read()
    except FileNotFoundError:
        return f"文件不存在: {path}"
    except Exception as e:
        return f"读取失败: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str, encoding: str = "utf-8") -> str:
    """写入文件内容

    Args:
        path: 文件绝对路径
        content: 要写入的内容
        encoding: 文件编码，默认utf-8
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding=encoding) as f:
            f.write(content)
        return f"成功写入文件: {path}"
    except Exception as e:
        return f"写入失败: {str(e)}"

@mcp.tool()
def list_directory(path: str = ".") -> List[str]:
    """列出目录内容

    Args:
        path: 目录路径，默认为当前目录
    """
    try:
        items = os.listdir(path)
        result = []
        for item in items:
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                result.append(f"[DIR]  {item}")
            else:
                size = os.path.getsize(full_path)
                result.append(f"[FILE] {item} ({size} bytes)")
        return result
    except Exception as e:
        return [f"列出失败: {str(e)}"]

@mcp.tool()
def get_file_info(path: str) -> Dict[str, Any]:
    """获取文件详细信息

    Args:
        path: 文件或目录的绝对路径
    """
    try:
        stat = os.stat(path)
        return {
            "path": path,
            "name": os.path.basename(path),
            "size": stat.st_size,
            "is_file": os.path.isfile(path),
            "is_dir": os.path.isdir(path),
            "created": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S"),
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "accessed": datetime.fromtimestamp(stat.st_atime).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def search_files(directory: str, pattern: str, recursive: bool = False) -> List[str]:
    """在目录中搜索文件

    Args:
        directory: 要搜索的目录
        pattern: 文件名模式（支持*和?通配符）
        recursive: 是否递归搜索子目录
    """
    try:
        results = []
        if recursive:
            for root, dirs, files in os.walk(directory):
                for name in files:
                    if pattern.replace('*', '') in name or name.endswith(pattern.replace('*', '')):
                        results.append(os.path.join(root, name))
        else:
            for item in os.listdir(directory):
                if pattern.replace('*', '') in item:
                    results.append(os.path.join(directory, item))
        return results if results else ["未找到匹配的文件"]
    except Exception as e:
        return [f"搜索失败: {str(e)}"]

@mcp.tool()
def get_system_info() -> Dict[str, Any]:
    """获取系统信息"""
    try:
        return {
            "platform": platform.system(),
            "platform_release": platform.release(),
            "platform_version": platform.version(),
            "architecture": platform.machine(),
            "processor": platform.processor(),
            "cpu_count": os.cpu_count(),
            "hostname": platform.node(),
            "python_version": platform.python_version()
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_disk_usage(path: str = ".") -> Dict[str, Any]:
    """获取磁盘使用情况

    Args:
        path: 磁盘路径，默认为当前目录所在磁盘
    """
    try:
        stat = shutil.disk_usage(path)
        return {
            "total": f"{stat.total / (1024**3):.2f} GB",
            "used": f"{stat.used / (1024**3):.2f} GB",
            "free": f"{stat.free / (1024**3):.2f} GB",
            "percent": f"{stat.used / stat.total * 100:.1f}%"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calculate(a: float, b: float, operator: str) -> float:
    """执行数学运算

    Args:
        a: 第一个操作数
        b: 第二个操作数
        operator: 运算符，支持 +, -, *, /, //, %, **
    """
    operators = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y if y != 0 else "错误: 除数不能为零",
        '//': lambda x, y: x // y if y != 0 else "错误: 除数不能为零",
        '%': lambda x, y: x % y if y != 0 else "错误: 除数不能为零",
        '**': lambda x, y: x ** y
    }
    if operator not in operators:
        return f"错误: 不支持的运算符 '{operator}'"
    result = operators[operator](a, b)
    return result

@mcp.tool()
def text_stats(text: str) -> Dict[str, Any]:
    """获取文本统计信息

    Args:
        text: 要统计的文本
    """
    return {
        "字符数": len(text),
        "字符数(不含空格)": len(text.replace(' ', '')),
        "单词数": len(text.split()),
        "行数": len(text.split('\n')),
        "段落数": len([p for p in text.split('\n\n') if p.strip()])
    }

@mcp.tool()
def find_replace(text: str, find: str, replace: str, case_sensitive: bool = True) -> str:
    """文本查找替换

    Args:
        text: 原始文本
        find: 要查找的内容
        replace: 替换后的内容
        case_sensitive: 是否区分大小写
    """
    if case_sensitive:
        return text.replace(find, replace)
    else:
        pattern = re.compile(re.escape(find), re.IGNORECASE)
        return pattern.sub(replace, text)

@mcp.tool()
def hash_text(text: str, algorithm: str = "md5") -> str:
    """计算文本哈希值

    Args:
        text: 要哈希的文本
        algorithm: 哈希算法，支持 md5, sha1, sha256, sha512
    """
    algorithms = {
        'md5': hashlib.md5,
        'sha1': hashlib.sha1,
        'sha256': hashlib.sha256,
        'sha512': hashlib.sha512
    }
    if algorithm.lower() not in algorithms:
        return f"错误: 不支持的算法 '{algorithm}'"
    return algorithms[algorithm.lower()](text.encode()).hexdigest()

@mcp.tool()
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """获取当前时间

    Args:
        format: 时间格式，默认 "YYYY-MM-DD HH:MM:SS"
    """
    return datetime.now().strftime(format)

@mcp.tool()
def format_date(timestamp: float, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """将时间戳转换为格式化日期字符串

    Args:
        timestamp: Unix 时间戳（秒）
        format: 时间格式
    """
    try:
        return datetime.fromtimestamp(timestamp).strftime(format)
    except Exception as e:
        return f"转换失败: {str(e)}"

@mcp.tool()
def calculate_time_diff(start: str, end: str, format: str = "%Y-%m-%d %H:%M:%S") -> Dict[str, Any]:
    """计算两个日期之间的时间差

    Args:
        start: 开始日期字符串
        end: 结束日期字符串
        format: 日期格式
    """
    try:
        start_dt = datetime.strptime(start, format)
        end_dt = datetime.strptime(end, format)
        diff = end_dt - start_dt
        return {
            "days": diff.days,
            "seconds": diff.total_seconds(),
            "hours": diff.total_seconds() / 3600,
            "minutes": diff.total_seconds() / 60,
            "formatted": f"{diff.days}天 {diff.seconds % 86400 // 3600}小时"
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def get_desktop_files() -> List[str]:
    """获取当前用户的桌面文件列表"""
    return os.listdir(os.path.expanduser("~/Desktop"))

if __name__ == "__main__":
    mcp.run(transport='stdio')