"""TODO: Write docstring"""

from sqlalchemy import Boolean, Column, Integer, String

from thousand_api.models.base import Base
from thousand_api.models.card import Pair, PairValue


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
    on_barrel_since = Column(Integer, default=0)
    round_point = Column(Integer, default=0)
    point = Column(Integer, default=0)
    max_biddable_amount = Column(Integer, default=120)
    silent = Column(Boolean, default=False)

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

    def assign_max_biddable_amount(self):
        """Assigns maximum biddable amount value, which will be used as a limit during bidding."""
        if len(self.cards_current) < 7:
            return -1

        self.max_biddable_amount = 120

        if set(Pair.HEART.value) <= set(self.cards_current_list):
            self.max_biddable_amount += PairValue.HEART.value
        if set(Pair.DIAMOND.value) <= set(self.cards_current_list):
            self.max_biddable_amount += PairValue.DIAMOND.value
        if set(Pair.CLUB.value) <= set(self.cards_current_list):
            self.max_biddable_amount += PairValue.CLUB.value
        if set(Pair.SPADE.value) <= set(self.cards_current_list):
            self.max_biddable_amount += PairValue.SPADE.value

        return 0
