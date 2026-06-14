import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

connection = psycopg2.connect(
    host="localhost",
    database="job_market_db",
    user="postgres",
    password="DB_password" #U r password
)

df = pd.read_sql(
    "SELECT * FROM jobs",
    connection
)

trend = (
    df.groupby("job_posting_year")
    .size()
    .reset_index(name="Jobs")
)

fig = px.line(
    trend,
    x="job_posting_year",
    y="Jobs",
    markers=True
)

st.plotly_chart(fig)