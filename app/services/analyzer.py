import pandas as pd


def analyze_match(csv_path: str):
    df = pd.read_csv(csv_path)

    goals = (
        df[df["event"] == "goal"]
        .groupby("team")
        .size()
        .to_dict()
    )

    shots = (
        df[df["event"] == "shot"]
        .groupby("team")
        .size()
        .to_dict()
    )

    xg = (
        df.groupby("team")["xg"]
        .sum()
        .round(2)
        .to_dict()
    )

    player_xg = (
        df.groupby("player")["xg"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .round(2)
        .to_dict()
    )

    return {
        "goals": goals,
        "shots": shots,
        "xg": xg,
        "top_players": player_xg,
    }


def generate_insights(results):
    winning_team = max(
        results["goals"],
        key=results["goals"].get,
    )

    best_player = max(
        results["top_players"],
        key=results["top_players"].get,
    )

    return {
        "winner": winning_team,
        "player_of_match": best_player,
        "summary": (
            f"{winning_team} generated the strongest attacking "
            f"performance and {best_player} was the most influential player."
        ),
    }
