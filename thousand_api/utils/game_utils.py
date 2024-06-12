"""TODO: Write docstring"""

from thousand_api.db.database import Session
from thousand_api.models.game import Game
from thousand_api.models.round import Round


def get_game(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    session.close()

    if game:
        return game
    else:
        return None


def delete_game(game_id):
    """
    Delete a game from the database by its ID.

    Args:
        game_id (int): The ID of the game to delete.

    Returns:
        bool: True if the game was deleted successfully, False otherwise.
    """
    session = Session()
    try:
        game = session.query(Game).filter_by(id=game_id).first()
        if game:
            session.delete(game)
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error deleting game: {e}")
        return False
    finally:
        session.close()


def update_game(game_id, player0_id, player1_id, player2_id):
    """
    Update a game in the database.

    Args:
        game_id (int): The ID of the game to update.
        player0_id (int): ID of player 1.
        player1_id (int): ID of player 2.
        player2_id (int): ID of player 3.

    Returns:
        bool: True if the game was updated successfully, False otherwise.
    """
    session = Session()
    try:
        game = session.query(Game).filter_by(id=game_id).first()
        if game:
            game.player0_id = player0_id
            game.player1_id = player1_id
            game.player2_id = player2_id
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        print(f"Error updating game: {e}")
        return False
    finally:
        session.close()


def get_games():
    """TODO: Write docstring"""
    session = Session()
    games = session.query(Game).all()
    session.close()

    if games:
        return games
    else:
        return None


def get_players(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter(id == game_id).first()
    session.close()

    if game:
        return [game.player0, game.player1, game.player2]
    else:
        return None


def get_current_round(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    round_number = game.current_round
    curr_round = session.query(Round).filter_by(game_id=game_id, round_number=round_number).first()
    session.close()

    if curr_round:
        return curr_round
    else:
        return None


def get_bid_winner_local_id(game_id: str):
    """TODO: Write docstring"""
    session = Session()
    game = session.query(Game).filter_by(id=game_id).first()
    round_number = game.current_round
    curr_round = session.query(Round).filter_by(game_id=game_id, round_number=round_number).first()
    session.close()

    if curr_round:
        return curr_round.bid_winner
    else:
        return None
