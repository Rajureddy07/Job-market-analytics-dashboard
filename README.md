# Job Market Analytics Dashboard

[![Python syntax](https://github.com/Rajureddy07/Job-market-analytics-dashboard/actions/workflows/syntax.yml/badge.svg)](https://github.com/Rajureddy07/Job-market-analytics-dashboard/actions/workflows/syntax.yml)

An interactive analytics application for exploring job-market data across roles, salaries, skills, industries, experience levels, countries, and hiring trends.

> **Project type:** Portfolio / analytics project. Results depend on the dataset you load and should not be treated as live labor-market forecasts.

## Features

- Filter job records by country, experience level, and industry.
- Explore salary distributions and role-level compensation patterns.
- Compare selected technical-skill demand fields.
- Review hiring trends and industry distribution.
- Download the filtered records as CSV.
- Use PostgreSQL for persistence and Streamlit + Plotly for interactive visualizations.

## Technology

Python · PostgreSQL · SQL · Pandas · Streamlit · Plotly · SQLAlchemy · Git

## Architecture

```text
.
├── Home.py                      # Main dashboard
├── database.py                  # Shared, environment-based DB access
├── import_data.py               # Load a CSV dataset to PostgreSQL
├── pages/
│   ├── 1_Salary_Insights.py
│   ├── 2_Skills_Insights.py
│   ├── 3_Hiring_Trends.py
│   └── 4_AI_Career_Advisor.py
├── requirements.txt
└── .env.example
```

## Run locally

### 1. Prerequisites

Install Python 3.10+ and PostgreSQL.

### 2. Clone and create a virtual environment

```bash
git clone https://github.com/Rajureddy07/Job-market-analytics-dashboard.git
cd Job-market-analytics-dashboard
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and replace the placeholders.

**Windows PowerShell**
```powershell
Copy-Item .env.example .env
```

Create a PostgreSQL database matching `DB_NAME` (default: `job_market_db`). The dashboard expects a table named `jobs` whose columns match the imported dataset. Do not commit your real `.env` file.

### 4. Import your dataset

Set `DATASET_PATH` in `.env` to the full path of your job-market CSV, then run:

```bash
python import_data.py
```

The importer appends records to the `jobs` table. Avoid repeatedly importing the same file unless duplicate records are intended. Ensure your dataset includes the fields used by the dashboard, including job title, salary, country, experience level, industry, job openings, skill flags, and posting-period fields where applicable.

### 5. Launch

```bash
streamlit run Home.py
```

Streamlit prints the local URL when the application starts.

## Configuration

The app reads these environment variables:

| Variable | Default | Purpose |
| --- | --- | --- |
| `DB_HOST` | `localhost` | PostgreSQL host |
| `DB_PORT` | `5432` | PostgreSQL port |
| `DB_NAME` | `job_market_db` | Database name |
| `DB_USER` | `postgres` | Database user |
| `DB_PASSWORD` | required | Local database password |
| `DATASET_PATH` | required for import | Source CSV path |

## Engineering notes

- Database configuration is centralized in `database.py`.
- Database credentials belong in local environment variables, not source files.
- Use synthetic or appropriately licensed datasets and document their origin before sharing.
- Salary values, currency, date coverage, and the dataset's representativeness should be verified before drawing real-world conclusions.

## Author

G. Rajasekhar Reddy · [GitHub](https://github.com/Rajureddy07)
