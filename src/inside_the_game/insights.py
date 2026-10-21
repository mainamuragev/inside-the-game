import pandas as pd


def load_events(path="data/raw/match_events.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.lstrip("#").strip() for c in df.columns]
    df.insert(0, "event_id", range(1, len(df) + 1))
    return df


def build_facts(df: pd.DataFrame, big_chance_xg: float = 0.30) -> dict:
    """Turn raw events into facts an LLM can narrate without inventing anything."""
    teams = list(df["team"].unique())
    attempts = df[df["event"].isin(["shot", "goal"])]  # assumes a goal row IS the shot

    score = {t: 0 for t in teams}
    moments = []
    for r in df.sort_values("minute").itertuples():
        if r.event == "goal":
            score[r.team] += 1
            moments.append({
                "event_id": r.event_id, "minute": r.minute, "type": "goal",
                "team": r.team, "player": r.player, "xg": r.xg,
                "score_after": dict(score),
            })
        elif r.event == "shot" and r.xg >= big_chance_xg:
            moments.append({
                "event_id": r.event_id, "minute": r.minute, "type": "big_chance_missed",
                "team": r.team, "player": r.player, "xg": r.xg,
            })

    return {
        "final_score": score,
        "xg": attempts.groupby("team")["xg"].sum().round(2).to_dict(),
        "shots": attempts.groupby("team").size().to_dict(),
        "moments": moments,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(build_facts(load_events()), indent=2))
