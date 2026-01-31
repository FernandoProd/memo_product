from fastapi import FastAPI
from services.auth_service.api.api_v1.endpoints.auth import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)