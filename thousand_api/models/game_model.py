"""TODO: Write docstring"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String

from thousand_api.models.table_model import Table


class GameState(Enum):
    """TODO: Write docstring"""

    CREATED = "created"
    PLAYING = "playing"
    BIDDING = "bidding"
    TALON = "talon"
    REBIDDING = "rebidding"
    ROUND_FINISHED = "round_finished"
    FINISHED = "finished"


class Game(Table):
    """TODO: Write docstring"""

    __tablename__ = "game"

    id = Column(String, ForeignKey("table.id"), primary_key=True)
    creation_date = Column(String)
    game_state = Column(String, default=GameState.CREATED.value)
    current_round = Column(Integer, default=0)
