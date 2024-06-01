"""System test to play a round on pre-configured db"""

import os
import shutil

import requests

if __name__ == "__main__":
    if os.path.exists("games.db"):
        os.remove("games.db")

    shutil.copyfile("test_db/games.db", "games.db")
    game_id = "game1"
    players_ids = ["farid", "huseyn", "samir"]
    headers = {"accept": "application/json"}

    bid_player_sequence = [0, 1, 2, 0]
    bid_sequence = [110, 120, 130, 140]

    card_player_sequence = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 0, 1, 2, 0, 1, 2, 0, 1, 2]
    card_sequence = [
        "A♤",
        "9♧",
        "9♤",
        "10♤",
        "J♧",
        "J♤",
        "K♤",
        "10♧",
        "Q♤",
        "Q♥",
        "A♥",
        "J♦",
        "9♦",
        "10♦",
        "9♥",
        "10♥",
        "Q♦",
        "Q♧",
        "K♥",
        "K♦",
        "K♧",
        "J♥",
        "A♦",
        "A♧",
    ]

    # bidding
    for i in range(len(bid_sequence)):
        print(
            requests.put(
                f"http://localhost:5001/game/{game_id}/make_bid",
                params={"game_id": game_id, "player_id": players_ids[bid_player_sequence[i]], "bid": bid_sequence[i]},
            )
        )
    print(
        requests.put(
            f"http://localhost:5001/game/{game_id}/pass_bid",
            params={"game_id": game_id, "player_id": players_ids[2]},
        )
    )

    # taking talon (3 cards)
    print(
        requests.put(
            f"http://localhost:5001/game/{game_id}/take_talon",
            params={"game_id": game_id, "player_id": players_ids[0]},
        )
    )

    # giving two cards from bid winner to the other 2 players
    print(
        requests.put(
            f"http://localhost:5001/game/{game_id}/give_two_cards",
            params={"game_id": game_id, "player_id": players_ids[0], "card1": "Q♦", "card2": "J♤"},
        )
    )

    # making final bid for the bid winner
    print(
        requests.put(
            f"http://localhost:5001/game/{game_id}/make_final_bid",
            params={"game_id": game_id, "player_id": players_ids[0], "final_bid": 160},
        )
    )

    # playing cards
    for i in range(24):
        print(
            requests.put(
                f"http://localhost:5001/game/{game_id}/play_card",
                params={
                    "game_id": game_id,
                    "player_id": players_ids[card_player_sequence[i]],
                    "card": card_sequence[i],
                },
            )
        )
