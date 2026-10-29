
from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "retailpulse.db"

st.set_page_config(
    page_title="RetailPulse",
    page_icon="📊",
    layout="wide"
)

st.title("RetailPulse")
st.subheader("Retail Performance & Profit Intelligence")
st.caption(
    "Explore sales performance, identify profit leaks, "
    "and test hypothetical business scenarios."
)

if not DB_PATH.exists():
    st.error("Database not found. Run python -m src.database first.")
    st.stop()

with sqlite3.connect(DB_PATH) as conn:
    df = pd.read_sql_query("SELECT * FROM transactions", conn)

# Ensure data types are correct
df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

# Sidebar filters
st.sidebar.header("Explore your business")

regions = ["All"] + sorted(df["Region"].dropna().unique().tolist())
categories = ["All"] + sorted(df["Category"].dropna().unique().tolist())

selected_region = st.sidebar.selectbox("Region", regions)
selected_category = st.sidebar.selectbox("Category", categories)

filtered = df.copy()

if selected_region != "All":
    filtered = filtered[filtered["Region"] == selected_region]

if selected_category != "All":
    filtered = filtered[filtered["Category"] == selected_category]

# KPI calculations
sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
margin = profit / sales if sales else 0

orders = (
    filtered["Order ID"].nunique()
    if "Order ID" in filtered.columns
    else len(filtered)
)

# KPI cards
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"${sales:,.0f}")
c2.metric("Total Profit", f"${profit:,.0f}")
c3.metric("Profit Margin", f"{margin:.2%}")
c4.metric("Orders", f"{orders:,}")

st.divider()

# Sales trend
monthly = (
    filtered.groupby("Month", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Month")
)

left, right = st.columns(2)

with left:
    st.plotly_chart(
        px.line(
            monthly,
            x="Month",
            y="Sales",
            markers=True,
            title="Monthly Sales Trend"
        ),
        use_container_width=True
    )

# Category profitability
category_data = (
    filtered.groupby("Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Profit")
)

with right:
    st.plotly_chart(
        px.bar(
            category_data,
            x="Category",
            y="Profit",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Profit by Category"
        ),
        use_container_width=True
    )

# Regional profit
left, right = st.columns(2)

region_data = (
    filtered.groupby("Region", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Profit")
)

with left:
    st.plotly_chart(
        px.bar(
            region_data,
            x="Profit",
            y="Region",
            orientation="h",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Regional Profitability"
        ),
        use_container_width=True
    )

# Loss-making subcategories
subcategories = (
    filtered.groupby("Sub-Category", as_index=False)
    .agg(Sales=("Sales", "sum"), Profit=("Profit", "sum"))
    .sort_values("Profit")
)

with right:
    st.plotly_chart(
        px.bar(
            subcategories.head(10),
            x="Profit",
            y="Sub-Category",
            orientation="h",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="10 Lowest-Profit Subcategories"
        ),
        use_container_width=True
    )

st.divider()

# Profit Leak Detector
st.header("Profit Leak Detector")

losses = subcategories[subcategories["Profit"] < 0].copy()

if losses.empty:
    st.success("No loss-making subcategories in this selection.")
else:
    losses["Potential Recovery"] = losses["Profit"].abs()

    st.write(
        "These subcategories have negative aggregate profit "
        "in the current selection. Investigate costs, product mix, "
        "returns, and discounts before changing policies."
    )

    st.dataframe(
        losses,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "Download Profit Leak Report",
        losses.to_csv(index=False).encode("utf-8"),
        "profit_leak_report.csv",
        "text/csv"
    )

# Discount analysis
st.header("Discount & Profit Analysis")

if "Discount Band" in filtered.columns:
    discount_data = (
        filtered.groupby("Discount Band", as_index=False)
        .agg(
            Sales=("Sales", "sum"),
            Profit=("Profit", "sum"),
            Transaction_Lines=("Profit", "size")
        )
    )

    st.plotly_chart(
        px.bar(
            discount_data,
            x="Discount Band",
            y="Profit",
            color="Profit",
            color_continuous_scale="RdYlGn",
            title="Profit by Discount Band"
        ),
        use_container_width=True
    )

    st.caption(
        "Discount-band comparisons are descriptive. "
        "They do not establish that discounts alone caused losses."
    )

# What-if simulator
st.divider()
st.header("What-If Discount Simulator")

st.write(
    "Explore how reducing discounts could affect revenue and profit, "
    "assuming the same quantities are sold and list prices remain unchanged."
)

discount_reduction = st.slider(
    "Reduce discount by (percentage points)",
    min_value=0,
    max_value=30,
    value=5,
    step=1
)

discounted_rows = filtered[
    (filtered["Discount"] > 0) &
    (filtered["Discount"] < 1)
].copy()

if discounted_rows.empty:
    st.info("No discounted transactions in the current selection.")
else:
    original_discount = discounted_rows["Discount"]

    # Approximate original list price from recorded sales.
    estimated_list_sales = (
        discounted_rows["Sales"] / (1 - original_discount)
    )

    new_discount = (
        original_discount - discount_reduction / 100
    ).clip(lower=0)

    estimated_new_sales = estimated_list_sales * (1 - new_discount)

    revenue_change = (
        estimated_new_sales - discounted_rows["Sales"]
    ).sum()

    # Assumes costs and quantities remain unchanged.
    scenario_profit = profit + revenue_change

    a, b, c = st.columns(3)
    a.metric("Current Profit", f"${profit:,.0f}")
    b.metric("Estimated Revenue Change", f"${revenue_change:,.0f}")
    c.metric("Illustrative Scenario Profit", f"${scenario_profit:,.0f}")

    st.caption(
        "Scenario only, not a forecast. It assumes recorded Sales are "
        "net of the recorded discount, list prices can be inferred as "
        "Sales / (1 - Discount), quantities remain unchanged, and "
        "incremental revenue flows to profit because costs remain fixed. "
        "Actual customer demand and costs may change."
    )

