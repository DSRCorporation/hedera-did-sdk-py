import logging
import re
from typing import Literal, TypeAlias

LogLevel: TypeAlias = Literal["DEBUG", "INFO", "WARN", "ERROR"]


def configure_logger(logger, log_level: LogLevel | None, log_format: str | None):
    """Helper function to configure SDK logger.

    Args:
        logger: Logger instance
        log_level: Log level
        log_format: Log format, should follow Java formatting pattern: https://logback.qos.ch/manual/layouts.html#ClassicPatternLayout
    """
    if log_level is None:
        log_level = "INFO"

    if log_format is None:
        log_format = "%d %level: %logger: %msg%n"

    # Translate from Java's logback.qos.ch formatting to Python formatting
    log_format = (
        log_format.replace("%d", "%(asctime)s")
        .replace("%level", "%(levelname)s")
        .replace("%logger", "%(filename)s")
        .replace("%msg", "%(message)s")
        .replace("%n", "")
    )

    # If there are any "%" tokens left, which aren't the already translated "%(.*)s" ones, they are not supported
    if re.search(r"%[^(]", log_format):
        raise Exception("Invalid log format token detected")

    logger.setLevel(log_level)
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter(log_format))
    logger.addHandler(console)
