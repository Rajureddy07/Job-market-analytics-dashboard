import pandas as pd
import streamlit as st
import plotly.express as px

from database import load_jobs, show_database_error

st.set_page_config(page_title="Skills Insights", page_icon="🧠", layout="wide")
st.title("Skills Insights")

try:
    df = load_jobs()
except Exception as exc:
    show_database_error(exc)
    st.stop()

if df.empty:
    st.info("No data is available yet.")
    st.stop()

skill_columns = {
    "Python": "skills_python",
    "SQL": "skills_sql",
    "Machine Learning": "skills_ml",
    "Deep Learning": "skills_deep_learning",
    "Cloud": "skills_cloud",
}
skills = {
    skill: df[column].fillna(0).sum()
    for skill, column in skill_columns.items()
    if column in df.columns
}
skills_df = pd.DataFrame(list(skills.items()), columns=["Skill", "Demand"])

fig = px.bar(
    skills_df,
    x="Skill",
    y="Demand",
    title="Skill Demand in the Selected Dataset",
)
st.plotly_chart(fig, use_container_width=True)
