import streamlit as st
import plotly.express as px
import pandas as pd
from utils.viz import line_chart, bar_chart, show_all_country_pies
import altair as alt

def show(df_clean, tables):
    """
    Display dashboard overview with KPIs and trends 
    """
    st.title(" Dashboard Overview ")

    # KPI 行 / KPI row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales", f"${tables['kpi']['total_sales']:.2f}")
    c2.metric("total_quantity", tables['kpi']['total_quantity'])
    c3.metric("Average Price", f"${tables['kpi']['avg_price']:.2f}")

    st.subheader("Sales Trends ")
    line_chart(tables["timeseries"])
    
    st.subheader("Sales Trends Insight")
    st.markdown("""
    - Sales show a clear temporal pattern with noticeable periodic fluctuations.
    - The line shapes for 2018 and 2019 are very similar, indicating that sales follow stable seasonal patterns influenced by months/quarters.
    - Deep Dive analysis could further explore the impact of seasonality or promotions on sales performance.
    """)

    st.subheader("Sales by Country ")
    bar_chart(tables["by_region"])

    st.subheader("Sales by Country Insight")
    st.markdown("""
    - There are clear differences in total sales across countries.
    - Since the dataset includes countries from both the Southern and Northern Hemispheres, sales peaks may be influenced by opposite seasonal patterns.
    - Hypothesis for Deep Dive: Sales performance in the same month may differ between countries in opposite hemispheres. This will be further explored in Deep Dive analysis.
    """)

    # -------------------------
    # Scatter plot: PRICEEACH vs selected X
    # -------------------------
    st.subheader("Price Scatter Plot ")

    # 在页面中选择横轴 / X-axis selection on the page
    x_options = ["QUANTITYORDERED", "ORDERDATE", "COUNTRY", "PRODUCTLINE","PRODUCTCODE"]
    x_axis = st.selectbox("Select X-axis ", x_options)

    # 如果选择的是日期，则按月份处理 / If ORDERDATE, convert to month
    df_plot = df_clean.copy()
    if x_axis == "ORDERDATE":
        df_plot["ORDERDATE"] = pd.to_datetime(df_plot["ORDERDATE"], dayfirst=True)
        df_plot["MONTH"] = df_plot["ORDERDATE"].dt.to_period("M").astype(str)
        x_axis = "MONTH"

    # 绘制散点图 / Scatter plot
    fig = px.scatter(
        df_plot,
        x=x_axis,
        y="PRICEEACH",
        color="PRODUCTLINE",
        hover_data=["CUSTOMERNAME", "COUNTRY", "ORDERNUMBER"],
        title=f"PRICEEACH vs {x_axis}",
        labels={"PRICEEACH": "Price Each ($)", x_axis: x_axis},
        template="plotly_white",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Price Insight")
    st.markdown("""
    - No clear relationship is observed between PRICEEACH and parameters like QUANTITYORDERED, ORDERDATE, COUNTRY, or PRODUCTLINE.
    - However, the dataset contains both MSRP (Manufacturer's Suggested Retail Price) and actual sales price (PRICEEACH).
    - Deep Dive analysis will focus on exploring the differences between actual price and MSRP, examining pricing strategies and discount behavior.
    """)

    """
    Display overall and per-country product line sales pies
    集成到 overview 页面，直接用 st 展示
    """

    st.subheader("Overall Sales by Product Line")
    # 总销售额按产品线
    df_total = df_clean.groupby("PRODUCTLINE").agg({"SALES": "sum"}).reset_index()
    fig_total = px.pie(
        df_total,
        names="PRODUCTLINE",
        values="SALES",
        title="Total Sales Share by Product Line",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_total, use_container_width=True)

    st.subheader("Sales Share by Product Line per Country")
    countries = df_clean["COUNTRY"].unique()
    n_cols = 3  # 每行显示几个饼图
    cols = st.columns(n_cols)

    for i, country in enumerate(countries):
        df_country = df_clean[df_clean["COUNTRY"] == country]
        df_country_group = df_country.groupby("PRODUCTLINE").agg({"SALES": "sum"}).reset_index()
        fig_country = px.pie(
            df_country_group,
            names="PRODUCTLINE",
            values="SALES",
            title=country,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        # 放到对应列
        cols[i % n_cols].plotly_chart(fig_country, use_container_width=True)
        # 每行结束后重新生成列对象
        if (i + 1) % n_cols == 0:
            cols = st.columns(n_cols)

    st.subheader("Product Line Sales Insight")
    st.markdown("""
    - The overall sales pie shows the distribution of sales across product lines.
    - Per-country pies reveal significant differences in product line sales between countries.
    - These differences may be influenced by geographical factors, cultural preferences, or local customs.
    - Deep Dive analysis will further explore these influences and regional product line strategies.
    """)    