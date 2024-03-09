"""TODO: Write docstring"""

import uvicorn
from database import database_init
from fastapi import FastAPI
from game import *

app = FastAPI()


@app.get("/start_round")
def start_round_endpoint(game_id: str = "game1"):
    """TODO: Write docstring"""
    return start_round(game_id=game_id)


@app.put("/make_bid")
def make_bid_endpoint(game_id: str = "game1", player_id: str = "farid", bid: int = 100):
    """TODO: Write docstring"""
    return make_bid(game_id, player_id, bid)


@app.put("/pass_bid")
def pass_bid_endpoint(game_id: str = "game1", player_id: str = "farid"):
    """Passing during the bidding"""
    return pass_bid(game_id, player_id)


@app.put("/take_talon")
def take_talon(game_id: str, player_local_id: int, cards: List[tuple[str, str]]):
    """TODO: Write docstring"""
    card_tuples = [(CardNumber(number), CardSuit(suit)) for number, suit in cards]
    return take_talon(game_id, player_local_id, card_tuples)


@app.put("/give_two_cards")
def give_two_cards_endpoint(player: str, card: str):
    """TODO: Write docstring"""
    return give_two_cards(player, card)


@app.put("/make_final_bid")
def make_final_bid_endpoint(game_id: str, player_id: str = "farid", final_bid: int = 120):
    """TODO: Write docstring"""
    return make_final_bid(game_id, player_id, final_bid)


@app.put("/play_card")
def play_card_endpoint(game_id: str, player_id: str, card: str):
    """TODO: Write docstring"""
    return play_card(game_id, player_id, card)


@app.put("/finalize_round")
def finalize_round_endpoint(game_id: str):
    """TODO: Write docstring"""
    return finalize_round(game_id)


@app.get("/game")
def get_game_endpoint(game_id: str = "game1"):
    """TODO: Write docstring"""
    return get_game(game_id)


@app.put("/game")
async def create_game_endpoint(game_id: str, players: List[str]):
    """TODO: Write docstring"""
    return create_game(game_id, players)


if __name__ == "__main__":
    database_init()
    uvicorn.run(app, host="localhost", port=5000)
