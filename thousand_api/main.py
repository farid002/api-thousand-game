"""TODO: Write docstring"""

import uvicorn
from fastapi import FastAPI

from thousand_api.core.game_core import *
from thousand_api.db.database import database_init
from thousand_api.endpoints.game import router as games_router
from thousand_api.endpoints.player import router as player_router

app = FastAPI()


@app.put("/game")
async def create_game_endpoint(players: List[str]):
    """TODO: Write docstring"""
    return create_game(players)


@app.put("/game/{game_id}/start_round")
def start_round_endpoint(game_id: str = "game1"):
    """TODO: Write docstring"""
    return start_round(game_id=game_id)


@app.put("/game/{game_id}/make_bid")
def make_bid_endpoint(game_id: str = "game1", player_id: str = "farid", bid: int = 100):
    """TODO: Write docstring"""
    return make_bid(game_id, player_id, bid)


@app.put("/game/{game_id}/pass_bid")
def pass_bid_endpoint(game_id: str = "game1", player_id: str = "farid"):
    """Passing during the bidding"""
    return pass_bid(game_id, player_id)


@app.put("/game/{game_id}/take_talon")
def take_talon_endpoint(game_id: str, player_id: str):
    """TODO: Write docstring"""
    return take_talon(game_id, player_id)


@app.put("/game/{game_id}/give_two_cards")
def give_two_cards_endpoint(game_id: str, player_id: str, card1: str, card2: str):
    """TODO: Write docstring"""
    return give_two_cards(game_id, player_id, card1, card2)


@app.put("/game/{game_id}/make_final_bid")
def make_final_bid_endpoint(game_id: str, player_id: str = "farid", final_bid: int = 120):
    """TODO: Write docstring"""
    return make_final_bid(game_id, player_id, final_bid)


@app.put("/game/{game_id}/play_card")
def play_card_endpoint(game_id: str, player_id: str, card: str):
    """TODO: Write docstring"""
    return play_card(game_id, player_id, card)


@app.put("game/{game_id}/finalize_round")
def finalize_round_endpoint(game_id: str):
    """TODO: Write docstring"""
    return finalize_round(game_id)


app.include_router(games_router, prefix="/game", tags=["games"])
app.include_router(player_router, prefix="/player", tags=["players"])

if __name__ == "__main__":
    database_init()
    uvicorn.run(app, host="0.0.0.0", port=5002)
