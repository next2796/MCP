# Cursor MCP 服务器

基于 Model Context Protocol (MCP) 的实用工具服务器，为 Cursor IDE 提供丰富的工具集。

## 项目结构

```
MCP/
├── test.py                 # 基础示例服务器
├── utility_server.py      # 完整功能服务器
├── cursor_mcp_manager.html # Web 管理界面
└── README.md              # 项目说明文档
```

## 快速开始

### 1. 安装依赖

```bash
pip install mcp
```

### 2. 启动服务器

#### 方式一：基础示例服务器
```bash
python test.py
```

#### 方式二：完整功能服务器
```bash
python utility_server.py
```

### 3. 接入 Cursor IDE

1. 打开 Cursor 设置 (`Ctrl + ,`)
2. 搜索并打开 `MCP (Model Context Protocol)` 设置
3. 编辑 `settings.json`，添加以下配置：

```json
{
  "mcpServers": {
    "UtilityServer": {
      "command": "python",
      "args": ["e:/shi yan dai ma er/MCP/utility_server.py"]
    }
  }
}
```

4. 重启 Cursor

## 可用工具

### 文件操作
| 工具 | 说明 |
|------|------|
| `read_file` | 读取文件内容 |
| `write_file` | 写入文件内容 |
| `list_directory` | 列出目录内容 |
| `get_file_info` | 获取文件详细信息 |
| `search_files` | 搜索文件 |

### 系统信息
| 工具 | 说明 |
|------|------|
| `get_system_info` | 获取系统信息 |
| `get_disk_usage` | 获取磁盘使用情况 |
| `get_desktop_files` | 获取桌面文件列表 |

### 文本处理
| 工具 | 说明 |
|------|------|
| `text_stats` | 文本统计（字符、单词、行数等） |
| `find_replace` | 文本查找替换 |
| `hash_text` | 计算文本哈希值 |

### 数学计算
| 工具 | 说明 |
|------|------|
| `calculate` | 数学运算（支持 + - * / // % **） |

### 日期时间
| 工具 | 说明 |
|------|------|
| `get_current_time` | 获取当前时间 |
| `format_date` | 时间戳转日期 |
| `calculate_time_diff` | 计算时间差 |

## Web 管理界面

打开 `cursor_mcp_manager.html` 文件，可以使用可视化的方式：

- 查看服务器状态
- 测试各种工具
- 执行终端命令
- 查看系统信息

## 使用示例

### 在 Cursor 中调用工具

```
请帮我读取 C:/Users/test/Documents/readme.txt 文件内容
计算 123 + 456 的结果
获取当前系统信息
```

## 技术栈

- Python 3.8+
- MCP SDK
- FastMCP

## 注意事项

1. 确保 Python 已添加到系统 PATH
2. 路径中包含空格时使用正斜杠 `/`
3. 服务使用 stdio 传输，需要通过 MCP 客户端连接

## 许可证

MIT License