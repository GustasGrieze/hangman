from typing import Union, Literal
from requests import Response
from hangman import app, db, bcrypt, forms
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user, login_user, logout_user
from hangman.models import User, Game
from hangman.functions import (
    calculate_games_played,
    calculate_win_rate,
    calculate_total_guesses,
    get_last_10_games,
)
from PIL import Image
import os
import secrets
import flask
import logging


logging.basicConfig(
    filename="hangman/logs/info.log",
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s",
)


@app.route("/")
def index() -> str:
    if current_user.is_authenticated:
        return render_template("main.html")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[Response, str]:
    if current_user.is_authenticated:
        return redirect(url_for("main"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            logging.info(f"User: {form.email.data} has logged in")
            return redirect(next_page) if next_page else redirect(url_for("main"))
        flash("Login failure, please check details", "danger")
    return render_template("login.html", form=form, title="login")


@app.route("/register", methods=["GET", "POST"])
def register() -> Union[Response, str]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            name=form.name.data, email=form.email.data, password=encrypted_password
        )
        if not User.query.filter_by(email=form.email.data).first():
            db.session.add(user)
            db.session.commit()
            flash(
                f"User: {form.email.data} was successfully created, please log in",
                "success",
            )
            logging.info(f"User: {form.email.data} was created")
            return redirect(url_for("login"))
        flash("Email is already in use, please choose a different email", "danger")
    return render_template("register.html", form=form, title="register")


def save_picture(form_picture: str) -> str:
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pictures", picture_fn)

    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile() -> Union[Response, str]:
    form = forms.ProfileUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture = save_picture(form.picture.data)
            current_user.picture = picture
        current_user.name = form.name.data
        db.session.commit()
        flash("Your profile has been updated", "success")
        return redirect(url_for("profile"))
    if request.method == "GET":
        form.name.data = current_user.name
    picture = url_for("static", filename="profile_pictures/" + current_user.picture)
    return render_template("profile.html", title="Account", form=form, picture=picture)


@app.route("/play")
@login_required
def new_game() -> Response:
    game = Game(user_id=current_user.get_id())
    db.session.add(game)
    db.session.commit()
    return redirect(url_for("play", game_id=game.id))


@app.route("/play/<game_id>", methods=["GET", "POST"])
@login_required
def play(game_id) -> Union[Response, str]:
    game = Game.query.get_or_404(game_id)
    if request.method == "POST":
        letter = request.form["letter"].upper()
        if len(letter) == 1 and letter.isalpha():
            game.try_letter(letter)
        if game.finished:
            game.update_result()
            logging.info(
                f"User ID={current_user.get_id()} {game.result} game {game.id}"
            )
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return flask.jsonify(
            current=game.current, errors=game.errors, finished=game.finished
        )
    return render_template("play.html", game=game)


@app.route("/stats")
@login_required
def stats() -> str:
    return render_template(
        "stats.html",
        games_played=calculate_games_played(),
        win_rate=calculate_win_rate(),
        total_guesses=calculate_total_guesses(),
        games=get_last_10_games(),
    )


@app.route("/main")
@login_required
def main() -> str:
    return render_template("main.html")


@app.route("/logout")
@login_required
def logout() -> str:
    logout_user()
    return redirect(url_for("index"))


@app.errorhandler(404)
def error_404(error) -> tuple[str, Literal[404]]:
    return render_template("404.html"), 404
