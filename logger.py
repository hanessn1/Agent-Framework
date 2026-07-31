import logging
import sys
import os
from datetime import datetime
from config import LOG_LEVEL


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\x1b[36m",
        "INFO": "\x1b[32m",
        "WARNING": "\x1b[33m",
        "ERROR": "\x1b[31m",
        "CRITICAL": "\x1b[31;1m",
    }

    def format(self, record):
        color = self.COLORS.get(record.levelname, "")
        record.levelname = f"{color}{record.levelname}\x1b[0m"
        return super().format(record)


def setup_logging(level=LOG_LEVEL, log_to_file=True, log_filename="agent.log"):
    """Sets up standardized logging across the framework."""
    fmt = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    date_fmt = "%Y-%m-%d %H:%M:%S"

    # Terminal handler (with colors)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(ColoredFormatter(fmt, datefmt=date_fmt))
    handlers = [console_handler]

    # File handler (plain text, no color codes)
    if log_to_file:
        file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
        file_handler.setFormatter(logging.Formatter(fmt, datefmt=date_fmt))
        handlers.append(file_handler)

    logging.basicConfig(level=level, handlers=handlers)

    # Mute 3rd-party library loggers
    third_party_loggers = [
        "httpx",
        "httpcore",
        "openai",
        "urllib3",
        "fastapi",
        "uvicorn",
        "asyncio",
    ]
    for logger_name in third_party_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)