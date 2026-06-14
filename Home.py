import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# DATABASE CONNECTION

connection = psycopg2.connect(
    host="localhost",
    database="job_market_db",
    user="postgres",
    password="DB_Password"  #Replace with your database password
)

# LOAD DATA FROM POSTGRESQL

query = "SELECT * FROM jobs"
df = pd.read_sql(query, connection)

# SIDEBAR FILTERS

st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(df["country"].unique().tolist())
)

experience = st.sidebar.selectbox(
    "Experience Level",
    ["All"] + sorted(df["experience_level"].unique().tolist())
)

industry = st.sidebar.selectbox(
    "Industry",
    ["All"] + sorted(df["company_industry"].unique().tolist())
)

# APPLY FILTERS

filtered_df = df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == country
    ]

if experience != "All":
    filtered_df = filtered_df[
        filtered_df["experience_level"] == experience
    ]

if industry != "All":
    filtered_df = filtered_df[
        filtered_df["company_industry"] == industry
    ]

# Handle empty results

if filtered_df.empty:
    st.warning(" No records found for selected filters.")
    st.stop()

# DASHBOARD HEADER

st.title(" Job Market Analytics Dashboard")

st.caption(
    "Analyze global AI & Data Science hiring trends, salaries, skills demand, and recruitment patterns."
)

# KPI CARDS

total_jobs = len(filtered_df)

avg_salary = round(
    filtered_df["salary"].mean(),
    2
)

total_openings = (
    filtered_df["job_openings"]
    .sum()
)

countries = (
    filtered_df["country"]
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Jobs",
    f"{total_jobs:,}"
)

col2.metric(
    "Average Salary",
    f"${avg_salary:,.0f}"
)

col3.metric(
    "Total Openings",
    f"{total_openings:,}"
)

col4.metric(
    "Countries",
    f"{countries:,}"
)

# TOP JOB ROLES

st.header(" Top Job Roles")

top_jobs = (
    filtered_df["job_title"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_jobs.columns = [
    "Job Title",
    "Count"
]

fig_roles = px.bar(
    top_jobs,
    x="Job Title",
    y="Count",
    title="Top 10 Job Roles"
)

st.plotly_chart(
    fig_roles,
    use_container_width=True
)

# SALARY DISTRIBUTION

st.header(" Salary Distribution")

fig_salary_dist = px.histogram(
    filtered_df,
    x="salary",
    nbins=30,
    title="Salary Distribution"
)

st.plotly_chart(
    fig_salary_dist,
    use_container_width=True
)

# KEY INSIGHTS

st.header(" Key Insights")

highest_role = (
    filtered_df.groupby("job_title")["salary"]
    .mean()
    .idxmax()
)

highest_salary = (
    filtered_df.groupby("job_title")["salary"]
    .mean()
    .max()
)

most_demanded_role = (
    filtered_df["job_title"]
    .value_counts()
    .idxmax()
)

st.success(
    f" Highest Paying Role: {highest_role} (${highest_salary:,.0f})"
)

st.info(
    f" Most Demanded Role: {most_demanded_role}"
)

st.warning(
    f" Countries Hiring: {filtered_df['country'].nunique()}"
)

# SALARY ANALYSIS

st.header("Salary Analysis")

salary_by_role = (
    filtered_df.groupby("job_title")["salary"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_salary = px.bar(
    salary_by_role,
    x="job_title",
    y="salary",
    title="Top 10 Highest Paying Job Roles"
)

st.plotly_chart(
    fig_salary,
    use_container_width=True
)

# SKILLS DEMAND ANALYSIS

st.header("Skills Demand Analysis")

skills = {
    "Python": filtered_df["skills_python"].sum(),
    "SQL": filtered_df["skills_sql"].sum(),
    "Machine Learning": filtered_df["skills_ml"].sum(),
    "Deep Learning": filtered_df["skills_deep_learning"].sum(),
    "Cloud": filtered_df["skills_cloud"].sum()
}

skills_df = pd.DataFrame(
    list(skills.items()),
    columns=["Skill", "Demand"]
)

fig_skills = px.bar(
    skills_df,
    x="Skill",
    y="Demand",
    title="Most Demanded Skills"
)

st.plotly_chart(
    fig_skills,
    use_container_width=True
)

# REMOTE WORK ANALYSIS

st.header(" Remote Work Analysis")

remote_df = (
    filtered_df["remote_type"]
    .value_counts()
    .reset_index()
)

remote_df.columns = [
    "Remote Type",
    "Count"
]

fig_remote = px.pie(
    remote_df,
    names="Remote Type",
    values="Count",
    title="Remote vs Hybrid vs On-Site Jobs"
)

st.plotly_chart(
    fig_remote,
    use_container_width=True
)

# INDUSTRY ANALYSIS

st.header(" Industry Analysis")

industry_df = (
    filtered_df.groupby("company_industry")
    .size()
    .sort_values(ascending=False)
    .head(10)
    .reset_index(name="Jobs")
)

fig_industry = px.bar(
    industry_df,
    x="company_industry",
    y="Jobs",
    title="Top Industries Hiring"
)

st.plotly_chart(
    fig_industry,
    use_container_width=True
)

# HIRING URGENCY

st.header(" Hiring Urgency")

urgency_df = (
    filtered_df["hiring_urgency"]
    .value_counts()
    .reset_index()
)

urgency_df.columns = [
    "Urgency",
    "Count"
]

fig_urgency = px.pie(
    urgency_df,
    names="Urgency",
    values="Count",
    title="Hiring Urgency Distribution"
)

st.plotly_chart(
    fig_urgency,
    use_container_width=True
)

# SALARY VS EXPERIENCE

st.header(" Salary vs Experience")

exp_salary = (
    filtered_df.groupby("experience_level")
    ["salary"]
    .mean()
    .reset_index()
)

fig_exp = px.bar(
    exp_salary,
    x="experience_level",
    y="salary",
    title="Average Salary by Experience Level"
)

st.plotly_chart(
    fig_exp,
    use_container_width=True
)

# TOP PAYING COUNTRIES

st.header(" Top Paying Countries")

country_salary = (
    filtered_df.groupby("country")
    ["salary"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_country = px.bar(
    country_salary,
    x="country",
    y="salary",
    title="Top Paying Countries"
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

# HIRING TRENDS

st.header("Hiring Trends")

trend = (
    filtered_df.groupby("job_posting_month")
    .size()
    .reset_index(name="Jobs")
    .sort_values("job_posting_month")
)

fig_trend = px.line(
    trend,
    x="job_posting_month",
    y="Jobs",
    markers=True,
    title="Jobs Posted Per Month"
)

st.plotly_chart(
    fig_trend,
    use_container_width=True
)

# DOWNLOAD FILTERED DATA

csv = filtered_df.to_csv(index=False)

st.download_button(
    label=" Download Filtered Data",
    data=csv,
    file_name="job_market_report.csv",
    mime="text/csv"
)