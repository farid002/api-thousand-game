import sqlite3
from model import *

# TODO: use SQL Alchemy or SQLModel to handle the database operations

def create_game_table():
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS game
                 (id TEXT PRIMARY KEY,
                 players_ids TEXT,
                 creation_date TEXT,
                 game_state TEXT,
                 current_round INTEGER)''')
    conn.commit()
    conn.close()


def create_player_table():
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS player
                 (id TEXT PRIMARY KEY,
                 local_id TEXT,
                 cards_init TEXT,
                 cards_current TEXT,
                 cards_played TEXT,
                 bolt_count TEXT,
                 barrel_count INTEGER)''')
    conn.commit()
    conn.close()


def create_round_table():
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS round
                 (id INTEGER PRIMARY KEY,
                 game_id TEXT,
                 on_barrel INTEGER,
                 activated_pairs TEXT,
                 bids TEXT,
                 last_bid_amount INTEGER,
                 FOREIGN KEY(game_id) REFERENCES game(id))''')
    conn.commit()
    conn.close()


def database_init():
    create_game_table()
    create_round_table()
    create_player_table()


def update_players_db(c, players):
    for i in range(0, len(players)):
        c.execute("INSERT OR REPLACE INTO player (id, local_id, cards_init, cards_current, cards_played, bolt_count, "
                  "barrel_count) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (players[i].id,
                   players[i].local_id,
                   ",".join(players[i].cards_init),
                   ",".join(players[i].cards_current),
                   ",".join(players[i].cards_played),
                   players[i].bolt_count,
                   players[i].barrel_count))


def get_player_from_db(player_id: str):
    conn = sqlite3.connect("games.db")
    c = conn.cursor()
    c.execute("SELECT * FROM player WHERE id = ?", player_id)
    player_data = c.fetchone()
    conn.close()

    if player_data:
        player_instance = Player(id=player_data[0],
                                 local_id=int(player_data[1]),
                                 cards_init=player_data[2].split(','),
                                 cards_current=player_data[3].split(','),
                                 cards_played=player_data[4].split(','),
                                 bolt_count=int(player_data[5]),
                                 barrel_count=int(player_data[6]))
        return player_instance
    else:
        return None
