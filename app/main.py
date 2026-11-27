from app.database.database import init_db, close_db
from fastapi import FastAPI
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from contextlib import asynccontextmanager
from app.api.v1.user_api_router import router as user_router
from app.api.v1.auth_api_router import router as auth_router
from app.api.v1.department_api_router import router as department_router

@asynccontextmanager
async def on_startup(app: FastAPI):
    init_db()
    yield
    close_db()

app = FastAPI()

app_v1 = FastAPI(
    title="Kanban Board API",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=on_startup
)

app.mount("/api/v1", app_v1)

app_v1.include_router(user_router)
app_v1.include_router(auth_router)
app_v1.include_router(department_router)