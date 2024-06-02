"""TODO: Write docstring"""

import requests
from flask import Flask, redirect, render_template, request, url_for

from thousand_api.db.database import (
    Session,
    get_current_round_from_db,
    get_player_from_db,
    get_players_with_game_from_db,
)

app = Flask(__name__)
FASTAPI_URL = "http://127.0.0.1:5001"


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
    game_state = game.get("game_state")
    current_round = game.get("current_round")
    
    session = Session()

    if not game:
        return "Game not found", 404

        # Create a dictionary to store player cards
    player_cards = {}

    for i in range(3):
        player_id = game.get(f"player{i}_id")
        player = get_player_from_db(session, player_id)
        if player:
            player_cards[player_id] = player.cards_current_list  # Get cards or an empty list if None
        else:
            player_cards[player_id] = []  # Empty list for players without cards

    game_state = game.get("game_state")
    current_round = game.get("current_round")
    current_player_id = get_current_player_id(game, current_round)

    return render_template(
        'game_info.html',
        game=game,  # Pass the game data
        players=player_cards,
        game_state=game_state,
        current_player_id=current_player_id
    )


def get_current_player_id(game, current_round):
    # Replace with your logic to determine the current player
    # based on the game state and round.
    return game.get("player0_id")

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
