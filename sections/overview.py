import streamlit as st
import pandas as pd
from utils.viz import line_chart, bar_chart, show_all_country_pies, scatter_price

def show(df_clean, tables):
    """
    Display dashboard overview with KPIs and trends / 总览页面
    """
    st.title("Dashboard Overview")

    # KPI row
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Sales", f"${tables['kpi']['total_sales']:.2f}")
    c2.metric("Total Quantity", tables['kpi']['total_quantity'])
    c3.metric("Average Price", f"${tables['kpi']['avg_price']:.2f}")

    # Sales trends
    st.subheader("Sales Trends")
    line_chart(tables["timeseries"])
    st.markdown("""
    - Sales show clear temporal patterns with periodic fluctuations.
    - Sales trends for 2018 and 2019 are similar, showing seasonal stability.
    """)

    # Sales by country
    st.subheader("Sales by Country")
    bar_chart(tables["by_region"])
    st.markdown("""
    - Significant differences in total sales across countries.
    - Southern vs Northern Hemisphere countries may show different seasonal peaks.
    """)

    # Price scatter plot
    st.subheader("Price Scatter Plot")
    x_options = ["QUANTITYORDERED", "ORDERDATE", "COUNTRY", "PRODUCTLINE","PRODUCTCODE"]
    x_axis = st.selectbox("Select X-axis", x_options)
    scatter_price(df_clean, x_axis)
    st.markdown("""
    - Examine relationship between PRICEEACH and selected parameter.
    - Deep Dive can explore price vs MSRP, discounts, and promotions.
    """)

    # Product line pies
    show_all_country_pies(df_clean)
    st.markdown("""
    - Overall sales pie shows distribution across product lines.
    - Country-level pies reveal differences in product line preferences.
    - Deep Dive can further explore regional strategies.
    """)
