import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
from utils.viz import line_chart_au_fr, choropleth_sales, heatmap_sales, scatter_price_msrp

def show(df_clean):
    """
    Deep dive analysis: Australia vs France sales trend + scatter plot
    深度分析：澳大利亚与法国销售趋势 + 散点图
    """
    st.title(" Deep Dive Analysis ")

    # -------------------------
    # Line chart: Australia vs France
    # -------------------------
    st.subheader("Australia vs France Sales Trend ")
    st.altair_chart(line_chart_au_fr(df_clean), use_container_width=True)
    # -------------------------
    # Sales Quantity Map by Month
    # -------------------------
    st.subheader("Sales Quantity Map by Month")
    months = df_clean["ORDERDATE"].dt.to_period("M").astype(str).sort_values().unique()
    selected_month = st.selectbox("Select Month for Map", months)
    st.plotly_chart(choropleth_sales(df_clean, selected_month), use_container_width=True)
    """
    Display side-by-side heatmaps of sales by country and month for 2018 and 2019
    分别显示 2018 年和 2019 年每个月各国家的销量热力图
    """
    st.subheader("Sales Heatmap by Country and Month")
    
    heatmap_2018 = heatmap_sales(df_clean, 2018)
    heatmap_2019 = heatmap_sales(df_clean, 2019)
    st.altair_chart(alt.hconcat(heatmap_2018, heatmap_2019), use_container_width=True)
    
    st.subheader("Updated Observation on Seasonal Sales Trends")
    st.markdown("""
    - After reviewing the first three charts, the previous assumption about opposite seasonal patterns between Northern and Southern Hemisphere countries appears incorrect.
    - In fact, peak sales periods are almost consistent across all regions, typically towards the end of the year.
    - Likely explanations include Christmas and winter holidays in Western countries.
    - In some Asian countries like Japan and Singapore, the Lunar New Year also falls around this period, contributing to higher sales.
    - Future Deep Dive analysis can explore the combined effects of global holidays and cultural events on sales patterns.
    """)

    """
    Scatter plot: Relative difference between PRICEEACH and MSRP
    显示售价与建议零售价的比例差
    """
    st.subheader("Price vs. MSRP Difference Ratio")
    
    options = ["QUANTITYORDERED", "SALES", "DAYS_SINCE_LASTORDER", "MSRP", "PRICEEACH", "ORDERDATE"]
    x_axis = st.selectbox("Select X-axis", options)
    st.altair_chart(scatter_price_msrp(df_clean, x_axis), use_container_width=True)
    
    st.subheader("Price vs MSRP Analysis Insight")
    st.markdown("""
    - The ratio between actual price (PRICEEACH) and MSRP shows two notable patterns:
      1. For products with higher MSRP, extreme overpricing is rare. In contrast, low-MSRP items sometimes sell at more than six times their reference price.
      2. Combining with seasonal sales observations: during off-peak periods, actual prices tend to stay close to MSRP, while in peak seasons, actual prices can significantly deviate from MSRP, both higher and lower.
    - Future Deep Dive analysis could explore pricing strategies, discounts, and market dynamics influencing these variations.
    """)

    st.markdown("---")
    st.info(
    """
    For further insights on how countries group together based on product line sales share,
    please check the **Country Clusters** page in the sidebar.  
    """
    )