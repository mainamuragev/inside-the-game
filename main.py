from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI

from app.services.analyzer import (
    analyze_match,
    generate_insights,
)

from app.services.momentum import (
    calculate_momentum,
)

from app.services.recap import (
    generate_match_recap,
)

from app.services.commentary import (
    generate_commentary,
)

from app.services.personas import (
    generate_personalized_views,
)

from app.services.tactics import (
    generate_tactical_insight,
)

app = FastAPI(
    title="Match Intelligence Copilot",
    version="0.1.0",
)


@app.get("/")
def home():
    return {
        "message": "Match Intelligence Copilot",
        "status": "running",
    }


@app.get("/match-analysis")
def match_analysis():

    data = analyze_match(
        "data/raw/match_events.csv"
    )

    data["insights"] = generate_insights(data)

    data["momentum"] = calculate_momentum(
        "data/raw/match_events.csv"
    )

    data["recap"] = generate_match_recap(data)

    data["commentary"] = generate_commentary(
        "data/raw/match_events.csv"
    )

    data["personas"] = generate_personalized_views(data)

    data["tactics"] = generate_tactical_insight(
        "data/raw/match_events.csv"
    )

    return data
