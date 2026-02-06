import logging
import sys


def setup_logging():
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Создаем обработчик для stdout
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Создаем обработчик для файла
    file_handler = logging.FileHandler('app.log')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Получаем корневой логгер и настраиваем его
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    # Устанавливаем уровень для библиотек
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    logging.getLogger('uvicorn').setLevel(logging.INFO)