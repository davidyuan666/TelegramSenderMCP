"""
Claude Code CLI service for executing computer operations
"""
import logging
import asyncio
from typing import AsyncGenerator, Dict, Any
from ..config import config

logger = logging.getLogger(__name__)


async def execute_claude_code(operation: str, timeout: int = None) -> dict:
    """
    Execute Claude Code CLI operation via PowerShell in specified working directory

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

    # Build PowerShell command to change directory and run claude CLI
    # Add --dangerously-skip-permissions to skip permission prompts
    powershell_cmd = (
        f'powershell.exe -Command "'
        f'cd \'{config.CLAUDE_WORK_DIR}\'; '
        f'claude --dangerously-skip-permissions \'{operation}\'"'
    )

    logger.info(f"Executing Claude CLI command: {operation}")
    logger.info(f"Working directory: {config.CLAUDE_WORK_DIR}")

    try:
        # Create subprocess to run PowerShell command
        process = await asyncio.create_subprocess_shell(
            powershell_cmd,
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

        logger.info(f"Command completed with return code: {process.returncode}")
        logger.info(f"STDOUT length: {len(stdout_text)}")

        return {
            'stdout': stdout_text,
            'stderr': stderr_text,
            'return_code': process.returncode,
            'success': process.returncode == 0
        }

    except Exception as e:
        logger.error(f"Error executing Claude Code: {e}", exc_info=True)
        raise


async def execute_claude_code_with_status(
    operation: str,
    timeout: int = None
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Execute Claude Code CLI with real-time status updates

    Args:
        operation: The operation description to execute
        timeout: Timeout in seconds (default: from config)

    Yields:
        Status updates as dictionaries with 'type' and 'message' or 'data'
    """
    if timeout is None:
        timeout = config.CLAUDE_TIMEOUT

    yield {'type': 'status', 'message': 'Claude Code正在初始化...'}

    # Build PowerShell command
    powershell_cmd = (
        f'powershell.exe -Command "'
        f'cd \'{config.CLAUDE_WORK_DIR}\'; '
        f'claude --dangerously-skip-permissions \'{operation}\'"'
    )

    logger.info(f"Executing Claude CLI command: {operation}")
    logger.info(f"Working directory: {config.CLAUDE_WORK_DIR}")

    yield {'type': 'status', 'message': 'Claude Code正在执行命令...'}

    try:
        # Create subprocess
        process = await asyncio.create_subprocess_shell(
            powershell_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        yield {'type': 'progress', 'message': 'Claude Code正在处理中...'}

        # Wait for completion with timeout
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            yield {
                'type': 'result',
                'data': {
                    'stdout': '',
                    'stderr': f'操作超时（{timeout}秒）',
                    'return_code': -1,
                    'success': False
                }
            }
            return

        # Decode output
        stdout_text = stdout.decode('utf-8', errors='replace')
        stderr_text = stderr.decode('utf-8', errors='replace')

        logger.info(f"Command completed with return code: {process.returncode}")

        yield {
            'type': 'result',
            'data': {
                'stdout': stdout_text,
                'stderr': stderr_text,
                'return_code': process.returncode,
                'success': process.returncode == 0
            }
        }

    except Exception as e:
        logger.error(f"Error executing Claude Code: {e}", exc_info=True)
        yield {
            'type': 'result',
            'data': {
                'stdout': '',
                'stderr': str(e),
                'return_code': -1,
                'success': False
            }
        }
