import logging
from loguru import logger
from typing import Any, Optional


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record: logging.LogRecord) -> Any:
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record: logging.LogRecord) -> None:
        logger_opt = logger.opt(depth=8, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


async def setup_logging(level: Optional[int] = logging.INFO) -> None:
    """
    Set up logging configuration to integrate standard logging with Loguru.

    Args:
        level (Optional[int]): The logging level for the standard logging module. Defaults to logging.INFO.
    """
    try:
        logging.basicConfig(handlers=[InterceptHandler()], level=level)
        logger.info("Logging has been configured successfully.")
    except Exception as e:
        logger.error(f"Error during logging setup: {e}")
        raise
