import streamlit as st

st.title(" AI Career Advisor")

role = st.selectbox(
    "Choose Career",
    [
        "Data Scientist",
        "Data Analyst",
        "ML Engineer",
        "AI Engineer"
    ]
)

if role == "Data Scientist":
    st.success("""
    Learn:
    • Python
    • SQL
    • Machine Learning
    • Statistics
    • Pandas
    """)

elif role == "Data Analyst":
    st.success("""
    Learn:
    • SQL
    • Excel
    • Power BI
    • Python
    """)

elif role == "ML Engineer":
    st.success("""
    Learn:
    • Python
    • Machine Learning
    • Deep Learning
    • Cloud
    """)

elif role == "AI Engineer":
    st.success("""
    Learn:
    • Python
    • ML
    • Deep Learning
    • LLMs
    • Cloud
    """)