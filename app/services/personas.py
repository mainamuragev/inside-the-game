def generate_personalized_views(data):

    winner = data["insights"]["winner"]
    player = data["insights"]["player_of_match"]

    fan_view = {
        "headline": f"{winner} take the victory!",
        "star_player": player,
        "message": (
            f"{player} was the standout performer "
            f"as {winner} secured the win."
        ),
    }

    analyst_view = {
        "winner": winner,
        "player_of_match": player,
        "xg": data["xg"],
        "momentum_periods": len(data["momentum"]),
    }

    studio_view = {
        "overlay_title": f"{winner} In Control",
        "key_story": (
            f"{player} led the match with the "
            f"highest attacking contribution."
        ),
    }

    return {
        "fan": fan_view,
        "analyst": analyst_view,
        "studio": studio_view,
    }
