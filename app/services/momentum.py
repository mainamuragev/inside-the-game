import pandas as pd


def calculate_momentum(csv_path: str):

    df = pd.read_csv(csv_path)

    windows = [
        (0, 15),
        (15, 30),
        (30, 45),
        (45, 60),
        (60, 75),
        (75, 90),
    ]

    momentum = []

    for start, end in windows:

        period = df[
            (df["minute"] >= start)
            & (df["minute"] < end)
        ]

        if period.empty:
            continue

        team_xg = (
            period.groupby("team")["xg"]
            .sum()
            .to_dict()
        )

        if team_xg:

            dominant_team = max(
                team_xg,
                key=team_xg.get
            )

            momentum.append({
                "period": f"{start}-{end}",
                "dominant_team": dominant_team,
                "xg": round(
                    team_xg[dominant_team],
                    2
                )
            })

    return momentum
