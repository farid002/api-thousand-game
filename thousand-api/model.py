"""TODO: Write docstring"""

from enum import Enum

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CardSuit(Enum):
    """TODO: Write docstring"""

    HEART = "♥"  # ♡
    DIAMOND = "♦"  # ♢
    SPADE = "♤"  # ♤
    CLUB = "♧"  # ♧


class CardNumber(Enum):
    """TODO: Write docstring"""

    NINE = "9"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    TEN = "10"
    ACE = "A"


class CardValue(Enum):
    """TODO: Write docstring"""

    NINE = 0
    JACK = 2
    QUEEN = 3
    KING = 4
    TEN = 10
    ACE = 11


class GameState(Enum):
    """TODO: Write docstring"""

    CREATED = "created"
    PLAYING = "playing"
    BIDDING = "bidding"
    FINISHED = "finished"


class Player(Base):
    """TODO: Write docstring"""

    __tablename__ = "player"

    id = Column(String, primary_key=True)  # global id, in our case email address
    local_id = Column(Integer)  # 0, 1 or 2
    cards_init = Column(String)
    cards_current = Column(String)
    cards_played = Column(String)
    bolt_count = Column(Integer, default=0)
    barrel_count = Column(Integer, default=0)

    @property
    def cards_init_list(self):
        """Getter: cards_init"""
        return self.cards_init.split(",") if self.cards_init else []

    @cards_init_list.setter
    def cards_init_list(self, value):
        """Getter: cards_init"""
        self.cards_init = ",".join(value) if value else ""

    @property
    def cards_current_list(self):
        """Getter: cards_current"""
        return self.cards_current.split(",") if self.cards_current else []

    @cards_current_list.setter
    def cards_current_list(self, value):
        """Setter: cards_current"""
        self.cards_current = ",".join(value) if value else ""

    @property
    def cards_played_list(self):
        """Getter: cards_played"""
        return self.cards_played.split(",") if self.cards_played else []

    @cards_played_list.setter
    def cards_played_list(self, value):
        """Setter: cards_played"""
        self.cards_played = ",".join(value) if value else ""


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

    player1 = relationship("Player", foreign_keys="Game.player0_id")
    player2 = relationship("Player", foreign_keys="Game.player1_id")
    player3 = relationship("Player", foreign_keys="Game.player2_id")


class Round(Base):
    """TODO: Write docstring"""

    __tablename__ = "round"

    id = Column(String, primary_key=True)
    game_id = Column(String, ForeignKey(Game.id))
    round_number = Column(Integer, default=1)  # can start from 1
    on_barrel = Column(Integer, default=-1)  # player local id
    activated_pair = Column(
        String, default=""
    )  # CardSuit.<suit>.value (i.e.:"♥") or ""
    talon = Column(String, default="")
    bids = Column(
        String, default="0,0,0"
    )  # "p1bid,p2bid,p3bid"; 0: new, -1: pass, >100: bid_amount.i.e.: "100,-1,110"
    last_bid_amount = Column(Integer, default=0)

    game = relationship("Game", foreign_keys="Round.game_id")

    @property
    def talon_list(self):
        """
        Converts comma-separated card strings (i.e.: "9♥,J♤,A♥") value of talon attribute to a list of card strings
        (i.e.: ["9♥", "J♤", "A♥"]), and returns it.

        Usage example
            my_talon_list = round_instance.talon_list

        :return:
            talon: list of card strings (i.e.: ["9♥", "J♤", "A♥"])
        """
        return self.talon.split(",") if self.talon else []

    @talon_list.setter
    def talon_list(self, value):
        """
        Sets talon value. Gets list of card strings (i.e.: ["9♥", "J♤", "A♥"]), converts it to one comma-separated
        string (i.e. "9♥,J♤,A♥") and assigns it to talon attribute of Round class.

        Usage example
            round_instance.talon_list = ["9♥", "J♤", "A♥"]

        Args
            value (list): list of strings (i.e.: ["9♥", "J♤", "A♥"])

        :return:
            None
        """
        self.talon = ",".join(value) if value else ""

    @property
    def bids_list(self):
        """Tbd"""
        return self.bids.split(",") if self.bids else []

    @bids_list.setter
    def bids_list(self, value):
        """Tbd"""
        self.bids = ",".join(value) if value else ""
