"""TODO: Write docstring"""

from model import Base, Game, Player, Round
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///games.db")
Session = sessionmaker(bind=engine)


def database_init():
    """TODO: Write docstring"""
    Base.metadata.create_all(engine)


def update_players_db(session, players):
    """TODO: Write docstring"""
    for player in players:
        session.merge(player)
    session.commit()


def get_current_round_from_db(session, game_id) -> Round:
    """TODO: Write docstring"""
    game_obj = session.query(Game).filter_by(id=game_id).first()
    return session.query(Round).filter_by(game_id=game_id, round_number=game_obj.current_round).first()


def get_player_from_db(session, player_id: str) -> Player:
    """TODO: Write docstring"""
    return session.query(Player).filter_by(id=player_id).first()


def get_player_with_game_and_local_id_from_db(session, game_id: str, player_local_id: int) -> Player:
    """TODO: Write docstring"""
    game = session.query(Game).filter_by(id=game_id).first()
    player_id = str(getattr(game, f"player{player_local_id}_id"))

    return get_player_from_db(session, player_id)


def get_players_with_game_from_db(session, game: Game) -> list[Player]:
    """Gets list of 3 players of a game with given id"""
    player0 = get_player_from_db(session, game.player0_id)
    player1 = get_player_from_db(session, game.player1_id)
    player2 = get_player_from_db(session, game.player2_id)

    return [player0, player1, player2]
