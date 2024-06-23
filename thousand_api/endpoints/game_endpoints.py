"""TODO: Write docstring"""

from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from http import HTTPStatus
import jwt

from thousand_api.core.game_core import (
    delete_game,
    get_bid_winner_local_id,
    get_current_round,
    get_game,
    get_games,
    get_players,
    update_game,
)

router = APIRouter()


def protected(token: str) -> str:
    """Get token, verify and return user_id"""
    decoded = jwt.decode(jwt=token, key='victoriasecret', algorithms=["HS256"])
    user = decoded.get('sub', None)
    return user


@router.get("/authenticate")
def authenticate(username: str, password: str):
    """If username, password are correct return token"""
    if username == 'admin' and password == 'admin':
        now = datetime.now(timezone.utc)
        token = jwt.encode({"sub": username, "exp": now + timedelta(hours=3)}, key='victoriasecret', algorithm="HS256")
        response_map = {}
        response_map['data'] = token
        response_map['message'] = f"{username} logged in successfully"
        return JSONResponse(status_code=HTTPStatus.CREATED, content=response_map)
    else:
        return JSONResponse(status_code=HTTPStatus.UNAUTHORIZED, content="Invalid username or password")


@router.get("/all")
def get_games_endpoint(user_id: Annotated[str, Depends(protected)]):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=get_games())


@router.get("/{game_id}")
def get_game_endpoint(user_id: Annotated[str, Depends(protected)], game_id: str):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=get_game(game_id))


@router.delete("/{game_id}")
def delete_game_endpoint(user_id: Annotated[str, Depends(protected)], game_id):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=delete_game(game_id))


@router.put("/{game_id}/edit")
def update_game_endpoint(user_id: Annotated[str, Depends(protected)], game_id, player0_id, player1_id, player2_id):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.CREATED, content=update_game(game_id, player0_id, player1_id, player2_id))


@router.get("/{game_id}/players")
def get_players_endpoint(user_id: Annotated[str, Depends(protected)], game_id: str):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=get_players(game_id=game_id))


@router.get("/{game_id}/current_round")
def get_current_round_endpoint(user_id: Annotated[str, Depends(protected)], game_id: str):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=get_current_round(game_id=game_id))


@router.get("/{game_id}/bid_winner")
def get_bid_winner_local_id_endpoint(user_id: Annotated[str, Depends(protected)], game_id: str):
    """TODO: Write docstring"""
    return JSONResponse(status_code=HTTPStatus.OK, content=get_bid_winner_local_id(game_id))
