from fastapi import APIRouter, HTTPException, Header
from app.api.jwt.jwt import verify_jwt_token
from app.database.models import UserStatusesOrm, UserTeamOrm
from app.api.models import AddresInfo
from app.repository import Repository


router_addresses = APIRouter(prefix="/address", tags=["Адреса"])


@router_addresses.post("/add_address_info")
async def address_info_add(address_info: AddresInfo, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    ret_val = await Repository.add_address_info(data=address_info)
    if not ret_val:
        raise HTTPException(status_code=400, detail="addition error")
    return ret_val


@router_addresses.get("/get_address_info_by_user_id")
async def get_address_info_by_user_id(token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    ret_val = await Repository.get_address_info_by_user_id(user_id=user.id)
    if not ret_val:
        raise HTTPException(status_code=400, detail="addition error")
    return ret_val


@router_addresses.get("/get_address_info_by_team")
async def get_address_info_by_user_id(token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    raise HTTPException(status_code=400, detail="todo: ...")