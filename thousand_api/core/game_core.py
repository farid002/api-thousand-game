"""TODO: Write docstring"""

import random
import uuid
from datetime import datetime
from typing import List

from thousand_api.db.database import (
    Session,
    get_current_round_from_db,
    get_player_from_db,
    get_players_with_game_from_db,
)
from thousand_api.models.card import (
    CARD_VALUES,
    SUIT_MAPPING,
    CardNumber,
    CardSuit,
    PairValue,
)
from thousand_api.models.game import Game, GameState
from thousand_api.models.player import Player
from thousand_api.models.round import Round
from thousand_api.utils.helper import find_trick_winner


def create_game(players_ids: List[str]):
    """TODO: Write docstring"""
    session = Session()
    game_id = str(uuid.uuid4())

    players = [
        Player(id=players_ids[0], local_id=0),
        Player(id=players_ids[1], local_id=1),
        Player(id=players_ids[2], local_id=2),
    ]

    game = Game(
        id=game_id,
        player0_id=players_ids[0],
        player1_id=players_ids[1],
        player2_id=players_ids[2],
        creation_date=str(datetime.now()),
        player0=players[0],
        player1=players[1],
        player2=players[2],
    )

    session.add(game)
    session.commit()

    session.close()

    return game_id


def start_round(game_id: str):
    """TODO: Write docstring"""
    session = Session()

    game = session.query(Game).filter_by(id=game_id).first()
    if not game:
        session.close()
        return "Game not found"
    game.game_state = GameState.BIDDING.value
    game.current_round = game.current_round + 1
    session.add(game)

    players = session.query(Player).filter(Player.id.in_([game.player0_id, game.player1_id, game.player2_id])).all()
    players, talon = deal_cards(players)

    for player in players:
        session.add(player)
    session.commit()

    bid_list = ["0", "0", "0"]
    bid_list[(game.current_round + 1) % 3] = "100"  # player before bid_starter should have bid of 100

    round_obj = Round(
        id=str(uuid.uuid4()),
        round_number=game.current_round,
        game_id=game_id,
        bid_starter=(game.current_round + 2) % 3,
        bid_winner=-1,
    )
    round_obj.bids_list = bid_list
    round_obj.talon_list = talon

    session.add(round_obj)
    session.commit()

    session.close()

    return "Round started successfully"


def deal_cards(players: List[Player]):
    """TODO: Write docstring"""
    deck = []

    for suit in CardSuit:
        for number in CardNumber:
            deck.append(number.value + suit.value)

    random.shuffle(deck)

    for i, player in enumerate(players):
        player.cards_init_list = deck[7 * i : 7 * (i + 1)]
        player.cards_current_list = deck[7 * i : 7 * (i + 1)]
        player.cards_played_list = []

    for i, card in enumerate(deck[:-3]):
        player_index = i % 3
        players[player_index].cards_init_list.append(deck[i])
        players[player_index].cards_current_list.append(deck[i])

    for player in players:
        player.assign_max_biddable_amount()

    talon = deck[-3:]

    return players, talon


def make_bid(game_id: str, player_id: str, bid: int):
    """Bidding function"""
    session = Session()

    game = session.query(Game).filter_by(id=game_id).first()

    if game.game_state != GameState.BIDDING.value:
        session.close()
        return "Not in bidding game state"

    curr_round_obj = get_current_round_from_db(session, game_id)
    players = get_players_with_game_from_db(session, game)

    if not curr_round_obj or len(players) != 3:
        session.close()
        return "Round or player not found"

    player_local_id = next((index for index, player in enumerate(players) if player.id == player_id), None)

    if curr_round_obj.bids_list[player_local_id] == "-1":
        session.close()
        return "The player already passed bidding"

    next_player_bid = int(curr_round_obj.bids_list[(player_local_id + 1) % 3])
    prev_player_bid = int(curr_round_obj.bids_list[(player_local_id + 2) % 3])

    if bid <= next_player_bid or bid <= prev_player_bid:
        session.close()
        return "Less than other players' bids"

    if bid > players[player_local_id].max_biddable_amount:
        session.close()
        return "More than maximum biddable amount"

    temp_bids_list = curr_round_obj.bids_list
    temp_bids_list[player_local_id] = str(bid)

    next_player = players[(player_local_id + 1) % 3]
    prev_player = players[(player_local_id + 2) % 3]

    if bid >= next_player.max_biddable_amount:
        temp_bids_list[(player_local_id + 1) % 3] = "-1"

    if bid >= prev_player.max_biddable_amount:
        temp_bids_list[(player_local_id + 2) % 3] = "-1"

    curr_round_obj.bids_list = temp_bids_list
    curr_round_obj.final_bid_amount = bid

    if temp_bids_list.count("-1") >= 2:
        game.game_state = GameState.TALON.value
        curr_round_obj.bid_winner = next((index for index, value in enumerate(temp_bids_list) if value != "-1"), None)

    session.add(curr_round_obj)
    session.commit()
    session.close()

    return "Bid made successfully"


