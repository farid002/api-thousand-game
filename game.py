from datetime import datetime
from model import *
import sqlite3
from database import *
import uuid
import random


def create_game(game_id: str, players_ids: List[str]):
    game = Game(id=game_id, players_ids=players_ids)  # str(uuid.uuid4())  # Generate UUID for the game
    players = [Player(id=game.players_ids[0], local_id=0),
               Player(id=game.players_ids[1], local_id=1),
               Player(id=game.players_ids[2], local_id=2)]

    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("INSERT INTO game (id, players_ids, creation_date, game_state, current_round) VALUES (?, ?, ?, ?, ?)",
              (game.id, ",".join(game.players_ids), game.creation_date, game.game_state, game.current_round))
    update_players_db(c, players)
    conn.commit()
    conn.close()

    return players_ids


def get_game(game_id: str):
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("SELECT * FROM game WHERE id=?", (game_id,))
    game_data = c.fetchone()
    conn.close()
    if game_data:
        return Game(id=game_data[0], players_ids=game_data[1].split(','), creation_date=game_data[2],
                    game_state=game_data[3], current_round=game_data[4])
    else:
        return None


def start_round(game_id: str):
    game: Game = get_game(game_id)
    game_round = Round(id=str(game.current_round + 1), game_id=game_id)

    players = [get_player_from_db(game.players_ids[0]),
               get_player_from_db(game.players_ids[1]),
               get_player_from_db(game.players_ids[2])]

    players, talon = deal_cards(players)

    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("UPDATE game SET current_round = ? WHERE id = ?", (game.current_round + 1, game_id))
    c.execute("INSERT INTO round (id, game_id, on_barrel, activated_pairs, bids, last_bid_amount) "
              "VALUES (?, ?, ?, ?, ?, ?)", (game_round.id, game_round.game_id, game_round.on_barrel,
                                            ",".join(game_round.activated_pairs),
                                            ",".join(game_round.bids), game_round.last_bid_amount))
    update_players_db(c, players)
    conn.commit()
    conn.close()

    return "Successful"


def deal_cards(players: List[Player]):
    deck = []

    for suit in CardSuit:
        for number in CardNumber:
            deck.append(number.value + suit.value)

    random.shuffle(deck)

    # TODO: it was in the Dart code - decide if important
    # gameState = GameState.BIDDING
    for player in players:
        player.cards_init = []
        player.cards_played = []
        player.cards_current = []

    for i, card in enumerate(deck[:-3]):
        player_index = i % 3
        players[player_index].cards_init.append(deck[i])
        players[player_index].cards_current.append(deck[i])

    talon = deck[-3:]

    return players, talon


def make_bid(player, bid):
    return


def take_three_cards(player, card):
    return


def give_two_cards(player, card):
    return


def make_last_bid(player, last_bid):
    return


def play_card(player, card):
    return


def finalize_round(player, card):
    return
