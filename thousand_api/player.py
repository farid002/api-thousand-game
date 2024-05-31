"""TODO: Write docstring"""

from thousand_api.database import Session
from thousand_api.model import *


def get_player(player_id: str):
    """TODO: Write docstring"""
    session = Session()
    player = session.query(Player).filter_by(id=player_id).first()
    session.close()

    if player:
        return player
    else:
        return None


def delete_player(player_id):
    """
    Delete a game from the database by its ID.

    Args:
        player_id (int): The ID of the game to delete.

    Returns:
        bool: True if the game was deleted successfully, False otherwise.
    """
    session = Session()
    try:
        player = session.query(Player).filter_by(id=player_id).first()
        if player:
            session.delete(player)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting player: {e}")
        return False
    finally:
        session.close()


def update_player(player_id, on_barrel_since, round_point, point, max_biddable_amount):
    """
    Update a game in the database.

    Args:
        player_id (str): The ID of the player to update.
        on_barrel_since (int): Since how many rounds on barrel.
        round_point (int): Round Point.
        point (int): Overall point for a game.
        max_biddable_amount (int): Maximum biddable amount.
        ...

    Returns:
        bool: True if the game was updated successfully, False otherwise.
    """
    session = Session()
    try:
        player = session.query(Player).filter_by(id=player_id).first()
        if player:
            player.on_barrel_since = on_barrel_since
            player.round_point = round_point
            player.point = point
            player.max_biddable_amount = max_biddable_amount
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error updating player: {e}")
        return False
    finally:
        session.close()


def get_players():
    """TODO: Write docstring"""
    session = Session()
    players = session.query(Player).all()
    session.close()

    if players:
        return players
    else:
        return None
