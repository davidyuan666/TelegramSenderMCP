"""
URL content fetcher service
"""
import logging
import aiohttp
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


async def fetch_url_content(url: str, timeout: int = 10) -> str:
    """
    Fetch content from a URL

    Args:
        url: The URL to fetch
        timeout: Request timeout in seconds

    Returns:
        Extracted text content from the URL
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=timeout) as response:
                response.raise_for_status()
                html = await response.text()

                # Parse HTML and extract text
                soup = BeautifulSoup(html, 'lxml')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text
                text = soup.get_text()

                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)

                return text

    except Exception as e:
        logger.error(f"Error fetching URL {url}: {e}")
        raise
