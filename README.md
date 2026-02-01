# Telegram Bot MCP Server

为 Claude Code CLI 提供 Telegram 消息收发能力的 MCP 服务器。

## 项目结构

本项目包含两个独立组件：

1. **MCP Server** (`mcp_server.py`) - 标准 MCP 服务器，让 Claude Code CLI 调用 Telegram 功能
2. **Telegram Bridge** (`telegram_bridge.py`) - 反向桥接，让 Telegram 消息触发 Claude Code CLI

详细配置请参考 [MCP_CONFIG.md](MCP_CONFIG.md)

## 功能

- 发送消息到 Telegram
- 接收 Telegram 消息
- 双向通信：CLI → Telegram 和 Telegram → CLI
- 异步架构，高性能

## 快速开始

### 1. 安装依赖

```bash
cd TelegramSenderMCP
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件：
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

### 3. 配置 Claude Code CLI

编辑配置文件（Windows: `%APPDATA%\Claude\claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "telegram-sender": {
      "command": "python",
      "args": ["C:\\workspace\\claudecodelabspace\\TelegramSenderMCP\\mcp_server.py"],
      "env": {
        "TELEGRAM_BOT_TOKEN": "your_bot_token_here"
      }
    }
  }
}
```

## MCP 工具 API

### send_telegram_message
发送消息到 Telegram。

**参数**:
- `chat_id` (string): Chat ID 或用户名，如 "123456789" 或 "@username"
- `text` (string): 消息内容

### get_telegram_updates
获取最近的 Telegram 消息。

**参数**:
- `limit` (number): 消息数量，默认 10

## 使用示例

### 在 Claude Code CLI 中使用

```
发送消息 "Hello from Claude!" 到 Telegram chat ID 123456789
```

```
获取最近的 Telegram 消息
```

### 使用 Telegram Bridge

启动桥接服务：
```bash
python telegram_bridge.py
```

然后在 Telegram 中向机器人发送消息，机器人会自动执行并返回结果。

## 测试

运行测试脚本验证配置：
```bash
python test_bot.py
```

这将显示 Bot 信息和最近的消息。

## 获取 Chat ID

1. 向你的 Bot 发送任意消息
2. 运行 `python test_bot.py`
3. 查看输出中的 Chat ID

## 故障排除

详细的故障排除指南请参考 [MCP_CONFIG.md](MCP_CONFIG.md#故障排查)

常见问题：
- **连接失败**: 检查 Python 版本 (需要 3.10+) 和依赖安装
- **发送失败**: 确认 Chat ID 格式正确，Bot Token 有效
- **无消息**: 确保已向 Bot 发送过消息

## 文档

- [MCP_CONFIG.md](MCP_CONFIG.md) - 详细配置指南
- [SETUP.md](SETUP.md) - 快速启动指南

## 技术栈

- Python 3.10+
- python-telegram-bot
- MCP SDK
- asyncio

## 安全提示

⚠️ **重要**: 不要将 Bot Token 提交到 Git 仓库！
- 使用 `.env` 文件存储敏感信息
- 确保 `.env` 在 `.gitignore` 中

## 许可证

MIT License
