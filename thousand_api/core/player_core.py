"""TODO: Write docstring"""

from sqlalchemy import Boolean

from thousand_api.db.database import Session
from thousand_api.models.player_model import Player


def get_player(player_id: str):
    """TODO: Write docstring"""
    session = Session()
    player = session.query(Player).filter_by(id=player_id).first()
    session.close()

    if player:
        return player
    else:
        return None


def create_player(player_id: str):
    """TODO: Write docstring"""
    session = Session()
    player = Player(id=player_id)
    session.add(player)
    session.commit()
    session.close()

    return player_id


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


def update_player(
    player_id,
    local_id,
    cards_init,
    cards_current,
    cards_played,
    bolt_count,
    barrel_count,
    on_barrel_since,
    round_point,
    point,
    max_biddable_amount,
    silent: Boolean,
):
    """
    Update a game in the database.

    Args:
        player_id (str): The ID of the player to update.
        local_id (str): The Local ID of the player.
        cards_init (str): Initial cards.
        cards_current (str): Current cards.
        cards_played (str): Played cards.
        bolt_count (int): Bolt count.
        barrel_count (int): Barrel count.
        on_barrel_since (int): Since how many rounds on barrel.
        round_point (int): Round Point.
        point (int): Overall point for a game.
        max_biddable_amount (int): Maximum biddable amount.
        silent (bool): Silent or not
        ...

    Returns:
        bool: True if the game was updated successfully, False otherwise.
    """
    session = Session()
    try:
        player = session.query(Player).filter_by(id=player_id).first()
        if player:
            player.local_id = local_id
            player.cards_init = cards_init
            player.cards_current = cards_current
            player.cards_played = cards_played
            player.bolt_count = bolt_count
            player.barrel_count = barrel_count
            player.on_barrel_since = on_barrel_since
            player.round_point = round_point
            player.point = point
            player.max_biddable_amount = max_biddable_amount
            player.silent = bool(silent)

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
