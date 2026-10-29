
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "retailpulse.db"
OUTPUT_DIR = BASE_DIR / "outputs"


def run_analysis():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            "Database not found. Run python -m src.database first."
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:

        # 1. Overall business performance
        overall = pd.read_sql_query("""
            SELECT
                COUNT(*) AS Transaction_Lines,
                ROUND(SUM(Sales), 2) AS Total_Sales,
                ROUND(SUM(Profit), 2) AS Total_Profit,
                ROUND(
                    100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2
                ) AS Profit_Margin_Percent
            FROM transactions
        """, conn)

        # 2. Products losing money
        loss_products = pd.read_sql_query("""
            SELECT
                "Sub-Category" AS Subcategory,
                ROUND(SUM(Sales), 2) AS Sales,
                ROUND(SUM(Profit), 2) AS Profit,
                ROUND(
                    100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2
                ) AS Margin_Percent
            FROM transactions
            GROUP BY "Sub-Category"
            HAVING SUM(Profit) < 0
            ORDER BY SUM(Profit) ASC
        """, conn)

        # 3. Regional performance
        regions = pd.read_sql_query("""
            SELECT
                Region,
                ROUND(SUM(Sales), 2) AS Sales,
                ROUND(SUM(Profit), 2) AS Profit,
                ROUND(
                    100.0 * SUM(Profit) / NULLIF(SUM(Sales), 0), 2
                ) AS Margin_Percent
            FROM transactions
            GROUP BY Region
            ORDER BY Margin_Percent ASC
        """, conn)

        # 4. Discount and profitability relationship
        discounts = pd.read_sql_query("""
            SELECT
                "Discount Band" AS Discount_Band,
                COUNT(*) AS Transaction_Lines,
                ROUND(SUM(Sales), 2) AS Sales,
                ROUND(SUM(Profit), 2) AS Profit
            FROM transactions
            GROUP BY "Discount Band"
            ORDER BY
                CASE "Discount Band"
                    WHEN '0% - No Discount' THEN 1
                    WHEN '1-10%' THEN 2
                    WHEN '11-20%' THEN 3
                    WHEN '21-30%' THEN 4
                    WHEN 'Above 30%' THEN 5
                    ELSE 6
                END
        """, conn)

        # 5. Monthly performance
        monthly = pd.read_sql_query("""
            SELECT Month, Total_Sales, Total_Profit,
                   Profit_Margin_Percent
            FROM monthly_performance
            ORDER BY Month
        """, conn)

    # Export results for the app, Tableau, and Google Sheets
    reports = {
        "overall_kpis.csv": overall,
        "loss_products.csv": loss_products,
        "regional_performance.csv": regions,
        "discount_analysis.csv": discounts,
        "monthly_analysis.csv": monthly,
    }

    for filename, report in reports.items():
        report.to_csv(OUTPUT_DIR / filename, index=False)

    print("\n========== RETAILPULSE ANALYSIS ==========")
    print("\nOVERALL PERFORMANCE")
    print(overall.to_string(index=False))

    print("\nLOSS-MAKING SUBCATEGORIES")
    print(loss_products.to_string(index=False))

    print("\nREGIONAL PERFORMANCE")
    print(regions.to_string(index=False))

    print("\nDISCOUNT ANALYSIS")
    print(discounts.to_string(index=False))

    print(f"\nReports saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    run_analysis()
