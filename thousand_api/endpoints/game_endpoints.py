"""TODO: Write docstring"""

from fastapi import APIRouter

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


@router.get("/{game_id}/players")
def get_players_endpoint(game_id: str):
    """TODO: Write docstring"""
    return get_players(game_id=game_id)


@router.get("/{game_id}/current_round")
def get_current_round_endpoint(game_id: str):
    """TODO: Write docstring"""
    return get_current_round(game_id=game_id)


@router.get("/{game_id}/bid_winner")
def get_bid_winner_local_id_endpoint(game_id: str):
    """TODO: Write docstring"""
    return get_bid_winner_local_id(game_id)
