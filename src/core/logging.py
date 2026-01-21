import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path

from src.core.settings import settings


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "app.log"


def get_logger(name: str = "address_book") -> logging.Logger:
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger 

    logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(module)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    """ File handler with rotation """
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


logger = get_logger()
