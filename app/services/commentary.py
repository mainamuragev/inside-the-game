from inside_the_game.insights import load_events


def _ordinal(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def generate_commentary(csv_path: str):
    df = load_events(csv_path).sort_values("minute")
    teams = list(df["team"].unique())
    score = {t: 0 for t in teams}
    attempts = {}
    lines = []

    for r in df.itertuples():
        tag = f"(event {r.event_id})"
        if r.event in ("shot", "goal"):
            attempts[r.player] = attempts.get(r.player, 0) + 1
        n = attempts.get(r.player, 0)

        if r.event == "goal":
            score[r.team] += 1
            lines.append(
                f"{r.minute}': GOAL! {r.player} scores for {r.team} "
                f"({r.xg:.2f} xG, attempt #{n}). "
                f"{teams[0]} {score[teams[0]]}-{score[teams[1]]} {teams[1]} {tag}"
            )
        elif r.event == "shot":
            kind = "a big chance" if r.xg >= 0.30 else "a speculative effort"
            lines.append(
                f"{r.minute}': {r.player} has {kind} for {r.team} "
                f"({r.xg:.2f} xG), his {_ordinal(n)} attempt {tag}"
            )
        elif r.event == "pass":
            lines.append(f"{r.minute}': {r.player} keeps possession for {r.team} {tag}")
        else:
            lines.append(f"{r.minute}': {r.player} involved in play {tag}")

    return lines
