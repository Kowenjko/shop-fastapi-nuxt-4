from pathlib import Path
from pydantic import PostgresDsn, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Union

BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class AuthJWT(BaseModel):
    private_jwt_key: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_jwt_key: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int
    refresh_token_expire_days: int


class GithubConfig(BaseModel):
    name: str = "github"
    client_id: str
    client_secret: str
    access_token_url: str = "https://github.com/login/oauth/access_token"
    authorize_url: str = "https://github.com/login/oauth/authorize"
    api_base_url: str = "https://api.github.com/"
    client_kwargs: dict = {"scope": "user:email"}
    redirect_uri: str = "https://api.shop.local/api/auth/github/callback"


class GoogleConfig(BaseModel):
    name: str = "google"
    client_id: str
    client_secret: str
    server_metadata_url: str = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )

    client_kwargs: dict = {"scope": "openid email profile"}
    redirect_uri: str = "https://api.shop.local/api/auth/google/callback"


class OAuthConfig(BaseModel):
    session_secret_key: str
    frontend_redirect: str = "https://shop.local/"
    github: GithubConfig
    google: GoogleConfig


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    cart: str = "/cart"
    auth: str = "/auth"
    categories: str = "/categories"
    users: str = "/users"
    posts: str = "/posts"
    cities: str = "/cities"
    orders: str = "/orders"
    profile: str = "/profile"
    products: str = "/products"
    docs: str = "/api/docs"
    redoc: str = "/api/redoc"


class WsPrefix(BaseModel):
    prefix: str = "/ws"
    orders: str = "/orders"


class DatabaseConfig(BaseSettings):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class RedisDB(BaseModel):
    cache: int = 0


class RedisConfig(BaseModel):
    host: str = "redis"
    port: int = 6379
    db: RedisDB = RedisDB()


class CacheNamespace(BaseModel):
    products: str = "products"
    cities: str = "cities"
    cities_regions: str = "cities-regions"
    cities_districts: str = "cities-districts"
    cities_communities: str = "cities-communities"


class CacheConfig(BaseModel):
    prefix: str = "fastapi-cache"
    namespace: CacheNamespace = CacheNamespace()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    app_name: str = "FastAPI Shop"
    debug: bool = True
    base_url: str

    cors_origins: Union[List[str], str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://0.0.0.0:5173",
        "http://0.0.0.0:3000",
        "https://shop.local",
        "https://api.shop.local",
    ]
    static_dir: str = "static"
    images_dir: str = "static/images"
    run: RunConfig = RunConfig()
    auth_jwt: AuthJWT
    oauth: OAuthConfig
    db: DatabaseConfig
    api: ApiPrefix = ApiPrefix()
    ws: WsPrefix = WsPrefix()
    redis: RedisConfig = RedisConfig()
    cache: CacheConfig = CacheConfig()


settings = Settings()
