"""TODO: Write docstring"""

from fastapi import APIRouter

from thousand_api.core.main_core import *

router = APIRouter()


@router.put("/game")
async def create_game_endpoint(table_id: str):
    """TODO: Write docstring"""
    return create_game(table_id)


@router.put("/game/{game_id}/start_round")
def start_round_endpoint(game_id: str = "game1"):
    """TODO: Write docstring"""
    return start_round(game_id=game_id)


@router.put("/game/{game_id}/make_bid")
def make_bid_endpoint(game_id: str = "game1", player_id: str = "farid", bid: int = 100):
    """TODO: Write docstring"""
    return make_bid(game_id, player_id, bid)


@router.put("/game/{game_id}/pass_bid")
def pass_bid_endpoint(game_id: str = "game1", player_id: str = "farid"):
    """Passing during the bidding"""
    return pass_bid(game_id, player_id)


@router.put("/game/{game_id}/take_talon")
def take_talon_endpoint(game_id: str, player_id: str):
    """TODO: Write docstring"""
    return take_talon(game_id, player_id)


@router.put("/game/{game_id}/fold")
def fold_endpoint(game_id: str, player_id: str):
    """TODO: Write docstring"""
    return fold(game_id, player_id)


@router.put("/game/{game_id}/give_two_cards")
def give_two_cards_endpoint(game_id: str, player_id: str, card1: str, card2: str):
    """TODO: Write docstring"""
    return give_two_cards(game_id, player_id, card1, card2)


@router.put("/game/{game_id}/make_final_bid")
def make_final_bid_endpoint(game_id: str, player_id: str = "farid", final_bid: int = 120):
    """TODO: Write docstring"""
    return make_final_bid(game_id, player_id, final_bid)


@router.put("/game/{game_id}/play_card")
def play_card_endpoint(game_id: str, player_id: str, card: str):
    """TODO: Write docstring"""
    return play_card(game_id, player_id, card)


@router.put("/game/{game_id}/finalize_round")
def finalize_round_endpoint(game_id: str):
    """TODO: Write docstring"""
    return finalize_round(game_id)
