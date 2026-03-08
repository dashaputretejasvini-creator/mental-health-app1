import streamlit as st
import plotly.express as px
import pandas as pd
import sys
import os

# Add parent folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.preprocess import load_and_clean_data

# ── PAGE CONFIG ──────────────────────────────────────
st.set_page_config(
    page_title="Group Analysis",
    page_icon="👥",
    layout="wide"
)

# ── LOAD DATA ────────────────────────────────────────
@st.cache_data
def load_data():
    return load_and_clean_data()

df = load_data()

# ── TITLE ────────────────────────────────────────────
st.title("👥 Group Analysis")
st.markdown("Analyse mental health patterns by age group and category")
st.markdown("---")

# ── SIDEBAR FILTERS ──────────────────────────────────
st.sidebar.title("🔍 Filters")

category = st.sidebar.selectbox(
    "Select Category",
    ["All", "Student", "Worker"]
)

age_groups = st.sidebar.multiselect(
    "Select Age Groups",
    options=df['age_group'].dropna().unique().tolist(),
    default=df['age_group'].dropna().unique().tolist()
)

# ── APPLY FILTERS ────────────────────────────────────
filtered = df.copy()

if category != "All":
    filtered = filtered[filtered['category'] == category]

if age_groups:
    filtered = filtered[filtered['age_group'].isin(age_groups)]

# ── METRIC CARDS ─────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total in Group", len(filtered))

with col2:
    high = round(
        filtered[filtered['risk_level'] == 'High'].shape[0] / len(filtered) * 100, 1
    ) if len(filtered) > 0 else 0
    st.metric("High Risk %", f"{high}%")

with col3:
    avg_sleep = round(filtered['sleep_hours'].mean(), 1) if len(filtered) > 0 else 0
    st.metric("Avg Sleep Hours", f"{avg_sleep}h")

st.markdown("---")

# ── ROW 1 ────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Level by Category")
    cat_risk = filtered.groupby(
        ['category', 'risk_level']
    ).size().reset_index(name='count')
    fig = px.bar(
        cat_risk,
        x='category',
        y='count',
        color='risk_level',
        barmode='group',
        color_discrete_map={
            'Low': '#10B981',
            'Medium': '#F59E0B',
            'High': '#EF4444'
        }
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Average Stress by Age Group")
    stress_age = filtered.groupby(
        'age_group'
    )['stress_level'].mean().reset_index()
    stress_age.columns = ['Age Group', 'Avg Stress']
    fig2 = px.bar(
        stress_age,
        x='Age Group',
        y='Avg Stress',
        color='Avg Stress',
        color_continuous_scale='RdYlGn_r'
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── ROW 2 ────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sleep Hours by Category")
    fig3 = px.box(
        filtered,
        x='category',
        y='sleep_hours',
        color='category',
        color_discrete_sequence=['#6366F1', '#F59E0B']
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Sleep Hours by Age Group")
    fig4 = px.box(
        filtered,
        x='age_group',
        y='sleep_hours',
        color='age_group'
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ── HEATMAP ───────────────────────────────────────────
st.subheader("Heatmap — Age Group vs Risk Level")
heat = filtered.groupby(
    ['age_group', 'risk_level']
).size().reset_index(name='count')

pivot = heat.pivot(
    index='age_group',
    columns='risk_level',
    values='count'
).fillna(0)

fig5 = px.imshow(
    pivot,
    color_continuous_scale='RdYlGn_r',
    title='Number of people per Age Group and Risk Level'
)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")

# ── INSIGHT TEXT ──────────────────────────────────────
st.subheader("📌 Key Insights")

if len(filtered) > 0:
    most_stressed_group = filtered.groupby(
        'age_group'
    )['stress_level'].mean().idxmax()

    lowest_sleep_group = filtered.groupby(
        'age_group'
    )['sleep_hours'].mean().idxmin()

    highest_risk_cat = filtered.groupby(
        'category'
    )['depression'].mean().idxmax()

    st.info(
        f"📍 **Most stressed age group:** {most_stressed_group}"
    )
    st.info(
        f"😴 **Least sleep age group:** {lowest_sleep_group}"
    )
    st.info(
        f"⚠️ **Highest depression rate category:** {highest_risk_cat}"
    )
