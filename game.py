"""TODO: Write docstring"""

import random
import uuid
from datetime import datetime
from typing import List

from database import Session, get_current_round_from_db
from model import *
from model import CardNumber, CardSuit, Game, Player, Round


def create_game(game_id: str, players_ids: List[str]):
    """TODO: Write docstring"""
    session = Session()

    game = Game(
        id=game_id,
        player1_id=players_ids[0],
        player2_id=players_ids[1],
        player3_id=players_ids[2],
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
    game.game_state = GameState.CREATED.value
    game.current_round = game.current_round + 1
    session.add(game)

    players = (
        session.query(Player)
        .filter(Player.id.in_([game.player1_id, game.player2_id, game.player3_id]))
        .all()
    )
    players, talon = deal_cards(players)

    for player in players:
        session.add(player)
    session.commit()

    round_obj = Round(
        id=str(uuid.uuid4()), round_number=game.current_round, game_id=game_id
    )
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

    talon = deck[-3:]

    return players, talon


def make_bid(game_id: str, player_local_id: str, bid: str):
    """TODO: Write docstring"""
    session = Session()

    curr_round = get_current_round_from_db(session, game_id)
    if not curr_round:
        session.close()
        return "Round not found"

    if int(bid) <= int(curr_round.bids[(int(player_local_id) + 1) % 3]) or int(
        bid
    ) <= int(curr_round.bids[(int(player_local_id) + 2) % 3]):
        session.close()
        return "Less than biddable amount"

    curr_round.bids[int(player_local_id)] = bid
    session.add(curr_round)
    session.commit()
    session.close()

    return "Bid made successfully"


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
