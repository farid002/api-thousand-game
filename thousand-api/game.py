"""TODO: Write docstring"""

import random
import uuid
from datetime import datetime
from typing import List

from database import (
    Session,
    get_current_round_from_db,
    get_player_from_db,
    get_players_with_game_from_db,
)
from model import *
from model import CardNumber, CardSuit, Game, Player, Round


def create_game(game_id: str, players_ids: List[str]):
    """TODO: Write docstring"""
    session = Session()

    game = Game(
        id=game_id,
        player0_id=players_ids[0],
        player1_id=players_ids[1],
        player2_id=players_ids[2],
        creation_date=str(datetime.now()),
    )

    session.add(game)
    session.commit()

    players = [
        Player(id=players_ids[0], local_id=0),
        Player(id=players_ids[1], local_id=1),
        Player(id=players_ids[2], local_id=2),
    ]

    for player in players:
        session.merge(player)
    session.commit()

    session.close()

    return players_ids


def get_game(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    session.close()

    if game:
        return game
    else:
        return None


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

    round_obj = Round(id=str(uuid.uuid4()), round_number=game.current_round, game_id=game_id)
    bid_list = ["0", "0", "0"]
    bid_list[(game.current_round + 1) % 3] = "100"  # player before bid_starter should have bid of 100

    round_obj.bids_list = bid_list
    round_obj.bid_starter = (game.current_round + 2) % 3
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


def take_three_cards(player, card):
    """TODO: Write docstring"""
    return


def give_two_cards(player, card):
    """TODO: Write docstring"""
    return


def make_last_bid(player, last_bid):
    """TODO: Write docstring"""
    return


def play_card(player, card):
    """TODO: Write docstring"""
    return


def finalize_round(player, card):
    """TODO: Write docstring"""
    return
