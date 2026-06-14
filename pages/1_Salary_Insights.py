# pages/1_Salary_Insights.py

import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

connection = psycopg2.connect(
    host="localhost",
    database="job_market_db",
    user="postgres",
    password="123raju"
)

df = pd.read_sql(
    "SELECT * FROM jobs",
    connection
)

st.title("Salary Insights")

salary_role = (
    df.groupby("job_title")["salary"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    salary_role,
    x="job_title",
    y="salary",
    title="Highest Paying Roles"
)

st.plotly_chart(fig)