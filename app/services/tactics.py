import pandas as pd


def generate_tactical_insight(csv_path: str):

    df = pd.read_csv(csv_path)

    passes = (
        df[df["event"] == "pass"]
        .groupby("team")
        .size()
        .to_dict()
    )

    tackles = (
        df[df["event"] == "tackle"]
        .groupby("team")
        .size()
        .to_dict()
    )

    pressure = (
        df[df["event"] == "pressure"]
        .groupby("team")
        .size()
        .to_dict()
    )

    return {
        "passes": passes,
        "tackles": tackles,
        "pressure": pressure
    }
