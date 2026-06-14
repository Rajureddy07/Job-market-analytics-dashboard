import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

connection = psycopg2.connect(
    host="localhost",
    database="job_market_db",
    user="postgres",
    password="DB_Password" #u r DB password
)

df = pd.read_sql(
    "SELECT * FROM jobs",
    connection
)

skills = {
    "Python": df["skills_python"].sum(),
    "SQL": df["skills_sql"].sum(),
    "ML": df["skills_ml"].sum(),
    "Deep Learning": df["skills_deep_learning"].sum(),
    "Cloud": df["skills_cloud"].sum()
}

skills_df = pd.DataFrame(
    list(skills.items()),
    columns=["Skill", "Demand"]
)

fig = px.bar(
    skills_df,
    x="Skill",
    y="Demand",
    title="Skill Demand"
)

st.plotly_chart(fig)