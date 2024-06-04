"""TODO: Write docstring"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from thousand_api.models.base import Base
from thousand_api.models.player import Player


class GameState(Enum):
    """TODO: Write docstring"""

    CREATED = "created"
    PLAYING = "playing"
    BIDDING = "bidding"
    TALON = "talon"
    REBIDDING = "rebidding"
    ROUND_FINISHED = "round_finished"
    FINISHED = "finished"


class Game(Base):
    """TODO: Write docstring"""

    __tablename__ = "game"

    id = Column(String, primary_key=True)
    player0_id = Column(String, ForeignKey(Player.id))
    player1_id = Column(String, ForeignKey(Player.id))
    player2_id = Column(String, ForeignKey(Player.id))
    creation_date = Column(String)
    game_state = Column(String, default=GameState.CREATED.value)
    current_round = Column(Integer, default=0)

    player0 = relationship("Player", foreign_keys="Game.player0_id")
    player1 = relationship("Player", foreign_keys="Game.player1_id")
    player2 = relationship("Player", foreign_keys="Game.player2_id")
