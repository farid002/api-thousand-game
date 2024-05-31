"""TODO: Write docstring"""

from fastapi import APIRouter

from thousand_api.game import *

router = APIRouter()


@router.get("/all")
def get_games_endpoint():
    """TODO: Write docstring"""
    return get_games()


@router.get("/{game_id}")
def get_game_endpoint(game_id: str):
    """TODO: Write docstring"""
    return get_game(game_id)


@router.delete("/{game_id}")
def delete_game_endpoint(game_id):
    """TODO: Write docstring"""
    return delete_game(game_id)


@router.put("/{game_id}/edit")
def update_game_endpoint(game_id, player0_id, player1_id, player2_id):
    """TODO: Write docstring"""
    return update_game(game_id, player0_id, player1_id, player2_id)


@router.get("/{game_id}/bid_winner")
def get_bid_winner_local_id_endpoint(game_id: str = "game1"):
    """TODO: Write docstring"""
    return get_bid_winner_local_id(game_id)
