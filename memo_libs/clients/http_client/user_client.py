from typing import Optional

from memo_libs.clients.base import BaseClient
import httpx
import logging

logger = logging.getLogger(__name__)

class UserServiceClient(BaseClient):
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None):
        super().__init__(base_url=base_url)
        self.api_key = api_key

    async def verify_password(self,
                              email: str,
                              password: str
                              ):
            response = await self.post(
                "/api/v1/users/verify",   # тут ошибка должно быть  api/v1/users/verify
                params={
                    "email": email,
                    "password": password
                }
            )
            return response

    async def get_user_by_id(
            self,
            user_id: str,
    ) -> httpx.Response:
        headers = {}
        if self.api_key:
            headers["X-Internal-Api-Key"] = self.api_key

        logger.debug(f"Sending request to /api/v1/users/{user_id} with headers: {headers}")
        response = await self.get(f'/api/v1/users/{user_id}', headers=headers)

        return response
