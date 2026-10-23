"""Database access helpers for the Job Market Analytics dashboard."""

import os
from contextlib import closing

import pandas as pd
import psycopg2
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def load_jobs() -> pd.DataFrame:
    """Load job records from PostgreSQL and always close the connection."""
    password = os.getenv("DB_PASSWORD")
    if not password:
        raise RuntimeError(
            "DB_PASSWORD is missing. Create a local .env file from .env.example."
        )

    settings = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "database": os.getenv("DB_NAME", "job_market_db"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": password,
        "connect_timeout": 5,
    }

    with closing(psycopg2.connect(**settings)) as connection:
        return pd.read_sql_query("SELECT * FROM jobs", connection)


def show_database_error(error: Exception) -> None:
    """Show a useful but non-secret database configuration message."""
    st.error(
        "Could not load job-market data. Verify PostgreSQL is running, the "
        "credentials in your local .env file are correct, and the jobs table exists."
    )
    st.caption(f"Details: {type(error).__name__}: {error}")
