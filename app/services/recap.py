from inside_the_game.insights import load_events, build_facts


def generate_match_recap(results, csv_path: str = "data/raw/match_events.csv"):
    facts = build_facts(load_events(csv_path))
    score, xg = facts["final_score"], facts["xg"]
    winner = results["insights"]["winner"]

    if winner not in score:  # draw or unexpected value
        narrative = "The match ended level. " + ", ".join(f"{t} {g}" for t, g in score.items())
        return {"narrative": narrative, "facts": facts}

    loser = next(t for t in score if t != winner)
    goals = [m for m in facts["moments"] if m["type"] == "goal"]
    goal_text = "; ".join(
        f"{m['player']} {m['minute']}' (event {m['event_id']})" for m in goals
    )
    missed = [m for m in facts["moments"] if m["type"] == "big_chance_missed"]
    missed_text = ", ".join(
        f"{m['player']} {m['minute']}' (event {m['event_id']})" for m in missed
    )

    narrative = (
        f"{winner} beat {loser} {score[winner]}-{score[loser]}, "
        f"creating {xg[winner]} xG to {xg[loser]}. "
        f"Goals: {goal_text}. "
        + (f"Big chances that didn't go in: {missed_text}." if missed_text else "")
    )
    return {"narrative": narrative, "facts": facts}
