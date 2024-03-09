"""TODO: Write docstring"""

import uvicorn
from database import database_init
from fastapi import FastAPI
from game import *

app = FastAPI()


@app.get("/start_round")
def start_round_endpoint(game_id: str):
    """TODO: Write docstring"""
    return start_round(game_id=game_id)


@app.put("/make_bid")
def make_bid_endpoint(game_id: str, player_local_id: int, bid: int):
    """TODO: Write docstring"""
    return make_bid(game_id, player_local_id, bid)


@app.put("/take_three_cards")
def take_three_cards_endpoint(player: str, card: str):
    """TODO: Write docstring"""
    return take_three_cards(player, card)


@app.put("/give_two_cards")
def give_two_cards_endpoint(player: str, card: str):
    """TODO: Write docstring"""
    return give_two_cards(player, card)


@app.put("/make_last_bid")
def make_last_bid_endpoint(player: str, last_bid: int):
    """TODO: Write docstring"""
    return make_last_bid(player, last_bid)


@app.put("/play_card")
def play_card_endpoint(player: str, card: str):
    """TODO: Write docstring"""
    return play_card(player, card)


@app.put("/finalize_round")
def finalize_round_endpoint(player: str, card: str):
    """TODO: Write docstring"""
    return finalize_round(player, card)


@app.get("/game")
def get_game_endpoint(game_id: str):
    """TODO: Write docstring"""
    return get_game(game_id)


@app.put("/game")
async def create_game_endpoint(game_id: str, players: List[str]):
    """TODO: Write docstring"""
    return create_game(game_id, players)


if __name__ == "__main__":
    database_init()
    uvicorn.run(app, host="localhost", port=5000)