def pass_bid(game_id: str, player_id: str):
    """Passing function during bidding"""
    session = Session()

    game = session.query(Game).filter_by(id=game_id).first()
    curr_round_obj = get_current_round_from_db(session, game_id)
    bidding_player = get_player_from_db(session, player_id)

    if not curr_round_obj or not bidding_player:
        session.close()
        return "Round or player not found"

    player_local_id = bidding_player.local_id

    temp_bids_list = curr_round_obj.bids_list
    temp_bids_list[player_local_id] = str(-1)  # -1 for pass
    curr_round_obj.bids_list = temp_bids_list

    if temp_bids_list.count("-1") >= 2:
        game.game_state = GameState.TALON.value
        curr_round_obj.bid_winner = next((index for index, value in enumerate(temp_bids_list) if value != "-1"), None)

    session.add(curr_round_obj)
    session.commit()
    session.close()

    return "Passed bidding successfully"


def take_talon(game_id: str, player_id: str) -> str:
    """
    Allows a player to take talon in their turn.

    Args:
        game_id (str): The ID of the game.
        player_id (str): The Global ID of the player (eg: jane.doe@example.com).

    Returns:
        str: A success message if the operation is successful, an error message otherwise.
    """
    session = Session()
    curr_round_obj = get_current_round_from_db(session, game_id)
    if not curr_round_obj:
        session.close()
        return "Round not found"

    cards = curr_round_obj.talon.split(",")
    if len(cards) != 3:
        session.close()
        return "Talon doesn't have 3 cards"

    player = get_player_from_db(session, player_id)
    if not player:
        session.close()
        return "Player not found"

    # add the card to player's hand
    player.cards_current_list = player.cards_current_list + cards

    session.add(curr_round_obj)
    session.add(player)
    session.commit()
    session.close()

    # TODO: we need return class for all responses, e.g. Response(code=200, message="Cards taken successfully")
    return "Cards taken successfully"


def give_two_cards(game_id: str, player_id: str, card1: str, card2: str):
    """Gives first card to next player, second card to previous player

    Args:
        game_id(str): Game ID
        player_id(str): Global ID of current player
        card1 (str): 1st card to be given
        card2 (str): 2nd card to be given
    """
    session = Session()
    curr_round_obj = get_current_round_from_db(session, game_id)

    game = session.query(Game).filter_by(id=game_id).first()
    players = get_players_with_game_from_db(session, game)  # [ 0 1 2 ]
    curr_player = get_player_from_db(session, player_id)
    curr_player_local_id = curr_player.local_id

    # check whether cards are in player's hand
    curr_player_cards_temp = curr_player.cards_current_list
    if card1 not in curr_player_cards_temp or card2 not in curr_player_cards_temp:
        session.close()
        return "Cards not in player's hand"

    if len(curr_player_cards_temp) != 10:
        session.close()
        return "Player doesn't have 10 cards to give 2 of them"

    # remove cards from current player
    curr_player_cards_temp.remove(card1)
    curr_player_cards_temp.remove(card2)
    curr_player.cards_current_list = curr_player_cards_temp

    # give card1 to next player
    next_player_local_id = int((curr_player_local_id + 1) % 3)
    next_player = players[next_player_local_id]
    next_player.cards_current_list += [card1]

    # give card2 to previous player
    prev_player_local_id = int((curr_player_local_id + 2) % 3)
    prev_player = players[prev_player_local_id]
    prev_player.cards_current_list += [card2]

    session.add(curr_round_obj)
    session.add(next_player)
    session.add(prev_player)
    session.commit()
    session.close()

    return "Cards given successfuly"


def make_final_bid(game_id: str, player_id: str, final_bid: int):
    """TODO: Write docstring"""
    session = Session()
    player = get_player_from_db(session, player_id)
    curr_round_obj = get_current_round_from_db(session, game_id)
    game = session.query(Game).filter_by(id=game_id).first()

    if final_bid < curr_round_obj.final_bid_amount:
        return "ERROR: final bid can not be less than max bid amount during bidding"
    if curr_round_obj.bids_list[player.local_id] == "-1":
        return "ERROR: player can't make final bid while, he already passed"
    if final_bid > player.max_biddable_amount:
        return "ERROR: can't bid, more than max biddable amount"

    curr_round_obj.final_bid_amount = final_bid
    curr_round_obj.trick_turn = player.local_id
    temp_bids = curr_round_obj.bids_list
    temp_bids[player.local_id] = str(final_bid)
    curr_round_obj.bids_list = temp_bids

    game.game_state = GameState.PLAYING.value

    session.add(curr_round_obj)
    session.commit()
    session.close()

    return


