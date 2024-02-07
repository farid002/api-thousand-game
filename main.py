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


class Game(BaseModel):
    id: Optional[str]
    players: List[str]
    creation_date: str = datetime.now()
    game_state: str = GameState.PLAYING
    current_round: int = 0


class Round(BaseModel):
    id: int
    game_id: str
    p1_hand_init: List[str]
    p2_hand_init: List[str]
    p3_hand_init: List[str]
    p1_hand_current: List[str]
    p2_hand_current: List[str]
    p3_hand_current: List[str]
    p1_bolt_count: int = 0
    p2_bolt_count: int = 0
    p3_bolt_count: int = 0
    p1_barrel_count: int = 0
    p2_barrel_count: int = 0
    p3_barrel_count: int = 0
    on_barrel: str = ""
    activated_pairs: List[str] = []
    bids: List[List[int]] = [[0, 0, 0]]  # 0: new, -1: pass, >100: bid_amount
    last_bid_amount: int = 0

    def __init__(self, id, game_id, p1_hand, p2_hand, p3_hand):
        super().__init__()
        self.id = id
        self.game_id = game_id
        self.p1_hand_init = self.p1_hand_current = p1_hand
        self.p2_hand_init = self.p2_hand_current = p2_hand
        self.p3_hand_init = self.p3_hand_current = p3_hand


def create_game_table():
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS games
                 (id TEXT PRIMARY KEY,
                 players TEXT,
                 creation_date TEXT,
                 game_state TEXT)''')
    conn.commit()
    conn.close()


def create_game(game: Game):
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    game.id = str(uuid.uuid4())  # Generate UUID for the game
    c.execute("INSERT INTO games (id, players, creation_date, game_state) VALUES (?, ?, ?, ?)",
              (game.id, ",".join(game.players), game.creation_date, game.game_state))
    conn.commit()
    conn.close()


@app.put("/games/")
async def create_game_endpoint(game: Game):
    create_game(game)
    return game


if __name__ == "__main__":
    create_game_table()

    uvicorn.run(app, host="localhost", port=5000)
