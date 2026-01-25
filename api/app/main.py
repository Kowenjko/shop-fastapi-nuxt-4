from asyncio import create_task
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.db_helper import db_helper
from typing import AsyncGenerator

from starlette.middleware.sessions import SessionMiddleware


from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from contextlib import asynccontextmanager


from fastapi.responses import JSONResponse, ORJSONResponse
from app.routes import router as api_router
from app.routes import ws_router

from app.core.redis import redis
from app.utils import ws_redis_listener


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # # startup

    FastAPICache.init(
        RedisBackend(redis),
        prefix=settings.cache.prefix,
    )

    ws_task = create_task(ws_redis_listener())

    yield
    # shutdown
    ws_task.cancel()
    await redis.close()
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
    SessionMiddleware,
    secret_key=settings.oauth.session_secret_key,
    session_cookie="oauth_session",
    same_site="none",
    https_only=True,
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
# app.include_router(ws_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to fastapi shop API",
        "docs": "api/docs",
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/debug")
async def debug_docs(request: Request):
    return {
        "scheme": request.url.scheme,
        "base_url": str(request.base_url),
        "headers": {
            "x-forwarded-proto": request.headers.get("x-forwarded-proto"),
            "host": request.headers.get("host"),
        },
    }


@app.get("/debug-cookies")
async def debug_cookies(request: Request):
    cookies = request.cookies
    return JSONResponse(
        {"cookies": cookies}
    )  # pyright: ignore[reportUndefinedVariable]


@app.get("/debug-oauth")
async def debug_oauth(request: Request):
    session_data = request.session
    return session_data
