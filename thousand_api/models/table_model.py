"""Table class to keep created tables, it must not be confused with game table! Table might not lead to a game"""

from enum import Enum

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from thousand_api.models.base_model import Base
from thousand_api.models.player_model import Player


class TableState(Enum):
    """TODO: Write docstring"""

    CREATED = "created"
    GAME_STARTED = "game_started"
    CANCELLED = "cancelled"


class Table(Base):
    """TODO: Write docstring"""

    __tablename__ = "table"

    id = Column(String, primary_key=True)
    player0_id = Column(String, ForeignKey(Player.id))
    player1_id = Column(String, ForeignKey(Player.id))
    player2_id = Column(String, ForeignKey(Player.id))
    creation_date = Column(String)
    table_state = Column(String, default=TableState.CREATED.value)

    entry_coins = Column(Integer, default=0)
    reliable = Column(Boolean, default=False)
    ace_marriage = Column(Boolean, default=False)
    game_speed = Column(Integer, default=0)  # in minutes per round
    password = Column(Integer, default=0)
    till_1001 = Column(Boolean, default=False)

    player0 = relationship("Player", foreign_keys="Table.player0_id")
    player1 = relationship("Player", foreign_keys="Table.player1_id")
    player2 = relationship("Player", foreign_keys="Table.player2_id")
