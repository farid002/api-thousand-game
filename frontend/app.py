"""TODO: Write docstring"""

import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
FASTAPI_URL = "http://127.0.0.1:5002"


@app.route("/")
def index():
    """TODO: Write docstring"""
    return render_template("index.html")


@app.route("/games")
def get_games():
    """TODO: Write docstring"""
    response = requests.get(FASTAPI_URL + "/game/all")
    games = response.json()
    return render_template("games.html", games=games)


@app.route("/game/<game_id>", methods=["GET"])
def get_game(game_id):
    """TODO: Write docstring"""
    response = requests.get(f"{FASTAPI_URL}/game/{game_id}")
    game = response.json()
    return game


@app.route("/game/<game_id>/edit", methods=["GET", "POST"])
def edit_game(game_id):
    """TODO: Write docstring"""
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
def delete_game(game_id):
    """TODO: Write docstring"""
    requests.delete(f"{FASTAPI_URL}/game/{game_id}")
    return redirect(url_for("index"))


@app.route("/players")
def get_players():
    """TODO: Write docstring"""
    response = requests.get(FASTAPI_URL + "/player")
    players = response.json()
    return render_template("players.html", players=players)


@app.route("/player/<player_id>", methods=["GET"])
def get_player(player_id):
    """TODO: Write docstring"""
    response = requests.get(f"{FASTAPI_URL}/player/{player_id}")
    player = response.json()
    return player


@app.route("/player/<player_id>/delete")
def delete_player(player_id):
    """TODO: Write docstring"""
    requests.delete(f"{FASTAPI_URL}/player/{player_id}")
    return redirect(url_for("get_players"))


if __name__ == "__main__":
    """TODO: Write docstring"""
    app.run(debug=True)
