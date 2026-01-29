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