def play_card(game_id: str, player_id: str, card: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    player = get_player_from_db(session, player_id)
    players = get_players_with_game_from_db(session, game)
    round_obj = get_current_round_from_db(session, game_id)
    trick = round_obj.trick_list

    if round_obj.trick_list[player.local_id] != "0" or round_obj.trick_turn != player.local_id:
        return "ERROR: player has already played card or not his/her turn"

    if card not in player.cards_current_list:
        return "ERROR: player does not have such card"

    # handle pair registration
    if trick == ["0", "0", "0"] and len(player.cards_played_list) > 0:
        if (
            card[0] == "K"
            and f"Q{card[-1]}" in player.cards_current_list
            or card[0] == "Q"
            and f"K{card[-1]}" in player.cards_current_list
        ):
            round_obj.activated_pair = card[-1]
            player.round_point += PairValue[SUIT_MAPPING.get(card[-1])].value

    trick[player.local_id] = card
    temp_cards_played = player.cards_played_list
    temp_cards_played.append(card)
    player.cards_played_list = temp_cards_played
    temp_cards_curr = player.cards_current_list
    temp_cards_curr.remove(card)
    player.cards_current_list = temp_cards_curr

    if "0" not in trick:
        # trick finished, assign points, and assign trick values to 0, also check if it was the last trick
        trick_value = CARD_VALUES[trick[0][:-1]] + CARD_VALUES[trick[1][:-1]] + CARD_VALUES[trick[2][:-1]]
        trick_winner_id = find_trick_winner(trick, (player.local_id + 1) % 3, round_obj.activated_pair)
        round_obj.trick_turn = trick_winner_id
        players[trick_winner_id].round_point += trick_value
        round_obj.trick_turn = trick_winner_id
        round_obj.trick_list = ["0", "0", "0"]

        if not player.cards_current:  # round finished
            finalize_round(game_id)
            game.game_state = GameState.ROUND_FINISHED.value
            session.add(round_obj)
            session.commit()
            session.close()
            return "Round finished"
    else:
        round_obj.trick_list = trick
        round_obj.trick_turn = (player.local_id + 1) % 3

    session.add(round_obj)
    session.commit()
    session.close()

    return "SUCCESS"


def finalize_round(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    if game is None:
        return "ERROR: Game not found"

    round_obj = get_current_round_from_db(session, game_id)
    players = get_players_with_game_from_db(session, game)

    # bid winner wins the round
    if players[round_obj.bid_winner].round_point >= round_obj.final_bid_amount:

        if (
            players[round_obj.bid_winner].point
            < 880
            <= players[round_obj.bid_winner].point + round_obj.final_bid_amount
        ):
            players[round_obj.bid_winner].point = 880
            players[round_obj.bid_winner].on_barrel_since += 1
            round_obj.on_barrel = round_obj.bid_winner

        elif (
            players[round_obj.bid_winner].point == 880
            and players[round_obj.bid_winner].point + round_obj.final_bid_amount < 1000
        ):
            players[round_obj.bid_winner].on_barrel_since += 1

        else:
            players[round_obj.bid_winner].point += round_obj.final_bid_amount

        # wins whole game
        if players[round_obj.bid_winner].point >= 1000:
            finalize_game(game_id)

    # bid winner loses
    else:

        # if point was 880, fell from barrel
        if players[round_obj.bid_winner].point == 880:
            players[round_obj.bid_winner].barrel_count += 1
            players[round_obj.bid_winner].on_barrel_since = 0
            round_obj.on_barrel = -1

        # if barrel count is 3, reset the point
        if players[round_obj.bid_winner].barrel_count == 3:
            players[round_obj.bid_winner].barrel_count = 0
            players[round_obj.bid_winner].on_barrel_since = 0
            players[round_obj.bid_winner].point = 0
            players[round_obj.bid_winner].bolt_count = 0

        else:
            players[round_obj.bid_winner].point -= round_obj.final_bid_amount

    for player in players:
        # assign bolts and decrease by 120 if bolt_count is 3
        if player.round_point == 0:
            player.bolt_count += 1
            if player.bolt_count == 3:
                player.point -= 120
                player.bolt_count = 0
        elif player.local_id != round_obj.bid_winner:
            player.point += round(player.round_point, -1)  # assign won points except bid winner

        # silence assignment
        player.silent = True if player.point <= -240 else False

    for player in players:
        session.merge(player)

    session.add(round_obj)
    session.commit()
    session.close()
    return


def finalize_game(game_id: str):
    """TODO: Write docstring"""
    pass
