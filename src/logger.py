""" Кастомный логгер (библиотека loguru)
"""
from loguru import logger


logger.add(
    "logging/parser.log",
    format="{time} {level} {message}",
    level="DEBUG",
    rotation="2 MB",
    compression="zip",
    serialize=True
)
