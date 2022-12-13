from hangman import db
from sqlalchemy import func, and_, desc
from flask_login import current_user
from models import Game, User


def get_last_10_games() -> list:
    return db.session.query(Game).join(User, User.id == Game.user_id).filter(User.id == current_user.get_id()).order_by(desc(Game.date)).limit(10).all()

def calculate_total_guesses() -> int:
    list_of_guesses = db.session.query(Game).join(User, User.id == Game.user_id).filter(User.id == current_user.get_id()).with_entities(func.length(Game.attempts)).all()
    return sum([i[0] for i in list_of_guesses])

def calculate_won_games() -> int:
    return db.session.query(Game).join(User, User.id == Game.user_id).filter(and_(User.id == current_user.get_id(), Game.result == "won")).with_entities(func.count()).scalar()

def calculate_games_played() -> int:
    return db.session.query(Game).join(User, User.id == Game.user_id).filter(User.id == current_user.get_id()).with_entities(func.count()).scalar()

def calculate_win_rate() -> int:
    try:
        return int(calculate_won_games() / calculate_games_played() * 100)
    except ZeroDivisionError:
        return 0
