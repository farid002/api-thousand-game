"""Docstring"""

import requests
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "your_secret_key"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

FASTAPI_URL = "http://147.78.130.54:5002"
# FASTAPI_URL = "http://localhost:5002"  # for local debugging

# Mock user database
users = {"admin": {"password": generate_password_hash("admin", method="scrypt")}}


class User(UserMixin):
    """User class for login"""

    def __init__(self, username):
        """Init with id"""
        self.id = username


@login_manager.user_loader
def load_user(user_id):
    """Load user"""
    return User(user_id) if user_id in users else None


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login implementation"""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and check_password_hash(users[username]["password"], password):
            user = User(username)
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Logout function"""
    logout_user()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    """Docstring"""
    games_response = requests.get(FASTAPI_URL + "/game/all")
    players_response = requests.get(FASTAPI_URL + "/player/all")
    games = games_response.json()
    players = players_response.json()
    return render_template("index.html", FASTAPI_URL=FASTAPI_URL, games=games, players=players)


@app.route("/play")
@login_required
def play():
    """Docstring"""
    response = requests.get(FASTAPI_URL + "/game/all")
    games = response.json()
    return render_template("play.html", games=games, FASTAPI_URL=FASTAPI_URL)


@app.route("/games")
@login_required
def get_games():
    """Docstring"""
    response = requests.get(FASTAPI_URL + "/game/all")
    games = response.json()
    return render_template("games.html", games=games, FASTAPI_URL=FASTAPI_URL)


@app.route("/tables")
@login_required
def get_tables():
    """Docstring"""
    response = requests.get(FASTAPI_URL + "/table/all")
    tables = response.json()
    return render_template("tables.html", tables=tables, FASTAPI_URL=FASTAPI_URL)


@app.route("/game/<game_id>", methods=["GET"])
@login_required
def get_game(game_id):
    """Docstring"""
    response = requests.get(f"{FASTAPI_URL}/game/{game_id}")
    game = response.json()
    return game


@app.route("/game/<game_id>/edit", methods=["GET", "POST"])
@login_required
def edit_game(game_id):
    """Docstring"""
    if request.method == "POST":
        game_data = request.json
        player0_id = game_data["player0_id"]
        player1_id = game_data["player1_id"]
        player2_id = game_data["player2_id"]
        requests.put(
            f"{FASTAPI_URL}/game/{game_id}/edit?player0_id={player0_id}&player1_id={player1_id}&player2_id={player2_id}"
        )
        return redirect(url_for("index"))

    response = requests.get(f"{FASTAPI_URL}/game/{game_id}")
    game = response.json()
    return game


@app.route("/game/<game_id>/delete")
@login_required
def delete_game(game_id):
    """Docstring"""
    requests.delete(f"{FASTAPI_URL}/game/{game_id}")
    return redirect(url_for("get_games"))


@app.route("/players")
@login_required
def get_players():
    """Docstring"""
    response = requests.get(FASTAPI_URL + "/player/all")
    players = response.json()
    return render_template("players.html", players=players, FASTAPI_URL=FASTAPI_URL)


@app.route("/player/<player_id>", methods=["GET"])
@login_required
def get_player(player_id):
    """Docstring"""
    response = requests.get(f"{FASTAPI_URL}/player/{player_id}")
    player = response.json()
    return player


@app.route("/player/<player_id>/edit", methods=["GET", "POST"])
@login_required
def edit_player(player_id):
    """Docstring"""
    if request.method == "POST":
        player_data = request.json
        local_id = player_data["local_id"]
        cards_init = player_data["cards_init"]
        cards_current = player_data["cards_current"]
        cards_played = player_data["cards_played"]
        bolt_count = player_data["bolt_count"]
        barrel_count = player_data["barrel_count"]
        on_barrel_since = player_data["on_barrel_since"]
        round_point = player_data["round_point"]
        point = player_data["point"]
        max_biddable_amount = player_data["max_biddable_amount"]
        silent = player_data["silent"]
        requests.put(
            f"{FASTAPI_URL}/player/{player_id}/edit?local_id={local_id}&cards_init={cards_init}"
            f"&cards_current={cards_current}&cards_played={cards_played}&bolt_count={bolt_count}"
            f"&barrel_count={barrel_count}&on_barrel_since={on_barrel_since}&round_point={round_point}"
            f"&point={point}&max_biddable_amount={max_biddable_amount}&silent={silent}"
        )
        return redirect(url_for("get_players"))

    response = requests.get(f"{FASTAPI_URL}/player/{player_id}")
    player = response.json()
    return player


@app.route("/player/<player_id>/delete")
@login_required
def delete_player(player_id):
    """Docstring"""
    requests.delete(f"{FASTAPI_URL}/player/{player_id}")
    return redirect(url_for("get_players"))


if __name__ == "__main__":
    app.run(debug=True)
