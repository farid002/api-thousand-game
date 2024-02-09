# main.py
from enum import Enum
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any
import uuid
import sqlite3
from datetime import datetime

app = FastAPI()


class GameState(Enum):
    PLAYING = "playing"
    FINISHED = "finished"


class Player(BaseModel):
    id: int  # 0, 1 or 2
    hand_init: List[str]
    hand_current: List[str]
    bolt_count: int = 0
    barrel_count: int = 0


class Game(BaseModel):
    id: str
    players: List[str]
    creation_date: str
    game_state: str
    current_round: int


class Round(BaseModel):
    id: int = 0
    game_id: str = ""
    on_barrel: int = -1  # player id
    activated_pairs: List[str] = []
    bids: List[str] = ["0", "0", "0"]  # 0: new, -1: pass, >100: bid_amount
    last_bid_amount: int = 0

    def __init__(self, id, game_id, on_barrel, activated_pairs, bids, last_bid_amount):
        super().__init__()
        self.id = id
        self.game_id = game_id
        self.on_barrel = on_barrel
        self.activated_pairs = activated_pairs
        self.bids = bids
        self.last_bid_amount = last_bid_amount


def create_game_table():
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (id TEXT PRIMARY KEY,
                 players TEXT,
                 creation_date TEXT,
                 game_state TEXT,
                 current_round INTEGER)''')
    conn.commit()
    conn.close()


@app.get("/start_round")
async def start_round(game_id: str):
    game: Game = await get_game(game_id)
    game_round = Round(
        id=str(game.current_round),
        game_id=game_id,
        on_barrel=-1,
        activated_pairs=[],
        bids=["0", "0", "0"],
        last_bid_amount=0
    )

    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS rounds
                     (id INTEGER PRIMARY KEY,
                     game_id TEXT,
                     on_barrel INTEGER,
                     activated_pairs TEXT,
                     bids TEXT
                     last_bid_amount INTEGER)''')
    conn.commit()
    conn.close()

    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("INSERT INTO rounds (id, game_id, on_barrel, activated_pairs, bids, last_bid_amount) VALUES "
              "(?, ?, ?, ?, ?, ?)", (game_round.id, game_round.game_id, game_round.on_barrel,
                                     ",".join(game_round.activated_pairs),
                                     ",".join(game_round.bids), game_round.last_bid_amount))
    conn.commit()
    conn.close()
    return


def make_bid(player: str, last_bid: int):
    return


def take_3_cards(player: str, card: str):
    return


def give_2_cards(player: str, card: str):
    return


def make_last_bid(player: str, last_bid: int):
    return


def play_card(player: str, card: str):
    return


def finalize_round(player: str, card: str):
    return


def create_game(game_id: str, players: List[str]):
    game = Game
    game.id = game_id  # str(uuid.uuid4())  # Generate UUID for the game
    game.players = players
    game.creation_date = str(datetime.now())
    game.game_state = GameState.PLAYING.value
    game.current_round = 0

    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("INSERT INTO games (id, players, creation_date, game_state, current_round) VALUES (?, ?, ?, ?, ?)",
              (game.id, ",".join(game.players), game.creation_date, game.game_state, game.current_round))
    conn.commit()
    conn.close()


@app.get("/game")
async def get_game(game_id: str):
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("SELECT * FROM games WHERE id=?", (game_id,))
    game_data = c.fetchone()
    conn.close()
    if game_data:
        return Game(id=game_data[0], players=game_data[1].split(','), creation_date=game_data[2],
                    game_state=game_data[3], current_round=game_data[4])
    else:
        return None


@app.put("/games")
async def create_game_endpoint(game_id: str, players: List[str]):
    create_game(game_id, players)
    return players


if __name__ == "__main__":
    create_game_table()

    uvicorn.run(app, host="localhost", port=5000)
