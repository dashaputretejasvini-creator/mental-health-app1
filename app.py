import streamlit as st

# ── PAGE CONFIG (must be first line always) ──────────
st.set_page_config(
    page_title="Mental Health Risk Analyser",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── MAIN PAGE ────────────────────────────────────────
st.title("🧠 Mental Health Risk Analyser")
st.markdown("---")

st.markdown("""
Welcome to the **Mental Health Risk Analyser** app.

This app analyses mental health patterns across different groups 
and helps identify individual risk levels.
""")

# ── INFO CARDS ───────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.info("📊 **Overview**\n\nPopulation level stats and key metrics")

with col2:
    st.success("👥 **Group Analysis**\n\nAge group and category wise patterns")

with col3:
    st.warning("👤 **Individual**\n\nEnter your details and get risk score")

with col4:
    st.error("🤖 **Predict**\n\nML model predicts your risk level")

st.markdown("---")
st.markdown("👈 **Use the sidebar to navigate between pages**")
