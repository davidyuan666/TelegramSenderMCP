# CommunicationPlugin

Telegram机器人插件，集成DeepSeek AI和Claude Code CLI功能。

## 功能特性

- **DeepSeek AI集成**: 使用 `/deepseek <问题>` 调用本地DeepSeek AI
- **Claude Code CLI集成**: 使用 `/claude <操作>` 调用本地Claude Code CLI执行操作
- **实时状态推送**: 执行过程中实时推送状态更新到Telegram
- **URL内容获取**: 使用 `/fetch <url>` 获取网页内容

## 快速开始

1. 安装依赖:
```bash
pip install -r requirements.txt
```

2. 配置环境变量（复制.env.example为.env并填写）:
```
TELEGRAM_BOT_TOKEN=your_bot_token
DEEPSEEK_API_KEY=your_deepseek_key
CLAUDE_WORK_DIR=C:\workspace\claudecodelabspace
```

3. 运行机器人:
```bash
python -m petircode.main
```

## 命令列表

- `/start` - 启动机器人
- `/help` - 显示帮助信息
- `/deepseek <问题>` - 使用DeepSeek AI回答问题
- `/claude <操作>` - 使用Claude Code CLI执行操作
- `/fetch <url>` - 从URL获取内容

