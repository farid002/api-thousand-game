"""TODO: Write docstring"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from thousand_api.models.base_model import Base
from thousand_api.models.game_model import Game


class Round(Base):
    """TODO: Write docstring"""

    __tablename__ = "round"

    id = Column(String, primary_key=True)
    game_id = Column(String, ForeignKey(Game.id))
    round_number = Column(Integer, default=1)  # can start from 1
    on_barrel = Column(Integer, default=-1)  # player local id
    activated_pair = Column(String, default="")  # CardSuit.<suit>.value (i.e.:"♥") or ""
    talon = Column(String, default="")
    bid_starter = Column(Integer, default=0)  # player local id
    bids = Column(String, default="0,0,0")  # "p1bid,p2bid,p3bid"; 0: new, -1: pass, >100: bid_amount.i.e.: "100,-1,110"
    bid_winner = Column(Integer, default=-1)  # player local id
    final_bid_amount = Column(Integer, default=100)
    trick = Column(String, default="0,0,0")
    trick_turn = Column(Integer, default=-1)

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

    @property
    def trick_list(self):
        """Tbd"""
        return self.trick.split(",") if self.trick else []

    @trick_list.setter
    def trick_list(self, value):
        """Tbd"""
        self.trick = ",".join(value) if value else ""
