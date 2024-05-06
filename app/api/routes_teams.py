from fastapi import APIRouter, HTTPException, Header
from app.api.jwt.jwt import verify_jwt_token
from app.database.models import UserStatusesOrm, UserTeamOrm
from app.repository import Repository
from .models import Team, UserTeam, UserStatuses


router_teams = APIRouter(prefix="/team", tags=["Команды"])


@router_teams.post("/create")
async def team_add(team: Team, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    return await Repository.add_team(data=team, user_id=user.id)


@router_teams.delete("/delete")
async def team_delete(team_id: int, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    return await Repository.del_team(team_id)


@router_teams.post("/join")
async def team_join(team_id: int, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    # TODO: проверка доступа 
    user_team = UserTeamOrm()
    user_team.role = UserStatusesOrm.USER
    user_team.team_id = team_id
    user_team.user_id = user.id
    return await Repository.join_to_team(user_team)


@router_teams.put("/leave")
async def team_leave(team_id: int, token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    return await Repository.leave_team(user_id=user.id, team_id=team_id)


@router_teams.get("/my_teams")
async def my_teams(token_authorization: str | None = Header(default=None)):
    if not token_authorization:
        raise HTTPException(status_code=400, detail="uncorrect header")
    user = await verify_jwt_token(token_authorization)
    return await Repository.get_all_teams_by_user_id(user.id)


