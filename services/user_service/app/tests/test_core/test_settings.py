import asyncio
from app.core.config import settings


async def test_db_config():
    print("DB Configuration:")
    print(f"URL: {settings.db.url}")

    # Попробуйте подключиться
    import asyncpg
    try:
        # Извлеките параметры из URL
        url = settings.db.url
        # postgresql+asyncpg://user:pass@host:port/dbname
        parts = url.split('://')[1].split('@')
        user_pass = parts[0].split(':')
        host_port_db = parts[1].split('/')

        conn = await asyncpg.connect(
            user=user_pass[0],
            password=user_pass[1],
            host=host_port_db[0].split(':')[0],
            port=int(host_port_db[0].split(':')[1]) if ':' in host_port_db[0] else 5432,
            database=host_port_db[1]
        )
        print("✅ Подключение успешно!")
        await conn.close()
    except Exception as e:
        print(f"❌ Ошибка: {e}")


asyncio.run(test_db_config())