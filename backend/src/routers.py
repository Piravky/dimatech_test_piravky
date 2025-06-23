from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from src.auth.router import auth_router
from src.users.router import user_router

http_bearer = HTTPBearer(auto_error=False)
router_v1 = APIRouter(
    prefix='/api/v1',
    dependencies=[Depends(http_bearer)]
)
router_v1.include_router(auth_router)
router_v1.include_router(user_router)
