from fastapi import APIRouter
from app.core.config import settings


from .products import router as products_router
from .categories import router as categories_router
from .cart import router as cart_router
from .user import router as users_router
from .profile import router as profile_router
from .orders import router as orders_router
from .post import router as posts_router
from .city import router as cities_router
from .auth import router as auth_base_router
from .ws_orders import router as ws_orders_router

router = APIRouter(prefix=settings.api.prefix)
auth_router = APIRouter(prefix=settings.api.auth)
ws_router = APIRouter(prefix=settings.ws.prefix)

auth_router.include_router(auth_base_router)

router.include_router(users_router, prefix=settings.api.users)
router.include_router(profile_router, prefix=settings.api.profile)
router.include_router(posts_router, prefix=settings.api.posts)
router.include_router(categories_router, prefix=settings.api.categories)
router.include_router(products_router, prefix=settings.api.products)
router.include_router(cart_router, prefix=settings.api.cart)
router.include_router(orders_router, prefix=settings.api.orders)
router.include_router(cities_router, prefix=settings.api.cities)

ws_router.include_router(ws_orders_router, prefix=settings.ws.orders)
