import streamlit as st
import pandas as pd
import sys
import os

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.scoring import calculate_risk

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Individual Risk Profile",
    page_icon="👤",
    layout="wide"
)

# ── TITLE ────────────────────────────────────────────
st.title("👤 Individual Risk Profile")
st.markdown("Enter your details below to get your personal mental health risk score")
st.markdown("---")

# ── FORM ─────────────────────────────────────────────
with st.form("risk_form"):

    st.subheader("Personal Details")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Your Name",
            placeholder="Enter your name..."
        )
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=80,
            value=25
        )
        category = st.selectbox(
            "Category",
            ["Student", "Worker"]
        )
        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

    with col2:
        occupation = st.text_input(
            "Occupation / Course",
            placeholder="e.g. Engineer, BCA, Nurse..."
        )
        bmi = st.selectbox(
            "BMI Category",
            ["Normal", "Overweight", "Obese", "Underweight"]
        )
        family_history = st.selectbox(
            "Family History of Mental Illness",
            ["No", "Yes"]
        )
        dietary_habits = st.selectbox(
            "Dietary Habits",
            ["Healthy", "Moderate", "Unhealthy"]
        )

    st.markdown("---")
    st.subheader("Daily Habits")
    col3, col4 = st.columns(2)

    with col3:
        sleep_hours = st.slider(
            "Sleep Hours per Night",
            min_value=2.0,
            max_value=12.0,
            value=7.0,
            step=0.5
        )
        stress_level = st.slider(
            "Stress Level (1-10)",
            min_value=1,
            max_value=10,
            value=5
        )
        work_study_hours = st.slider(
            "Work / Study Hours per Day",
            min_value=0.0,
            max_value=16.0,
            value=8.0,
            step=0.5
        )

    with col4:
        sleep_quality = st.slider(
            "Sleep Quality (1-10)",
            min_value=1,
            max_value=10,
            value=6
        )
        physical_activity = st.slider(
            "Physical Activity Level (0-100)",
            min_value=0,
            max_value=100,
            value=50
        )

    st.markdown("---")
    st.subheader("Mental Health Indicators")
    col5, col6 = st.columns(2)

    with col5:
        anxiety = st.checkbox("Have Anxiety")
        depression_hist = st.checkbox("History of Depression")

    with col6:
        suicidal_thoughts = st.checkbox("Ever had Suicidal Thoughts")
        seeking_help = st.checkbox("Currently Seeking Help")

    st.markdown("---")
    submitted = st.form_submit_button(
        "🔍 Analyse My Risk",
        use_container_width=True
    )

# ── RESULTS ──────────────────────────────────────────
if submitted:
    score, risk_level, factors = calculate_risk(
        sleep_hours=sleep_hours,
        stress_level=stress_level,
        sleep_quality=sleep_quality,
        work_study_hours=work_study_hours,
        physical_activity=physical_activity
    )

    # Add extra score for mental health indicators
    if anxiety:         score += 2
    if depression_hist: score += 2
    if suicidal_thoughts: score += 3
    if family_history == "Yes": score += 1
    if dietary_habits == "Unhealthy": score += 1

    # Recalculate risk level with updated score
    if score >= 8:
        risk_level = "High"
    elif score >= 4:
        risk_level = "Medium"
    else:
        risk_level = "Low"

    st.markdown("---")
    st.subheader(f"Results for {name if name else 'You'}")

    # ── RISK LEVEL DISPLAY ────────────────────────────
    col1, col2, col3 = st.columns(3)

    with col1:
        if risk_level == "High":
            st.error(f"⚠️ Risk Level: **HIGH**")
        elif risk_level == "Medium":
            st.warning(f"🟠 Risk Level: **MEDIUM**")
        else:
            st.success(f"✅ Risk Level: **LOW**")

    with col2:
        st.metric("Total Score", f"{score} pts")

    with col3:
        st.metric("Sleep Hours", f"{sleep_hours}h")

    st.markdown("---")

    # ── FACTORS ──────────────────────────────────────
    st.subheader("📋 Your Risk Factors Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Contributing Factors:**")
        for factor in factors:
            st.write(factor)

        if anxiety:
            st.write("🔴 Anxiety present — adds to risk")
        if depression_hist:
            st.write("🔴 History of depression — adds to risk")
        if suicidal_thoughts:
            st.write("🔴 Suicidal thoughts history — high risk indicator")
        if family_history == "Yes":
            st.write("🟠 Family history of mental illness")
        if dietary_habits == "Unhealthy":
            st.write("🟠 Unhealthy dietary habits")

    with col2:
        st.markdown("**What you should do:**")

        if risk_level == "High":
            st.error("""
            - Please consult a mental health professional
            - Talk to someone you trust immediately
            - Reduce work/study hours if possible
            - Prioritise sleep above everything
            """)
        elif risk_level == "Medium":
            st.warning("""
            - Consider talking to a counsellor
            - Try to improve sleep schedule
            - Add physical activity to daily routine
            - Practice stress management techniques
            """)
        else:
            st.success("""
            - You are doing well — keep it up!
            - Maintain your sleep schedule
            - Stay physically active
            - Keep stress levels in check
            """)

    st.markdown("---")

    # ── SAVE TO SESSION STATE ─────────────────────────
    st.session_state['individual_result'] = {
        'name': name,
        'age': age,
        'category': category,
        'score': score,
        'risk_level': risk_level,
        'sleep_hours': sleep_hours,
        'stress_level': stress_level,
        'sleep_quality': sleep_quality,
        'work_study_hours': work_study_hours,
        'physical_activity': physical_activity
    }

    st.info("💡 Go to the **Predict** page to see what the ML model predicts for you!")