import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
import sys
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocess import load_and_clean_data

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="ML Prediction",
    page_icon="🤖",
    layout="wide"
)

# ── LOAD DATA ────────────────────────────────────────
@st.cache_data
def load_data():
    return load_and_clean_data()

# ── TRAIN AND SAVE MODEL ─────────────────────────────
@st.cache_resource
def train_model():
    df = load_data()

    # Features for training
    features = [
        'age', 'sleep_hours', 'sleep_quality',
        'stress_level', 'physical_activity', 'depression'
    ]

    X = df[features].copy()
    y = df['risk_level']

    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)

    # Train model
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=0.2,
        random_state=42
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight='balanced'
    )
    model.fit(X_train, y_train)

    # Accuracy
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    # Save model
    os.makedirs('models', exist_ok=True)
    with open('models/risk_model.pkl', 'wb') as f:
        pickle.dump((model, le), f)

    return model, le, accuracy, features

# ── TITLE ────────────────────────────────────────────
st.title("🤖 ML Risk Prediction")
st.markdown("Machine Learning model predicts your mental health risk level")
st.markdown("---")

# ── TRAIN MODEL ──────────────────────────────────────
with st.spinner("Training ML model... please wait"):
    model, le, accuracy, features = train_model()

st.success(f"✅ Model trained successfully! Accuracy: {round(accuracy * 100, 1)}%")
st.markdown("---")

# ── FEATURE IMPORTANCE ───────────────────────────────
st.subheader("📊 What Factors Drive Mental Health Risk?")
st.markdown("This chart shows which factors the ML model considers most important:")

importance_df = pd.DataFrame({
    'Feature': features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=True)

import plotly.express as px
fig = px.bar(
    importance_df,
    x='Importance',
    y='Feature',
    orientation='h',
    color='Importance',
    color_continuous_scale='RdYlGn_r',
    title='Feature Importance — What leads to mental health risk?'
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ── PREDICTION FORM ───────────────────────────────────
st.subheader("🔍 Predict Your Risk")

# Check if coming from Individual page
if 'individual_result' in st.session_state:
    prev = st.session_state['individual_result']
    st.info(f"📌 Using data from Individual page for **{prev['name']}**. You can change values below.")
    default_sleep = float(prev['sleep_hours'])
    default_stress = int(prev['stress_level'])
    default_quality = int(prev['sleep_quality'])
    default_work = float(prev['work_study_hours'])
    default_activity = int(prev['physical_activity'])
else:
    default_sleep = 7.0
    default_stress = 5
    default_quality = 6
    default_work = 8.0
    default_activity = 50

with st.form("predict_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=10,
            max_value=80,
            value=25
        )
        sleep_hours = st.slider(
            "Sleep Hours per Night",
            min_value=2.0,
            max_value=12.0,
            value=default_sleep,
            step=0.5
        )
        sleep_quality = st.slider(
            "Sleep Quality (1-10)",
            min_value=1,
            max_value=10,
            value=default_quality
        )

    with col2:
        stress_level = st.slider(
            "Stress Level (1-10)",
            min_value=1,
            max_value=10,
            value=default_stress
        )
        physical_activity = st.slider(
            "Physical Activity (0-100)",
            min_value=0,
            max_value=100,
            value=default_activity
        )
        depression = st.selectbox(
            "Do you have depression?",
            ["No", "Yes"]
        )

    submitted = st.form_submit_button(
        "🤖 Predict My Risk",
        use_container_width=True
    )

# ── PREDICTION RESULT ────────────────────────────────
if submitted:
    depression_val = 1 if depression == "Yes" else 0

    input_data = pd.DataFrame([{
        'age': age,
        'sleep_hours': sleep_hours,
        'sleep_quality': sleep_quality,
        'stress_level': stress_level,
        'physical_activity': physical_activity,
        'depression': depression_val
    }])

    prediction_encoded = model.predict(input_data)[0]
    prediction = le.inverse_transform([prediction_encoded])[0]

    probability = model.predict_proba(input_data)[0]
    classes = le.inverse_transform(range(len(probability)))

    st.markdown("---")
    st.subheader("🎯 ML Prediction Result")

    col1, col2, col3 = st.columns(3)

    with col1:
        if prediction == "High":
            st.error(f"⚠️ ML Predicted Risk: **HIGH**")
        elif prediction == "Medium":
            st.warning(f"🟠 ML Predicted Risk: **MEDIUM**")
        else:
            st.success(f"✅ ML Predicted Risk: **LOW**")

    with col2:
        st.metric("Model Accuracy", f"{round(accuracy * 100, 1)}%")

    with col3:
        st.metric("Sleep Hours", f"{sleep_hours}h")

    st.markdown("---")

    # ── PROBABILITY CHART ─────────────────────────────
    st.subheader("📊 Risk Probability Breakdown")
    prob_df = pd.DataFrame({
        'Risk Level': classes,
        'Probability %': [round(p * 100, 1) for p in probability]
    })

    fig2 = px.bar(
        prob_df,
        x='Risk Level',
        y='Probability %',
        color='Risk Level',
        color_discrete_map={
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444'
        }
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")

    # ── RECOMMENDATION ────────────────────────────────
    st.subheader("💡 Recommendation")

    if prediction == "High":
        st.error("""
        The ML model has detected **HIGH** mental health risk.
        - Please consult a mental health professional immediately
        - Prioritise sleep — aim for at least 7-8 hours
        - Reduce stress through meditation or exercise
        - Talk to someone you trust about how you feel
        """)
    elif prediction == "Medium":
        st.warning("""
        The ML model has detected **MEDIUM** mental health risk.
        - Consider speaking to a counsellor
        - Improve your sleep schedule
        - Add 30 minutes of physical activity daily
        - Try journaling or mindfulness techniques
        """)
    else:
        st.success("""
        The ML model shows **LOW** mental health risk.
        - You are in good mental health — keep it up!
        - Maintain your current sleep and activity habits
        - Stay connected with friends and family
        - Regular exercise keeps stress levels low
        """)

    # ── DOWNLOAD REPORT ───────────────────────────────
    st.markdown("---")
    report_df = pd.DataFrame([{
        'Age': age,
        'Sleep Hours': sleep_hours,
        'Sleep Quality': sleep_quality,
        'Stress Level': stress_level,
        'Physical Activity': physical_activity,
        'Depression': depression,
        'ML Predicted Risk': prediction,
        'Model Accuracy': f"{round(accuracy * 100, 1)}%"
    }])

    csv = report_df.to_csv(index=False)
    st.download_button(
        label="📥 Download My Risk Report",
        data=csv,
        file_name="mental_health_risk_report.csv",
        mime="text/csv",
        use_container_width=True
    )
