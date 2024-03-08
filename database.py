"""TODO: Write docstring"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import Base, Player, Round

engine = create_engine("sqlite:///games.db")
Session = sessionmaker(bind=engine)


def create_tables():
    """TODO: Write docstring"""
    Base.metadata.create_all(engine)


def database_init():
    """TODO: Write docstring"""
    create_tables()


def update_players_db(session, players):
    """TODO: Write docstring"""
    for player in players:
        session.merge(player)
    session.commit()


def get_current_round_from_db(session, game_id):
    """TODO: Write docstring"""
    return (
        session.query(Round)
        .filter_by(game_id=game_id)
        .order_by(Round.id.desc())
        .first()
    )


def get_player_from_db(session, player_id):
    """TODO: Write docstring"""
    return session.query(Player).filter_by(id=player_id).first()
