from libs.clients.base import BaseClient
import httpx
import logging

logger = logging.getLogger(__name__)

class AuthServiceClient(BaseClient):
    def __init__(self):
        super().__init__(base_url="http://localhost:8001")

    async def get_current_user(self, token) -> httpx.Response:
        logger.debug("Вот такой вот токен отправляется по httpx client: %s", token)
        response = await self.post(
            "/auth/verify_token",
            json={
                "token": token
            }
        )
        logger.debug("Вот такой вот ответ отв /auth/verify_token: %s", response)

        return response