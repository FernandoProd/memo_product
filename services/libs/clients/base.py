import httpx


class BaseClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def post(self, endpoint: str, **kwargs):
        async with httpx.AsyncClient(base_url=self.base_url) as client:
            try:
                response = await client.post(endpoint, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                raise e
            except Exception as e:
                # Любые другие исключения
                raise

    async def get(self):
        pass