# RetailPulse --- Retail Performance & Profit Intelligence

RetailPulse is a retail analytics project that turns transaction-level
sales data into practical business insights. It combines a Python
data-cleaning pipeline, SQL-based analysis, a Streamlit dashboard,
Tableau visualizations, and a business action tracker.

> **Project dataset:** Sample Superstore\
> **Focus:** Sales performance, profitability, discount analysis,
> regional trends, and identifying potential profit leaks\
> **Approach:** Descriptive analytics and business rules --- no machine
> learning or LLM features

## Project Goals

-   Track core retail KPIs such as sales, profit, profit margin, and
    order count.
-   Identify loss-making product subcategories for further
    investigation.
-   Compare sales and profitability across categories, regions, discount
    bands, and months.
-   Explore a discount-reduction scenario through a what-if simulator.
-   Translate analytical findings into assigned, measurable business
    actions.

## Tech Stack

-   **Python** --- data cleaning and analysis
-   **Pandas** --- data preparation and tabular analysis
-   **SQLite** --- local analytical database
-   **SQL** --- KPI queries and performance views
-   **Streamlit** --- interactive dashboard
-   **Plotly** --- charts in the Streamlit app
-   **Tableau Public** --- business intelligence visualizations
-   **Google Sheets / Excel** --- business action tracking

## Project Structure

``` text
RetailPulse/
├── app.py
├── data/
│   └── Sample_Superstore.csv
├── database/
│   └── retailpulse.db
├── outputs/
│   ├── cleaned_superstore.csv
│   ├── overall_kpis.csv
│   ├── loss_products.csv
│   ├── regional_performance.csv
│   ├── discount_analysis.csv
│   └── monthly_analysis.csv
├── sql/
├── src/
│   ├── __init__.py
│   ├── data_cleaning.py
│   ├── database.py
│   └── analysis.py
├── requirements.txt
└── README.md
```

Generated database and output files may appear after running the
pipeline; they do not need to be committed if the project repository
uses generated-file exclusions.

## Features

### 1. Data cleaning

-   Loads the Sample Superstore CSV.
-   Cleans and prepares fields for analysis.
-   Derives month, year, profit margin, and discount-band fields.
-   Exports a cleaned dataset for downstream use.

### 2. SQL analytics

-   Loads the cleaned dataset into a local SQLite database.
-   Creates analytical views for monthly, category, and regional
    performance.
-   Exports KPI summaries, loss-making subcategories, regional results,
    discount analysis, and monthly analysis.

### 3. Streamlit dashboard

-   KPI summaries and interactive region/category filters.
-   Monthly performance trends.
-   Category and regional profitability views.
-   Profit leak detector for low-profit or loss-making subcategories.
-   Discount analysis and a what-if discount simulator.

**Simulator note:** Treat scenario outputs as estimates based on the
assumptions shown in the app, not as a guaranteed forecast. Document the
assumptions and validate them against actual business data before making
pricing decisions.

### 4. Tableau Public dashboard

The Tableau workbook is intended to present: - Category profitability -
Monthly sales and profit trends - Profit by subcategory to investigate
potential profit leaks - Regional performance

**Published dashboard:** [https://public.tableau.com/authoring/RetailPulseExecutiveDashboard_17932958426970/RetailPulseExecutiveOverview#1]

### 5. Business action tracker

The accompanying `RetailPulse_Business_Action_Tracker.xlsx` provides a
practical workflow for: - Recording issues and opportunities - Capturing
evidence to validate - Recommending actions - Assigning priority, owner,
and target date - Tracking status and success metrics - Recording actual
outcomes and notes

Recommendations should be treated as hypotheses until evidence confirms
the cause and results demonstrate an impact.

## Dataset Notes

This project uses the Sample Superstore dataset for demonstration and
portfolio purposes. The commonly used full dataset baseline is
approximately:

  Metric                             Reference value
  -------------------------------- -----------------
  Rows / records                               9,994
  Sales                               \$2,297,200.86
  Profit                                \$286,397.02
  Profit margin (profit ÷ sales)              12.47%
  Distinct orders                              5,009

Values in the dashboard may vary if filters are applied, data is
modified, or a different version of the dataset is used. Confirm the
current outputs before presenting figures.

## Setup and Run Locally

### 1. Clone or download the project

Open a terminal in the project root folder.

### 2. Create and activate a virtual environment

**Windows PowerShell:**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the appropriate activation command
for your terminal or run the environment's Python executable directly.

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the data pipeline in order

Run these commands from the project root:

``` bash
python -m src.data_cleaning
python -m src.database
python -m src.analysis
```

The scripts should generate the cleaned CSV, SQLite database, and
analysis exports under `outputs/` and `database/`.

### 5. Launch the Streamlit dashboard

``` bash
streamlit run app.py
```

Streamlit will display a local URL in the terminal, usually
`http://localhost:8501`.

## Key Business Questions

-   Which categories and subcategories generate the strongest and
    weakest profit?
-   Which regions contribute most to overall profit?
-   How do sales and profit change over time?
-   How does profit vary across discount bands?
-   Which areas should be investigated first, and how will actions be
    measured?

## Limitations and Responsible Interpretation

-   The Sample Superstore dataset is a demonstration dataset, not live
    retail data.
-   Observed relationships do not automatically prove causation. For
    example, a discount/profit relationship alone does not prove that
    discounts caused a loss.
-   The what-if simulator is assumption-based and should not be
    presented as a validated financial forecast.
-   Business recommendations should be validated with transaction
    details, cost drivers, and comparable time periods.
-   Do not include confidential business data in a publicly shared
    Tableau workbook or repository.

## Portfolio Links

-   **GitHub repository:** Add your repository URL here.
-   **Tableau Public dashboard:** Add your published workbook URL here.
-   **Streamlit demo:** Add a hosted app URL here if deployed.
-   **Business Action Tracker:**
    `RetailPulse_Business_Action_Tracker.xlsx`

## Future Improvements

-   Add automated data-quality checks and validation reports.
-   Add date-range filters and clearer KPI definitions.
-   Improve the discount simulator with documented assumptions and
    sensitivity scenarios.
-   Add a repeatable monthly reporting workflow.
-   Connect action outcomes back to the original KPI baseline to assess
    whether changes worked.

## Author

**Krish Tiwari**\
Retail analytics project combining Python, SQL, dashboards, and business
operations thinking.
