from hangman import db
from flask_login import UserMixin
import random
from sqlalchemy import DateTime, func


MAXIMUM_ALLOWED_ERRORS = 10


def generate_game_id() -> int:
    return random.randint(1e9, 1e10)


def choose_random_word() -> str:
    words = [line.rstrip() for line in open("hangman/static/words.txt")]
    return random.choice(words).upper()


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(180), unique=True, nullable=False)
    picture = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(100), nullable=False)


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True, default=generate_game_id)
    word = db.Column(db.String(50), default=choose_random_word)
    attempts = db.Column(db.String(50), default="")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    result = db.Column(db.String(50))
    date = db.Column(DateTime, default=func.now())
    user = db.relationship("User", backref=db.backref("user", uselist=False))

    @property
    def errors(self) -> str:
        return "".join(set(self.attempts) - set(self.word))

    @property
    def current(self) -> str:
        return "".join([c if c in self.attempts else "_" for c in self.word])

    @property
    def won(self) -> bool:
        return self.current == self.word

    @property
    def lost(self) -> bool:
        return len(self.errors) == MAXIMUM_ALLOWED_ERRORS

    @property
    def finished(self) -> bool:
        return self.won or self.lost

    def try_letter(self, letter: str) -> None:
        if not self.finished and letter not in self.attempts:
            self.attempts += letter
            db.session.commit()

    def update_result(self) -> None:
        if self.won:
            self.result = "won"
        elif self.lost:
            self.result = "lost"
        db.session.commit()
