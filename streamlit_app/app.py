import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/match-analysis"

st.set_page_config(
    page_title="Match Intelligence Copilot",
    layout="wide",
)

st.title("⚽ Match Intelligence Copilot")

response = requests.get(API_URL)

data = response.json()

st.header("Match Result")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Winner",
        data["insights"]["winner"]
    )

with col2:
    st.metric(
        "Player of Match",
        data["insights"]["player_of_match"]
    )

st.divider()

st.header("AI Match Recap")

st.info(
    data["recap"]["narrative"]
)

st.divider()

st.header("Momentum Timeline")

for period in data["momentum"]:

    st.write(
        f"{period['period']} → "
        f"{period['dominant_team']} "
        f"(xG: {period['xg']})"
    )

st.divider()

st.header("AI Commentary")

for event in data["commentary"]:
    st.write(event)

st.divider()

st.header("Personalised Experiences")

tab1, tab2, tab3 = st.tabs(
    ["Fan", "Analyst", "Studio"]
)

with tab1:
    st.json(
        data["personas"]["fan"]
    )

with tab2:
    st.json(
        data["personas"]["analyst"]
    )

with tab3:
    st.json(
        data["personas"]["studio"]
    )
