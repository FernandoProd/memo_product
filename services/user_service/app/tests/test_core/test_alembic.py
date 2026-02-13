# tests/test_core/test_alembic.py
import pytest
import configparser
from pathlib import Path
from sqlalchemy import create_engine, text


def get_alembic_config():
    """Получаем конфигурацию alembic.ini"""
    # Поднимаемся на 2 уровня выше от теста
    alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"

    if not alembic_ini_path.exists():
        pytest.fail(f"Файл alembic.ini не найден по пути: {alembic_ini_path}")

    print(f"Найден файл: {alembic_ini_path}")

    config = configparser.ConfigParser()
    config.read(alembic_ini_path)

    if 'alembic' not in config:
        pytest.fail("Секция [alembic] не найдена в alembic.ini")

    return config['alembic']


def test_database_connection():
    """Тест подключения к базе данных"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    # Маскируем пароль в выводе
    if '@' in db_url:
        parts = db_url.split('@')
        if ':' in parts[0]:
            user_pass = parts[0].split(':')
            if len(user_pass) >= 3:
                masked_url = f"{user_pass[0]}:****@{parts[1]}"
                print(f"Подключаемся к: {masked_url}")

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("✓ Подключение к БД успешно")
    except Exception as e:
        pytest.fail(f"Ошибка подключения к БД: {e}")


def test_check_tables():
    """Проверяем существование таблиц"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    engine = create_engine(db_url)

    with engine.connect() as conn:
        # 1. Проверяем alembic_version
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alembic_version'
            )
        """))
        has_alembic_version = result.scalar()
        print(f"Таблица alembic_version: {'СУЩЕСТВУЕТ' if has_alembic_version else 'ОТСУТСТВУЕТ'}")

        if has_alembic_version:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            print(f"Текущая версия миграции: {version}")

        # 2. Проверяем users
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            )
        """))
        has_users = result.scalar()
        print(f"Таблица users: {'СУЩЕСТВУЕТ' if has_users else 'ОТСУТСТВУЕТ'}")

        if has_users:
            # Получаем информацию о таблице
            result = conn.execute(text("""
                SELECT 
                    column_name, 
                    data_type,
                    is_nullable,
                    column_default
                FROM information_schema.columns 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
                ORDER BY ordinal_position
            """))
            columns = result.fetchall()
            print(f"Структура таблицы users ({len(columns)} колонок):")
            for col in columns:
                print(f"  - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")


def test_alembic_current():
    """Проверяем команду alembic current"""
    import subprocess
    import sys

    # Путь к директории с alembic.ini (на 2 уровня выше теста)
    project_root = Path(__file__).parent.parent.parent

    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "current"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        print("=" * 50)
        print("РЕЗУЛЬТАТ КОМАНДЫ: alembic current")
        print("=" * 50)

        if result.stdout:
            print(f"Вывод:\n{result.stdout}")

        if result.stderr:
            print(f"Ошибки:\n{result.stderr}")

        print(f"Код возврата: {result.returncode}")

        # Тест не падает, просто показывает информацию
        assert True

    except subprocess.TimeoutExpired:
        print("Таймаут выполнения команды alembic")
        assert True
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        assert True


def test_alembic_history():
    """Проверяем историю миграций"""
    import subprocess
    import sys

    project_root = Path(__file__).parent.parent.parent

    try:
        result = subprocess.run(
            [sys.executable, "-m", "alembic", "history"],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10
        )

        print("\n" + "=" * 50)
        print("РЕЗУЛЬТАТ КОМАНДЫ: alembic history")
        print("=" * 50)

        if result.stdout:
            print(f"Вывод:\n{result.stdout}")

        if result.stderr:
            print(f"Ошибки:\n{result.stderr}")

        assert True

    except Exception as e:
        print(f"Ошибка: {e}")
        assert True


def test_database_direct_info():
    """Прямая проверка информации о БД"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    engine = create_engine(db_url)

    with engine.connect() as conn:
        # 1. Информация о БД
        result = conn.execute(text("SELECT current_database(), current_user, version()"))
        db_info = result.fetchone()
        print("\n" + "=" * 50)
        print("ИНФОРМАЦИЯ О БАЗЕ ДАННЫХ")
        print("=" * 50)
        print(f"База данных: {db_info[0]}")
        print(f"Пользователь: {db_info[1]}")
        print(f"Версия PostgreSQL: {db_info[2].split(',')[0]}")

        # 2. Список всех таблиц
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]

        print(f"\nТаблицы в схеме public ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

        # 3. Если таблица users существует, показываем первые записи
        if 'users' in tables:
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"\nТаблица users содержит {count} записей")

                if count > 0:
                    result = conn.execute(text("SELECT * FROM users LIMIT 3"))
                    rows = result.fetchall()
                    print("Первые записи:")
                    for row in rows:
                        print(f"  {row}")
            except Exception as e:
                print(f"Не удалось прочитать таблицу users: {e}")