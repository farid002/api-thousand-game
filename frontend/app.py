"""TODO: Write docstring"""

import requests
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
FASTAPI_URL = "http://http://147.78.130.54:5002"
# FASTAPI_URL = "http://localhost:5002"  # for local debugging uncomment this line


@app.route("/")
def index():
    """TODO: Write docstring"""
    return render_template("index.html")


@app.route("/play")
def play():
    """TODO: Write docstring"""
    response = requests.get(FASTAPI_URL + "/game/all")
    games = response.json()
    return render_template("play.html", games=games)


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
    return redirect(url_for("get_games"))


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


@app.route("/player/<player_id>/edit", methods=["GET", "POST"])
def edit_player(player_id):
    """TODO: Write docstring"""
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
def delete_player(player_id):
    """TODO: Write docstring"""
    requests.delete(f"{FASTAPI_URL}/player/{player_id}")
    return redirect(url_for("get_players"))


if __name__ == "__main__":
    """TODO: Write docstring"""
    app.run(debug=True)
