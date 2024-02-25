from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from typing import List


class CardSuit(Enum):
    HEART = "♥"  # ♡
    DIAMOND = "♦"  # ♢
    SPADE = "♤"  # ♤
    CLUB = "♧"  # ♧


class CardNumber(Enum):
    NINE = "9"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    TEN = "10"
    ACE = "A"


class CardValue(Enum):
    NINE = 0
    JACK = 2
    QUEEN = 3
    KING = 4
    TEN = 10
    ACE = 11


class GameState(Enum):
    PLAYING = "playing"
    BIDDING = "bidding"
    FINISHED = "finished"

# TODO: We can convert the following classes to dataclasses

class Player(BaseModel):
    id: str
    local_id: int  # 0, 1 or 2
    cards_init: List[str] = [""]
    cards_current: List[str] = [""]
    cards_played: List[str] = [""]
    bolt_count: int = 0
    barrel_count: int = 0


class Game(BaseModel):
    id: str
    players_ids: List[str]
    creation_date: str = str(datetime.now())
    game_state: str = GameState.PLAYING.value
    current_round: int = 0


class Round(BaseModel):
    id: int
    game_id: str = ""
    on_barrel: int = -1  # player id
    activated_pairs: List[str] = []
    bids: List[str] = ["0", "0", "0"]  # 0: new, -1: pass, >100: bid_amount
    last_bid_amount: int = 0
