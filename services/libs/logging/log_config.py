import logging
import sys
import os
from pathlib import Path


def setup_logging():
    """Настройка логирования, предотвращающая дублирование при reload"""

    # Создаем директорию для логов
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Основной форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Настраиваем корневой логгер
    root_logger = logging.getLogger()

    # Очищаем существующие обработчики (важно для предотвращения дублирования)
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Добавляем обработчики только если их нет
    if not root_logger.handlers:
        # Консольный обработчик
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        # Файловый обработчик
        file_handler = logging.FileHandler(
            log_dir / 'app.log',
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)  # В файл только INFO и выше

        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(console_handler)
        root_logger.addHandler(file_handler)

    # Настраиваем уровни для библиотек
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)  # Скрываем запросы

    return root_logger