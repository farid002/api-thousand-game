"""TODO: Write docstring"""

from enum import Enum

CARD_VALUES = {"9": 0, "J": 2, "Q": 3, "K": 4, "10": 10, "A": 11}
SUIT_MAPPING = {"♥": "HEART", "♦": "DIAMOND", "♧": "CLUB", "♤": "SPADE"}


class CardSuit(Enum):
    """Suit of the card"""

    HEART = "♥"  # ♡
    DIAMOND = "♦"  # ♢
    CLUB = "♧"  # ♧
    SPADE = "♤"  # ♤


class CardNumber(Enum):
    """Number of the card"""

    NINE = "9"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    TEN = "10"
    ACE = "A"


class Pair(Enum):
    """Card Pairs"""

    HEART = ["K♥", "Q♥"]
    DIAMOND = ["K♦", "Q♦"]
    CLUB = ["K♧", "Q♧"]
    SPADE = ["K♤", "Q♤"]


class PairValue(Enum):
    """Each Pair has a value during 'melden' or used for max. biddable amount calculation"""

    HEART = 100
    DIAMOND = 80
    CLUB = 60
    SPADE = 40
