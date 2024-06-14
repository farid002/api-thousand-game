"""System test to play a round on pre-configured db"""

import os
import shutil

import requests

if __name__ == "__main__":
    if os.path.exists("games.db"):
        os.remove("games.db")

    shutil.copyfile("test_db/games.db", "games.db")
    game_id = "40222538-3d6a-4f4a-950d-8402f4614714"
    players_ids = ["farid", "huseyn", "samir"]
    headers = {"accept": "application/json"}

    bid_player_sequence = [0, 1, 2, 0]
    bid_sequence = [105, 110, 115, 120]

    card_player_sequence = [0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 0, 1, 2, 1, 2, 0, 0, 1, 2, 2, 0, 1]
    card_sequence = [
        (0, "A♦"),
        (1, "9♦"),
        (2, "Q♦"),
        (0, "10♦"),
        (1, "J♧"),
        (2, "9♥"),
        (0, "K♦"),
        (1, "9♧"),
        (2, "J♥"),
        (0, "J♦"),
        (1, "A♥"),
        (2, "K♥"),
        (0, "K♧"),
        (1, "A♧"),
        (2, "10♧"),
        (1, "10♥"),
        (2, "A♤"),
        (0, "Q♧"),
        (0, "K♤"),
        (1, "9♤"),
        (2, "10♤"),
        (2, "Q♤"),
        (0, "J♤"),
        (1, "Q♥"),
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
            params={"game_id": game_id, "player_id": players_ids[0], "card1": "J♥", "card2": "Q♥"},
        )
    )

    # making final bid for the bid winner
    print(
        requests.put(
            f"http://localhost:5001/game/{game_id}/make_final_bid",
            params={"game_id": game_id, "player_id": players_ids[0], "final_bid": 120},
        )
    )

    # playing cards
    for i in range(24):
        print(
            requests.put(
                f"http://localhost:5001/game/{game_id}/play_card",
                params={
                    "game_id": game_id,
                    "player_id": players_ids[card_sequence[i][0]],
                    "card": card_sequence[i][1],
                },
            )
        )
