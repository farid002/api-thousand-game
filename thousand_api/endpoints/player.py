"""TODO: Write docstring"""

from fastapi import APIRouter

from thousand_api.utils.player_utils import *

router = APIRouter()


@router.get("/")
def get_players_endpoint():
    """TODO: Write docstring"""
    return get_players()


@router.get("/{player_id}")
def get_player_endpoint(player_id: str):
    """TODO: Write docstring"""
    return get_player(player_id)


@router.delete("/{player_id}")
def delete_player_endpoint(player_id):
    """TODO: Write docstring"""
    return delete_player(player_id)


@router.put("/{player_id}/edit")
def update_player_endpoint(
        player_id,
        local_id,
        cards_init,
        cards_current,
        cards_played,
        bolt_count,
        barrel_count,
        on_barrel_since,
        round_point,
        point,
        max_biddable_amount,
        silent
    ):
    """TODO: Write docstring"""
    return update_player(
        player_id,
        local_id,
        cards_init,
        cards_current,
        cards_played,
        bolt_count,
        barrel_count,
        on_barrel_since,
        round_point,
        point,
        max_biddable_amount,
        silent
    )
