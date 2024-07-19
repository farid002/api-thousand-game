"""TODO: Write docstring"""

from fastapi import APIRouter

from thousand_api.core.table_core import (
    add_player,
    create_table,
    delete_table,
    get_players,
    get_table,
    get_tables,
    make_ready,
    make_unready,
    update_table,
)

router = APIRouter()


@router.get("/all")
def get_tables_endpoint():
    """TODO: Write docstring"""
    return get_tables()


@router.post("")
def create_table_endpoint(
    creator_player_id: str,
    entry_coins: int,
    reliable: bool = False,
    ace_marriage: bool = False,
    game_speed: int = 2,
    password: int = None,
    till_1001: bool = False,
):
    """TODO: Write docstring"""
    return create_table(creator_player_id, entry_coins, reliable, ace_marriage, game_speed, password, till_1001)


@router.get("/{table_id}")
def get_table_endpoint(table_id: str):
    """TODO: Write docstring"""
    return get_table(table_id)


@router.delete("/{table_id}")
def delete_table_endpoint(table_id):
    """TODO: Write docstring"""
    return delete_table(table_id)


@router.put("/{table_id}/edit")
def update_table_endpoint(table_id, player0_id, player1_id, player2_id):
    """TODO: Write docstring"""
    return update_table(table_id, player0_id, player1_id, player2_id)


@router.get("/{table_id}/players")
def get_players_endpoint(table_id: str):
    """TODO: Write docstring"""
    return get_players(table_id=table_id)


@router.get("/{table_id}/player")
def add_player_endpoint(table_id: str, player_id: str):
    """TODO: Write docstring"""
    return add_player(table_id=table_id, player_id=player_id)


@router.post("/{table_id}/ready/{player_local_id}")
def make_ready_player_endpoint(table_id: str, player_local_id: int):
    """Make a player ready when he/she presses ready button"""
    return make_ready(table_id=table_id, player_local_id=player_local_id)


@router.post("/{table_id}/unready/{player_local_id}")
def make_unready_player_endpoint(table_id: str, player_local_id: int):
    """Make a player ready when he/she presses ready button"""
    return make_unready(table_id=table_id, player_local_id=player_local_id)
