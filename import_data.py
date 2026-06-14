import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv(r"C:\Users\reddy\Downloads\AI Job Market Dataset.csv")

# PostgreSQL Connection
engine = create_engine(
    "postgresql://postgres:123raju@localhost/job_market_db"
)

# Upload Data
df.to_sql(
    "jobs",
    engine,
    if_exists="append",
    index=False
)

print("Data Imported Successfully!")