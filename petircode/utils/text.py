"""
Utility functions for text processing
"""
import re
from typing import List


def truncate_text(text: str, max_length: int = 4000) -> str:
    """
    Truncate text to maximum length

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "\n\n... (truncated)"


def clean_text(text: str) -> str:
    """
    Clean and normalize text

    Args:
        text: Text to clean

    Returns:
        Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text
