import logging
import sys
from pathlib import Path


def setup_logging(
    log_level: str = "DEBUG",
    file_log_level: str = "INFO",
    log_dir: Path | None = None,
) -> logging.Logger:
    """
    Configure logging for the application.

    This function ensures no duplicate handlers are added, which is especially
    important when using uvicorn with reload=True.

    Args:
        log_level: Log level for console output (DEBUG, INFO, WARNING, etc.).
        file_log_level: Log level for file output.
        log_dir: Directory for log files. If None, uses "logs" in current dir.

    Returns:
        Configured root logger.
    """

    # Create log directory if needed
    if log_dir is None:
        log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Get root logger and remove any existing handlers
    # (prevents duplication when reloading in uvicorn)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Set root logger level
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, log_level.upper()))
    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(
        log_dir / 'app.log',
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, file_log_level.upper()))
    root_logger.addHandler(file_handler)

    # Configure third-party loggers
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)

    return root_logger