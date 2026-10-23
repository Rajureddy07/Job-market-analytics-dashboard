"""Import a job-market CSV into PostgreSQL.

Usage:
    Set DATASET_PATH and database credentials in .env, then run:
    python import_data.py
"""

import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

load_dotenv()


def main() -> None:
    dataset_path = os.getenv("DATASET_PATH")
    if not dataset_path:
        raise SystemExit(
            "Set DATASET_PATH in .env to the location of your job-market CSV."
        )

    csv_path = Path(dataset_path).expanduser()
    if not csv_path.is_file():
        raise SystemExit(f"Dataset file not found: {csv_path}")

    password = os.getenv("DB_PASSWORD")
    if not password:
        raise SystemExit("Set DB_PASSWORD in your local .env file.")

    df = pd.read_csv(csv_path)
    if df.empty:
        raise SystemExit("The selected CSV has no rows; nothing to import.")

    database_url = URL.create(
        drivername="postgresql+psycopg2",
        username=os.getenv("DB_USER", "postgres"),
        password=password,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME", "job_market_db"),
    )

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        df.to_sql("jobs", engine, if_exists="append", index=False, chunksize=1000)
    finally:
        engine.dispose()

    print(f"Imported {len(df):,} rows into the jobs table.")


if __name__ == "__main__":
    main()
