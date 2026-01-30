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


async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /ask command to query DeepSeek AI"""
    if not context.args:
        await update.message.reply_text(
            "Please provide a question.\nUsage: /ask <your question>"
        )
        return

    question = " ".join(context.args)
    await update.message.reply_text("🤔 正在思考...")

    try:
        from ..services.deepseek import query_deepseek
        response = await query_deepseek(question)

        # Handle long responses (Telegram limit is 4096 characters)
        if len(response) > 4000:
            # Split into chunks
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for i, chunk in enumerate(chunks):
                if i == 0:
                    await update.message.reply_text(chunk)
                else:
                    await update.message.reply_text(f"(continued...)\n\n{chunk}")
        else:
            await update.message.reply_text(response)

    except ValueError as e:
        await update.message.reply_text(
            "⚠️ DeepSeek API is not configured. Please set DEEPSEEK_API_KEY in .env file."
        )
    except Exception as e:
        logger.error(f"Error querying DeepSeek: {e}")
        await update.message.reply_text(
            f"❌ Error: {str(e)}\n\nPlease try again later."
        )


async def computer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /computer command to execute Claude Code operations"""
    if not context.args:
        await update.message.reply_text(
            "Please provide an operation description.\n"
            "Usage: /computer <operation description>\n\n"
            "Examples:\n"
            "• /computer list files in current directory\n"
            "• /computer create a file named test.txt"
        )
        return

    operation = " ".join(context.args)
    await update.message.reply_text("💻 正在执行操作...")

    try:
        from ..services.claude_code import execute_claude_code
        result = await execute_claude_code(operation)

        if result['success']:
            output = result['stdout'].strip()
            if not output:
                output = "✅ 执行成功！"

            # Truncate if too long
            if len(output) > 3800:
                output = output[:3800] + "\n\n... (truncated)"

            await update.message.reply_text(f"✅ 执行成功！\n\n{output}")
        else:
            error_msg = result['stderr'].strip() or result['stdout'].strip()
            if len(error_msg) > 3800:
                error_msg = error_msg[:3800] + "\n\n... (truncated)"

            await update.message.reply_text(
                f"❌ 执行失败 (exit code: {result['return_code']})\n\n{error_msg}"
            )

    except Exception as e:
        logger.error(f"Error executing Claude Code: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")
