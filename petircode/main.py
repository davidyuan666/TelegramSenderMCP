"""
Main entry point for PetriCode bot
"""
import asyncio
import logging
from .bot import PetriBot
from .config import config

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, config.LOG_LEVEL)
)

logger = logging.getLogger(__name__)


async def main():
    """Main function"""
    try:
        bot = PetriBot()
        await bot.run()
    except Exception as e:
        logger.error(f"Error running bot: {e}")
        raise


if __name__ == '__main__':
    asyncio.run(main())
