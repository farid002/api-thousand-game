"""TODO: Write docstring"""

import uuid
from datetime import datetime

from thousand_api.db.database import Session
from thousand_api.models.table_model import Table, TableState


def create_table(entry_coins: int, reliable: bool, ace_marriage: bool, game_speed: int, password: int, till_1001: bool):
    """TODO: Write docstring"""
    session = Session()

    table_id = str(uuid.uuid4())
    table = Table(
        id=table_id,
        creation_date=str(datetime.now()),
        table_state=TableState.CREATED.value,
        entry_coins=entry_coins,
        reliable=reliable,
        ace_marriage=ace_marriage,
        game_speed=game_speed,
        password=password,
        till_1001=till_1001,
    )

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
    table = session.query(Table).filter(id == table_id).first()
    session.close()

    if table:
        return [table.player0, table.player1, table.player2]
    else:
        return None
