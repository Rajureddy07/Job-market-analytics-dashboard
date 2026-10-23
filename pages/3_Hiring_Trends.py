import streamlit as st
import plotly.express as px

from database import load_jobs, show_database_error

st.set_page_config(page_title="Hiring Trends", page_icon="📈", layout="wide")
st.title("Hiring Trends")

try:
    df = load_jobs()
except Exception as exc:
    show_database_error(exc)
    st.stop()

if df.empty:
    st.info("No data is available yet.")
    st.stop()

if "job_posting_month" in df.columns:
    trend = (
        df.groupby("job_posting_month", dropna=True)
        .size()
        .reset_index(name="Job Records")
        .sort_values("job_posting_month")
    )
elif "job_posting_year" in df.columns:
    trend = (
        df.groupby("job_posting_year", dropna=True)
        .size()
        .reset_index(name="Job Records")
        .sort_values("job_posting_year")
    )
else:
    st.warning("The dataset needs a job_posting_month or job_posting_year column for trend analysis.")
    st.stop()

fig = px.line(
    trend,
    x=trend.columns[0],
    y="Job Records",
    markers=True,
    title="Job Postings Over Time",
)
st.plotly_chart(fig, use_container_width=True)
