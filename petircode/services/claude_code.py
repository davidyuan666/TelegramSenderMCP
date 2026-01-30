"""
Claude Code CLI service for executing computer operations
"""
import logging
import asyncio
from ..config import config

logger = logging.getLogger(__name__)


async def execute_claude_code(operation: str, timeout: int = None) -> dict:
    """
    Execute a Claude Code CLI operation

    Args:
        operation: The operation description to execute
        timeout: Timeout in seconds (default: from config)

    Returns:
        dict with keys:
            - stdout: Standard output
            - stderr: Standard error
            - return_code: Process return code
            - success: Boolean indicating success

    Raises:
        Exception: If execution fails
    """
    if timeout is None:
        timeout = config.CLAUDE_TIMEOUT

    try:
        # Create subprocess to run claude CLI
        process = await asyncio.create_subprocess_exec(
            config.CLAUDE_CLI_PATH,
            operation,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise Exception(f"Operation timed out after {timeout} seconds")

        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace')
        stderr_text = stderr.decode('utf-8', errors='replace')

        return {
            'stdout': stdout_text,
            'stderr': stderr_text,
            'return_code': process.returncode,
            'success': process.returncode == 0
        }

    except FileNotFoundError:
        logger.error(f"Claude CLI not found at: {config.CLAUDE_CLI_PATH}")
        raise Exception(
            "Claude Code CLI not found. Please install it first.\n"
            "Visit: https://github.com/anthropics/claude-code"
        )
    except Exception as e:
        logger.error(f"Error executing Claude Code: {e}")
        raise
