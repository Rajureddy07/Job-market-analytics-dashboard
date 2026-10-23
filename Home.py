import streamlit as st
import pandas as pd
import plotly.express as px

from database import load_jobs, show_database_error

st.set_page_config(
    page_title="Job Market Analytics",
    page_icon="📈",
    layout="wide",
)

try:
    df = load_jobs()
except Exception as exc:
    show_database_error(exc)
    st.stop()

if df.empty:
    st.warning("No job records were found in the jobs table. Import the dataset first.")
    st.stop()

# SIDEBAR FILTERS

st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["country"].dropna().unique().tolist())
)

experience = st.sidebar.selectbox(
    "Experience Level",
    ["All"] + sorted(df["experience_level"].dropna().unique().tolist())
)

industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + sorted(df["company_industry"].dropna().unique().tolist())
)

# APPLY FILTERS

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[filtered_df["country"] == country]

if experience != "All":
    filtered_df = filtered_df[filtered_df["experience_level"] == experience]

if industry != "All":
    filtered_df = filtered_df[filtered_df["company_industry"] == industry]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

st.title("Job Market Analytics Dashboard")
st.caption(
    "Explore salary patterns, job demand, skills, hiring activity, and work arrangements."
)

total_jobs = len(filtered_df)
avg_salary = filtered_df["salary"].mean()
total_openings = filtered_df["job_openings"].sum()
countries = filtered_df["country"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Job Records", f"{total_jobs:,}")
col2.metric("Average Salary", f"${avg_salary:,.0f}" if pd.notna(avg_salary) else "N/A")
col3.metric("Listed Openings", f"{total_openings:,.0f}")
col4.metric("Countries", f"{countries:,}")

st.subheader("Top job roles")
top_jobs = filtered_df["job_title"].value_counts().head(10).rename_axis("Job Title").reset_index(name="Records")
st.plotly_chart(
    px.bar(top_jobs, x="Records", y="Job Title", orientation="h", title="Most Frequent Roles"),
    use_container_width=True,
)

left, right = st.columns(2)
with left:
    st.subheader("Salary distribution")
    st.plotly_chart(
        px.histogram(filtered_df, x="salary", nbins=30, title="Salary Distribution"),
        use_container_width=True,
    )
with right:
    st.subheader("Skills demand")
    skill_columns = {
        "Python": "skills_python",
        "SQL": "skills_sql",
        "Machine Learning": "skills_ml",
        "Deep Learning": "skills_deep_learning",
        "Cloud": "skills_cloud",
    }
    available_skills = {
        label: filtered_df[column].fillna(0).sum()
        for label, column in skill_columns.items()
        if column in filtered_df.columns
    }
    skills_df = pd.DataFrame(list(available_skills.items()), columns=["Skill", "Demand"])
    st.plotly_chart(
        px.bar(skills_df, x="Skill", y="Demand", title="Recorded Skill Demand"),
        use_container_width=True,
    )

st.subheader("Hiring by industry")
if "company_industry" in filtered_df.columns:
    industry_df = filtered_df["company_industry"].value_counts().head(10).rename_axis("Industry").reset_index(name="Records")
    st.plotly_chart(
        px.bar(industry_df, x="Records", y="Industry", orientation="h"),
        use_container_width=True,
    )

st.subheader("Filtered dataset")
st.dataframe(filtered_df, use_container_width=True)

st.download_button(
    label="Download filtered data",
    data=filtered_df.to_csv(index=False),
    file_name="job_market_report.csv",
    mime="text/csv",
)
