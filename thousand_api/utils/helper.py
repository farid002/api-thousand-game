"""Python module to store helper and utility functions"""

from thousand_api.models.model import CARD_VALUES


def is_card_bigger(first_card, second_card, activated_pair):
    """Check if first card bigger than second card"""
    if first_card[-1] == second_card[-1]:  # they have same suit
        if CARD_VALUES[first_card[:-1]] > CARD_VALUES[second_card[:-1]]:
            return True
        else:
            return False
    elif second_card[-1] == activated_pair:
        return False
    else:
        return True


def find_trick_winner(trick, player_local_id, activated_pair):
    """Find the trick winner. REMARK: player_local_id is the one who put the card first (so can be player 2)"""
    next_player_local_id = (player_local_id + 1) % 3
    prev_player_local_id = (player_local_id + 2) % 3

    player_card_suit = trick[player_local_id][-1]
    next_player_card_value = CARD_VALUES[trick[next_player_local_id][:-1]]
    next_player_card_suit = trick[next_player_local_id][-1]
    prev_player_card_value = CARD_VALUES[trick[prev_player_local_id][:-1]]
    prev_player_card_suit = trick[prev_player_local_id][-1]

    if is_card_bigger(trick[player_local_id], trick[next_player_local_id], activated_pair) and is_card_bigger(
        trick[player_local_id], trick[prev_player_local_id], activated_pair
    ):
        return player_local_id

    elif next_player_card_suit == player_card_suit:
        if prev_player_card_suit != activated_pair:
            if prev_player_card_suit != player_card_suit:
                return next_player_local_id
            elif next_player_card_value > prev_player_card_value:
                return next_player_local_id
            else:
                return prev_player_local_id
        elif next_player_card_suit == activated_pair:
            if next_player_card_value > prev_player_card_value:
                return next_player_local_id
            else:
                return prev_player_local_id
        else:
            return prev_player_local_id

    elif next_player_card_suit == activated_pair:
        if prev_player_card_suit != activated_pair:
            return next_player_local_id
        elif next_player_card_value > prev_player_card_value:
            return next_player_local_id
        else:
            return prev_player_local_id

    elif prev_player_card_suit == player_card_suit or prev_player_card_suit == activated_pair:
        return prev_player_local_id

    else:
        return -1
