from fastapi import APIRouter, HTTPException, Header, Request
from .models import User, Statistics
from ..repository import *
from .jwt import create_jwt_token, verify_jwt_token


router_users = APIRouter(prefix="/user", tags=["Пользователи"])

@router_users.post("/registration", status_code=201)
async def user_registration(user: User):
    res = await Repository.registrate_user(user)
    if not res:
        raise HTTPException(status_code=400, detail="registration error")
    return res


@router_users.get("/authorization", status_code=200)
async def user_authorization(login: str, password: str):
    current_user = await Repository.get_user_by_login(login, password)
    if current_user:
        return create_jwt_token(current_user)
    else:
        raise HTTPException(status_code=400, detail="authorization error")
    
    
@router_users.get("/info", status_code=200)
async def user_authorization(req: Request, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    return await verify_jwt_token(token_authorization)


@router_users.put("/edit")
async def user_edit(user: User, token_authorization: str | None = Header(default=None)):
    ...
    
    
@router_users.get("/statistics/get")
async def user_statistics_get(period: str, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    res = await Repository.get_statistics_by_period(user.id, period)
    return res


@router_users.get("/statistics/update")
async def user_statistics_update(statistic: str, addvalue: int, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    res = await Repository.update_statistics(user.id, statistic, addvalue)
    return res


@router_users.get("/teames")
async def user_teames(token_authorization: str | None = Header(default=None)):
    ...