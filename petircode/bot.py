"""
Core bot functionality
"""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from .config import config
from .handlers.commands import fetch_command, ask_command, computer_command

logger = logging.getLogger(__name__)


class PetriBot:
    """Main bot class"""

    def __init__(self):
        """Initialize the bot"""
        self.application = None

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        await update.message.reply_text(
            f"Hello {user.first_name}! 👋\n\n"
            "I'm PetriCode bot. I can help you with:\n"
            "• Message interaction\n"
            "• External information retrieval\n"
            "• Data processing\n\n"
            "Use /help to see available commands."
        )

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
Available commands:

/start - Start the bot
/help - Show this help message
/info - Get bot information
/fetch <url> - Fetch content from URL
/search <query> - Search for information
/ask <question> - Ask DeepSeek AI a question
/computer <operation> - Execute computer operations via Claude Code

Send me any message and I'll echo it back!
"""
        await update.message.reply_text(help_text)

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        info_text = (
            "🤖 PetriCode Bot v0.1.0\n\n"
            "A Python-based Telegram bot for message interaction "
            "and external information retrieval."
        )
        await update.message.reply_text(info_text)

    async def echo_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Echo received messages"""
        text = update.message.text
        await update.message.reply_text(f"You said: {text}")

    def setup_handlers(self):
        """Setup command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("info", self.info_command))
        self.application.add_handler(CommandHandler("fetch", fetch_command))
        self.application.add_handler(CommandHandler("ask", ask_command))
        self.application.add_handler(CommandHandler("computer", computer_command))
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.echo_message)
        )

    def run(self):
        """Run the bot"""
        config.validate()
        self.application = Application.builder().token(config.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
        logger.info("Starting PetriCode bot...")
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)
