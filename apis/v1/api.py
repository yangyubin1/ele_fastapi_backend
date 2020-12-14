from fastapi import APIRouter

from apis.v1 import health, user, user2, cities, captchas, pois, entry, pois2, shops, ugc, cart

api_v1_router = APIRouter()
api_v1_router.include_router(health.router, prefix="/v1/health", tags=["健康页"])
api_v1_router.include_router(user.router, prefix="/v1/user", tags=["用户"])
api_v1_router.include_router(user2.router, prefix="/v2/login", tags=["用户2"])
api_v1_router.include_router(cities.router, prefix="/v1/cities", tags=["城市"])
api_v1_router.include_router(pois.router, prefix="/v1/pois", tags=["位置"])
api_v1_router.include_router(pois2.router, prefix="/v2/pois", tags=["位置"])
api_v1_router.include_router(shops.router, prefix="/shopping", tags=["位置"])
api_v1_router.include_router(ugc.router, prefix="/ugc/v2", tags=["评价"])
api_v1_router.include_router(cart.router, prefix="/v1/carts", tags=["购物车"])
api_v1_router.include_router(captchas.router, prefix="/v1/captchas", tags=["验证码"])
api_v1_router.include_router(entry.router, prefix="/v2/index_entry", tags=["入口"])
