import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent folder to path so we can import utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocess import load_and_clean_data

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)

# ── LOAD DATA ────────────────────────────────────────
@st.cache_data
def load_data():
    return load_and_clean_data()

df = load_data()

# ── TITLE ────────────────────────────────────────────
st.title("📊 Population Overview")
st.markdown("Key mental health statistics across all groups")
st.markdown("---")

# ── METRIC CARDS ─────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Records",
        value=len(df)
    )

with col2:
    high_risk = round(
        df[df['risk_level'] == 'High'].shape[0] / len(df) * 100, 1
    )
    st.metric(
        label="High Risk %",
        value=f"{high_risk}%"
    )

with col3:
    avg_sleep = round(df['sleep_hours'].mean(), 1)
    st.metric(
        label="Avg Sleep Hours",
        value=f"{avg_sleep}h"
    )

with col4:
    avg_stress = round(df['stress_level'].mean(), 1)
    st.metric(
        label="Avg Stress Level",
        value=f"{avg_stress}/10"
    )

st.markdown("---")

# ── ROW 1 CHARTS ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Level Distribution")
    risk_counts = df['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['Risk Level', 'Count']
    fig = px.bar(
        risk_counts,
        x='Risk Level',
        y='Count',
        color='Risk Level',
        color_discrete_map={
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Category Breakdown")
    cat_counts = df['category'].value_counts().reset_index()
    cat_counts.columns = ['Category', 'Count']
    fig2 = px.pie(
        cat_counts,
        names='Category',
        values='Count',
        color_discrete_sequence=['#6366F1', '#F59E0B']
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── ROW 2 CHARTS ─────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sleep Hours Distribution")
    fig3 = px.histogram(
        df,
        x='sleep_hours',
        color='risk_level',
        color_discrete_map={
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444'
        },
        barmode='overlay',
        nbins=20
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Stress Level Distribution")
    fig4 = px.histogram(
        df,
        x='stress_level',
        color='risk_level',
        color_discrete_map={
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444'
        },
        barmode='overlay',
        nbins=10
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── AGE GROUP CHART ───────────────────────────────────
st.subheader("Risk Level by Age Group")
age_risk = df.groupby(['age_group', 'risk_level']).size().reset_index(name='count')
fig5 = px.bar(
    age_risk,
    x='age_group',
    y='count',
    color='risk_level',
    barmode='group',
    color_discrete_map={
        'Low': '#10B981',
        'Medium': '#F59E0B',
        'High': '#EF4444'
    }
)
st.plotly_chart(fig5, use_container_width=True)

# ── RAW DATA ─────────────────────────────────────────
st.markdown("---")
with st.expander("See Raw Data"):
    st.dataframe(df)
