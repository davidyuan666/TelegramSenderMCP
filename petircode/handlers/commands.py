"""
Command handlers for the bot
"""
import logging
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def fetch_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fetch command to retrieve content from URL"""
    if not context.args:
        await update.message.reply_text(
            "Please provide a URL.\nUsage: /fetch <url>"
        )
        return

    url = context.args[0]
    await update.message.reply_text(f"Fetching content from: {url}\n\nPlease wait...")

    try:
        from ..services.fetcher import fetch_url_content
        content = await fetch_url_content(url)

        if len(content) > 4000:
            content = content[:4000] + "\n\n... (truncated)"

        await update.message.reply_text(f"Content:\n\n{content}")
    except Exception as e:
        logger.error(f"Error fetching URL: {e}")
        await update.message.reply_text(f"Error fetching URL: {str(e)}")


async def deepseek_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /deepseek command to query DeepSeek AI"""
    if not context.args:
        await update.message.reply_text(
            "请提供问题。\n用法: /deepseek <你的问题>"
        )
        return

    question = " ".join(context.args)
    status_msg = await update.message.reply_text("🤔 DeepSeek正在思考...")

    try:
        from ..services.deepseek import query_deepseek

        # Update status
        await status_msg.edit_text("🤔 DeepSeek正在处理您的问题...")

        response = await query_deepseek(question)

        # Update status
        await status_msg.edit_text("✅ DeepSeek已完成回答")

        # Handle long responses (Telegram limit is 4096 characters)
        if len(response) > 4000:
            # Split into chunks
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await update.message.reply_text(f"📝 回答 (第{i+1}部分):\n\n{chunk}")
                else:
                    await update.message.reply_text(f"📝 回答 (第{i+1}部分):\n\n{chunk}")
        else:
            await update.message.reply_text(f"📝 回答:\n\n{response}")

    except ValueError as e:
        await status_msg.edit_text("⚠️ DeepSeek API未配置")
        await update.message.reply_text(
            "⚠️ DeepSeek API未配置。请在.env文件中设置DEEPSEEK_API_KEY。"
        )
    except Exception as e:
        logger.error(f"Error querying DeepSeek: {e}")
        await status_msg.edit_text("❌ DeepSeek执行失败")
        await update.message.reply_text(
            f"❌ 错误: {str(e)}\n\n请稍后重试。"
        )


async def claude_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /claude command to execute Claude Code CLI operations"""
    if not context.args:
        await update.message.reply_text(
            "请提供操作描述。\n"
            "用法: /claude <操作描述>\n\n"
            "示例:\n"
            "• /claude 列出当前目录的文件\n"
            "• /claude 创建一个名为test.txt的文件\n"
            "• /claude 帮我写一个Python脚本计算斐波那契数列"
        )
        return

    operation = " ".join(context.args)
    status_msg = await update.message.reply_text("💻 Claude Code正在启动...")

    try:
        from ..services.claude_code import execute_claude_code_with_status

        # Execute with status updates
        async for status_update in execute_claude_code_with_status(operation):
            if status_update['type'] == 'status':
                await status_msg.edit_text(f"💻 {status_update['message']}")
            elif status_update['type'] == 'progress':
                await status_msg.edit_text(f"⚙️ {status_update['message']}")
            elif status_update['type'] == 'result':
                result = status_update['data']

                if result['success']:
                    await status_msg.edit_text("✅ Claude Code执行完成")

                    output = result['stdout'].strip()
                    if not output:
                        output = "执行成功，无输出内容。"

                    # Split long output
                    if len(output) > 3800:
                        chunks = [output[i:i+3800] for i in range(0, len(output), 3800)]
                        for i, chunk in enumerate(chunks):
                            await update.message.reply_text(
                                f"📄 输出 (第{i+1}/{len(chunks)}部分):\n\n{chunk}"
                            )
                    else:
                        await update.message.reply_text(f"📄 输出:\n\n{output}")
                else:
                    await status_msg.edit_text("❌ Claude Code执行失败")

                    error_msg = result['stderr'].strip() or result['stdout'].strip()
                    if len(error_msg) > 3800:
                        error_msg = error_msg[:3800] + "\n\n... (已截断)"

                    await update.message.reply_text(
                        f"❌ 执行失败 (退出码: {result['return_code']})\n\n{error_msg}"
                    )

    except Exception as e:
        logger.error(f"Error executing Claude Code: {e}")
        await status_msg.edit_text("❌ Claude Code执行出错")
        await update.message.reply_text(f"❌ 错误: {str(e)}")
