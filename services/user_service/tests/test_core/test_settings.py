import asyncio

from services.user_service.app.core.config import settings


async def test_db_config():
    print("DB Configuration:")
    print(f"URL: {settings.db.url}")

    # Try to connect
    import asyncpg
    try:
        # Retrieve params from URL
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
        print("Connection was successful!")
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")


asyncio.run(test_db_config())