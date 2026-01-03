from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.db_helper import db_helper
from typing import AsyncGenerator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from contextlib import asynccontextmanager

from fastapi.responses import ORJSONResponse
from app.routes import router as api_router
from app.routes import ws_router

from redis.asyncio import Redis


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # # startup
    redis = Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db.cache,
    )
    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )

    yield
    # shutdown

    await db_helper.dispose()


app = FastAPI(
    title=settings.app_name,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    debug=settings.debug,
    docs_url=settings.api.docs,
    redoc_url=settings.api.redoc,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")

app.include_router(api_router)
app.include_router(ws_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to fastapi shop API",
        "docs": "api/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}
