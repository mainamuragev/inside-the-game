import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8001/match-analysis"

st.set_page_config(
    page_title="Match Intelligence Copilot",
    layout="wide",
)

st.title("⚽ Match Intelligence Copilot")

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    data = response.json()

except requests.RequestException as e:
    st.error(f"Unable to reach API: {e}")
    st.stop()

# MATCH SUMMARY

st.header("Match Summary")

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

# AI RECAP

st.divider()

st.header("AI Match Recap")

st.info(
    data["recap"]["narrative"]
)

# XG CHART

st.divider()

st.header("Expected Goals")

xg_df = pd.DataFrame(
    list(data["xg"].items()),
    columns=["Team", "xG"]
)

st.bar_chart(
    xg_df.set_index("Team")
)

# MOMENTUM

st.divider()

st.header("Momentum Timeline")

momentum_df = pd.DataFrame(
    data["momentum"]
)

st.dataframe(
    momentum_df,
    use_container_width=True
)

# TACTICS

st.divider()

st.header("Tactical Intelligence")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Passes")
    st.json(
        data["tactics"]["passes"]
    )

with col2:
    st.subheader("Tackles")
    st.json(
        data["tactics"]["tackles"]
    )

with col3:
    st.subheader("Pressure")
    st.json(
        data["tactics"]["pressure"]
    )

# COMMENTARY

st.divider()

st.header("AI Commentary")

for line in data["commentary"]:
    st.write(f"• {line}")

# PERSONAS

st.divider()

st.header("Personalised Experiences")


def render_persona(persona):

    if isinstance(persona, dict):

        if "headline" in persona:
            st.subheader(
                persona["headline"]
            )

        for key, value in persona.items():

            if key != "headline":

                st.markdown(
                    f"**{key.replace('_', ' ').title()}:** {value}"
                )

    else:
        st.write(persona)


tab1, tab2, tab3 = st.tabs(
    ["Fan", "Analyst", "Studio"]
)

with tab1:
    render_persona(
        data["personas"]["fan"]
    )

with tab2:
    render_persona(
        data["personas"]["analyst"]
    )

with tab3:
    render_persona(
        data["personas"]["studio"]
    )

# RAW RESPONSE

st.divider()

with st.expander(
    "View Raw API Response"
):
    st.json(data)
