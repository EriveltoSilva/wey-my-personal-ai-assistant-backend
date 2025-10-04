"""main module for the FastAPI application"""

import asyncio
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.agents.routes import router as agent_routes
from src.auth.routes import router as auth_routes
from src.chats.background_tasks import background_tasks
from src.chats.routes import router as chat_routes
from src.chats.routes_streaming import router as chat_streaming_routes
from src.core.config import settings
from src.core.database import create_and_seed_database
from src.exceptions import NotFoundException, TypeErrorException, UnauthorizedException
from src.exceptions.exception_handlers import http_exception_handler
from src.users.interest_routes import router as interest_routes
from src.users.professional_area_routes import router as professional_area_routes
from src.users.routes import router as user_routes
from src.websocket.routes import router as websocket_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the FastAPI app."""

    print("STARTING SERVER...")
    await create_and_seed_database(False)
    await background_tasks.start_processing()
    yield
    await background_tasks.stop_processing()
    print("STOPPING SERVER...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@lru_cache
def get_settings():
    """Get settings."""
    return settings


@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"message": "API OK"}


app.add_exception_handler(NotFoundException, http_exception_handler)
app.add_exception_handler(UnauthorizedException, http_exception_handler)
app.add_exception_handler(TypeErrorException, http_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)

app.include_router(websocket_routes)
app.include_router(auth_routes, prefix=settings.API_V1_STR)
app.include_router(agent_routes, prefix=settings.API_V1_STR)
app.include_router(user_routes, prefix=settings.API_V1_STR)
app.include_router(interest_routes, prefix=settings.API_V1_STR)
app.include_router(professional_area_routes, prefix=settings.API_V1_STR)
app.include_router(chat_routes, prefix=settings.API_V1_STR)
app.include_router(chat_streaming_routes, prefix=settings.API_V1_STR)


# Mount static files for uploads
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


if __name__ == "__main__":
    asyncio.run(create_and_seed_database(False))

    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)
