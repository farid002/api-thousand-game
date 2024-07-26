"""TODO: Write docstring"""

import uuid
from datetime import datetime

from thousand_api.db.database import Session
from thousand_api.models.player_model import Player
from thousand_api.models.table_model import Table, TableState


def create_table(
    creator_player_id: str,
    entry_coins: int,
    reliable: bool,
    ace_marriage: bool,
    game_speed: int,
    password: int,
    till_1001: bool,
):
    """TODO: Write docstring"""
    session = Session()
    player = session.query(Player).filter_by(id=creator_player_id).first()

    if player is None:
        return "Player could not be found"
    if player.coins < entry_coins:
        return "Player does not have enough coins"

    table_id = str(uuid.uuid4())
    table = Table(
        id=table_id,
        player0_id=creator_player_id,
        creation_date=str(datetime.now()),
        table_state=TableState.CREATED.value,
        entry_coins=entry_coins,
        reliable=reliable,
        ace_marriage=ace_marriage,
        game_speed=game_speed,
        password=password,
        till_1001=till_1001,
    )

    player = session.query(Player).filter_by(id=creator_player_id).first()
    player.local_id = 0

    session.add(player)
    session.add(table)
    session.commit()
    session.close()

    return table_id


def get_table(table_id: str):
    """TODO: Write docstring"""
    session = Session()
    table = session.query(Table).filter_by(id=table_id).first()
    session.close()

    if table:
        return table
    else:
        return None


def delete_table(table_id):
    """
    Delete a table from the database by its ID.

    Args:
        table_id (int): The ID of the game to delete.

    Returns:
        bool: True if the game was deleted successfully, False otherwise.
    """
    session = Session()
    try:
        table = session.query(Table).filter_by(id=table_id).first()
        if table:
            session.delete(table)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting table: {e}")
        return False
    finally:
        session.close()


def update_table(table_id, player0_id, player1_id, player2_id):
    """
    Update a table in the database.

    Args:
        table_id (int): The ID of the game to update.
        player0_id (int): ID of player 1.
        player1_id (int): ID of player 2.
        player2_id (int): ID of player 3.

    Returns:
        bool: True if the table was updated successfully, False otherwise.
    """
    session = Session()
    try:
        table = session.query(Table).filter_by(id=table_id).first()
        if table:
            table.player0_id = player0_id
            table.player1_id = player1_id
            table.player2_id = player2_id
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error updating table: {e}")
        return False
    finally:
        session.close()


def get_tables():
    """TODO: Write docstring"""
    session = Session()
    tables = session.query(Table).all()
    session.close()

    if tables:
        return tables
    else:
        return None


def get_players(table_id: str):
    """TODO: Write docstring"""
    session = Session()
    table = session.query(Table).filter_by(id=table_id).first()

    if table:
        players = [table.player0, table.player1, table.player2]
        session.close()
        return players
    else:
        session.close()
        return None


def add_player(table_id: str, player_id: str):
    """TODO: Write docstring"""
    session = Session()
    table = session.query(Table).filter_by(id=table_id).first()
    player = session.query(Player).filter_by(id=player_id).first()

    if player.local_id != -1:
        return "Player is already in a game"

    if player.coins < table.entry_coins:
        return "Player does not have enough coins"

    if table:
        if table.player0_id == "" or table.player0_id is None:
            table.player0_id = player_id
            player.local_id = 0
        elif table.player1_id == "" or table.player1_id is None:
            table.player1_id = player_id
            player.local_id = 1
        elif table.player2_id == "" or table.player2_id is None:
            table.player2_id = player_id
            player.local_id = 2
        else:
            session.close()
            return "No place"
        session.add(table)
        session.add(player)
        session.commit()
        session.close()
        return "Success"
    else:
        session.close()
        return "Table not found"


def make_ready(table_id: str, player_local_id: int):
    """Make a player ready to play"""
    session = Session()

    table = session.query(Table).filter_by(id=table_id).first()
    readiness = table.players_readiness_list
    readiness[player_local_id] = "1"
    table.players_readiness_list = readiness

    session.add(table)
    session.commit()
    session.close()


def make_unready(table_id: str, player_local_id: int):
    """Make a player unready"""
    session = Session()
    table = session.query(Table).filter_by(id=table_id).first()
    readiness = table.players_readiness_list
    readiness[player_local_id] = "0"
    table.players_readiness_list = readiness

    session.add(table)
    session.commit()
    session.close()
