
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
CLEANED_PATH = BASE_DIR / "outputs" / "cleaned_superstore.csv"
DB_PATH = BASE_DIR / "database" / "retailpulse.db"


def create_database():
    """Load cleaned retail data into a SQLite database."""

    if not CLEANED_PATH.exists():
        raise FileNotFoundError(
            f"Cleaned data not found: {CLEANED_PATH}. "
            "Run data_cleaning.py first."
        )

    # Ensure database folder exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Read cleaned CSV
    df = pd.read_csv(CLEANED_PATH, encoding="utf-8-sig")

    # Create or replace the transactions table
    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "transactions",
            conn,
            if_exists="replace",
            index=False
        )

        # Create useful SQL views
        conn.executescript("""
            DROP VIEW IF EXISTS monthly_performance;

            CREATE VIEW monthly_performance AS
            SELECT
                Month,
                SUM(Sales) AS Total_Sales,
                SUM(Profit) AS Total_Profit,
                ROUND(
                    100.0 * SUM(Profit) /
                    NULLIF(SUM(Sales), 0), 2
                ) AS Profit_Margin_Percent
            FROM transactions
            GROUP BY Month;

            DROP VIEW IF EXISTS category_performance;

            CREATE VIEW category_performance AS
            SELECT
                Category,
                SUM(Sales) AS Total_Sales,
                SUM(Profit) AS Total_Profit,
                ROUND(
                    100.0 * SUM(Profit) /
                    NULLIF(SUM(Sales), 0), 2
                ) AS Profit_Margin_Percent
            FROM transactions
            GROUP BY Category;

            DROP VIEW IF EXISTS regional_performance;

            CREATE VIEW regional_performance AS
            SELECT
                Region,
                SUM(Sales) AS Total_Sales,
                SUM(Profit) AS Total_Profit
            FROM transactions
            GROUP BY Region;
        """)

    print("DATABASE CREATED SUCCESSFULLY")
    print(f"Rows loaded: {len(df):,}")
    print(f"Database location: {DB_PATH}")


if __name__ == "__main__":
    create_database()
