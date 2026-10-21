import pandas as pd


def generate_commentary(csv_path: str):

    df = pd.read_csv(csv_path)

    commentary = []

    for _, row in df.iterrows():

        minute = row["minute"]
        player = row["player"]
        team = row["team"]
        event = row["event"]

        if event == "goal":
            text = (
                f"{minute}': GOAL! "
                f"{player} scores for {team}."
            )

        elif event == "shot":
            text = (
                f"{minute}': "
                f"{player} attempts a shot "
                f"for {team}."
            )

        elif event == "pass":
            text = (
                f"{minute}': "
                f"{player} keeps possession "
                f"for {team}."
            )

        else:
            text = (
                f"{minute}': "
                f"{player} involved in play."
            )

        commentary.append(text)

    return commentary
