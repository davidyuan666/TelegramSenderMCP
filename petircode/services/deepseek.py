"""
DeepSeek AI service for handling AI chat queries
"""
import logging
import aiohttp
from ..config import config

logger = logging.getLogger(__name__)


async def query_deepseek(prompt: str, max_tokens: int = 2000) -> str:
    """
    Query DeepSeek AI API with a prompt

    Args:
        prompt: The user's question or prompt
        max_tokens: Maximum tokens in the response (default: 2000)

    Returns:
        AI generated response text

    Raises:
        Exception: If API call fails
    """
    if not config.DEEPSEEK_API_KEY:
        raise ValueError("DEEPSEEK_API_KEY is not configured")

    headers = {
        "Authorization": f"Bearer {config.DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": config.DEEPSEEK_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.7
    }

    try:
        timeout = aiohttp.ClientTimeout(total=30)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(
                config.DEEPSEEK_API_URL,
                headers=headers,
                json=payload
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"DeepSeek API error: {response.status} - {error_text}")
                    raise Exception(f"API returned status {response.status}: {error_text}")

                data = await response.json()

                # Extract the response text
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise Exception("Invalid response format from API")

    except aiohttp.ClientError as e:
        logger.error(f"Network error calling DeepSeek API: {e}", exc_info=True)
        raise Exception(f"Network error: {str(e)}")
    except Exception as e:
        logger.error(f"Error querying DeepSeek: {e}", exc_info=True)
        raise
