from fastapi import APIRouter, Header
from .models import Team, UserTeam, UserStatuses


router_teams = APIRouter(prefix="/team", tags=["Команды"])


@router_teams.post("/create")
async def team_add(team: Team, authorization: str | None = Header(default=None)):
    ...


@router_teams.delete("/{team_id}/delete")
async def team_delete(team_id: int, authorization: str | None = Header(default=None)):
    ...


@router_teams.post("/{team_id}/join")
async def team_join(team_id: int, authorization: str | None = Header(default=None)):
    ...
    
    
@router_teams.put("/{team_id}/leave")
async def team_leave(team_id: int, authorization: str | None = Header(default=None)):
    ...
    
    
@router_teams.get("/{team_id}/members")
async def team_members(team_id: int, authorization: str | None = Header(default=None)):
    ...


