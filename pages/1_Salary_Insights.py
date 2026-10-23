import streamlit as st
import plotly.express as px

from database import load_jobs, show_database_error

st.set_page_config(page_title="Salary Insights", page_icon="💰", layout="wide")
st.title("Salary Insights")

try:
    df = load_jobs()
except Exception as exc:
    show_database_error(exc)
    st.stop()

if df.empty:
    st.info("No data is available yet.")
    st.stop()

salary_role = (
    df.groupby("job_title", dropna=True)["salary"]
    .mean()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig = px.bar(
    salary_role,
    x="salary",
    y="job_title",
    orientation="h",
    title="Highest-Paying Roles by Average Listed Salary",
    labels={"salary": "Average salary", "job_title": "Job role"},
)
st.plotly_chart(fig, use_container_width=True)
st.caption("Salary patterns reflect the source dataset and are not a guarantee of market compensation.")
