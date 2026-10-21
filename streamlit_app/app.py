import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001/match-analysis"

st.set_page_config(page_title="Match Intelligence Copilot", layout="wide")
st.title("⚽ Match Intelligence Copilot")

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.RequestException as e:
    st.error(f"Backend not reachable at {API_URL}. Start it first. ({e})")
    st.stop()

st.header("Match Result")
col1, col2 = st.columns(2)
col1.metric("Winner", data["insights"]["winner"])
col2.metric("Player of Match", data["insights"]["player_of_match"])

st.divider()
st.header("AI Match Recap")
st.info(data["recap"]["narrative"])

facts = data["recap"].get("facts")
if facts:
    with st.expander("Why does the AI say this? (evidence)"):
        c1, c2 = st.columns(2)
        c1.write("**xG**")
        c1.json(facts["xg"])
        c2.write("**Shots**")
        c2.json(facts["shots"])
        st.write("**Key moments**")
        st.dataframe(facts["moments"], use_container_width=True)

st.divider()
st.header("Momentum Timeline")
for period in data["momentum"]:
    st.write(f"{period['period']} → {period['dominant_team']} (xG: {period['xg']})")

st.divider()
st.header("AI Commentary")
for line in data["commentary"]:
    st.write(line)

st.divider()
st.header("Personalised Experiences")


def render_persona(p):
    if isinstance(p, dict):
        if "headline" in p:
            st.subheader(p["headline"])
        for k, v in p.items():
            if k != "headline":
                st.markdown(f"**{k.replace('_', ' ').title()}:** {v}")
    else:
        st.write(p)


tab1, tab2, tab3 = st.tabs(["Fan", "Analyst", "Studio"])
with tab1:
    render_persona(data["personas"]["fan"])
with tab2:
    render_persona(data["personas"]["analyst"])
with tab3:
    render_persona(data["personas"]["studio"])
