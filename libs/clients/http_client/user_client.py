from libs.clients.base import BaseClient
import httpx

class UserServiceClient(BaseClient):
    def __init__(self):
        super().__init__(base_url="http://localhost:8000") # Ссылку вывести потом в отдельное место
                                                                # (чтобы все ссылки хранились централизованно, консолидированно)

    async def verify_password(self,
                              email: str,
                              password: str
                              ):
            response = await self.post(
                "/api/api/v1/users/verify",   # тут ошибка должно быть  api/v1/users/verify
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
        response = await self.get(f'/api/api/v1/users/{user_id}')

        return response
