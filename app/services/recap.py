def generate_match_recap(results):

    winner = results["insights"]["winner"]

    player = results["insights"]["player_of_match"]

    winner_goals = results["goals"][winner]

    momentum_periods = len(
        results["momentum"]
    )

    recap = (
        f"{winner} secured a victory with "
        f"{winner_goals} goals. "
        f"{player} produced the most influential "
        f"performance of the match. "
        f"The game featured {momentum_periods} key "
        f"momentum periods which helped shape the "
        f"final result."
    )

    return {
        "narrative": recap
    }
