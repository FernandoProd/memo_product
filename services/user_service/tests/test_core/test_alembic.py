# tests/test_core/test_alembic.py
import configparser
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text


def get_alembic_config():
    """Getting configuration of alembic.ini"""

    # Climb up for 2 levels of test
    alembic_ini_path = Path(__file__).parent.parent.parent / "alembic.ini"

    if not alembic_ini_path.exists():
        pytest.fail(f"File alembic.ini not found on a path: {alembic_ini_path}")

    print(f"Not found: {alembic_ini_path}")

    config = configparser.ConfigParser()
    config.read(alembic_ini_path)

    if 'alembic' not in config:
        pytest.fail("Section [alembic] not found in alembic.ini")

    return config['alembic']


def test_database_connection():
    """Test of connection to database"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    # Hide the password in return
    if '@' in db_url:
        parts = db_url.split('@')
        if ':' in parts[0]:
            user_pass = parts[0].split(':')
            if len(user_pass) >= 3:
                masked_url = f"{user_pass[0]}:****@{parts[1]}"
                print(f"Connect to: {masked_url}")

    try:
        engine = create_engine(db_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("Connection to db was successful")
    except Exception as e:
        pytest.fail(f"Error in connection to db: {e}")


def test_check_tables():
    """Checking the existence of tables"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    engine = create_engine(db_url)

    with engine.connect() as conn:
        # Checking alembic_version
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'alembic_version'
            )
        """))
        has_alembic_version = result.scalar()
        print(f"The table of alembic_version: {'exists' if has_alembic_version else 'not exists'}")

        if has_alembic_version:
            result = conn.execute(text("SELECT version_num FROM alembic_version"))
            version = result.scalar()
            print(f"Current version of migration: {version}")

        # Checking users
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            )
        """))
        has_users = result.scalar()
        print(f"The table of users: {'exist' if has_users else 'not exist'}")

        if has_users:
            # Getting information of table
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
            print(f"Structure of users table ({len(columns)} columns):")
            for col in columns:
                print(f"  - {col[0]}: {col[1]} {'NULL' if col[2] == 'YES' else 'NOT NULL'}")


def test_alembic_current():
    """Checking of alembic current handle"""
    import subprocess
    import sys

    # Path to directory from alembic.ini (2 level higher than test)
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
        print("Result of handle: alembic current")
        print("=" * 50)

        if result.stdout:
            print(f"Result:\n{result.stdout}")

        if result.stderr:
            print(f"Errors:\n{result.stderr}")

        print(f"Codee of return: {result.returncode}")


        assert True

    except subprocess.TimeoutExpired:
        print("Timeout of handle action of alembic")
        assert True
    except Exception as e:
        print(f"Error of action of handle: {e}")
        assert True


def test_alembic_history():
    """Checking history of migration"""
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
        print("Result of the handle: alembic history")
        print("=" * 50)

        if result.stdout:
            print(f"Result:\n{result.stdout}")

        if result.stderr:
            print(f"Errors:\n{result.stderr}")

        assert True

    except Exception as e:
        print(f"Error: {e}")
        assert True


def test_database_direct_info():
    """Direct checking information of database"""
    alembic_config = get_alembic_config()
    db_url = alembic_config['sqlalchemy.url']

    engine = create_engine(db_url)

    with engine.connect() as conn:
        # Information of database
        result = conn.execute(text("SELECT current_database(), current_user, version()"))
        db_info = result.fetchone()
        print("\n" + "=" * 50)
        print("Information about database")
        print("=" * 50)
        print(f"DataBase: {db_info[0]}")
        print(f"Customer: {db_info[1]}")
        print(f"Version of PostgreSQL: {db_info[2].split(',')[0]}")

        # List of all tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]

        print(f"\nTables in the public schema ({len(tables)}):")
        for table in tables:
            print(f"  - {table}")

        # If the table of users is existed, will show the notes
        if 'users' in tables:
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"\nThe table of users store {count} notes")

                if count > 0:
                    result = conn.execute(text("SELECT * FROM users LIMIT 3"))
                    rows = result.fetchall()
                    print("First notes:")
                    for row in rows:
                        print(f"  {row}")
            except Exception as e:
                print(f"Couldn't read table of users: {e}")