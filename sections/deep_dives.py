import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt

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

    # 转换 ORDERDATE 为月份
    df_clean["ORDER_MONTH"] = pd.to_datetime(df_clean["ORDERDATE"], dayfirst=True).dt.to_period("M")

    # 筛选 Australia 和 France
    df_countries = df_clean[df_clean["COUNTRY"].isin(["Australia", "France"])]

    # 按月份和国家汇总销售额
    df_monthly = df_countries.groupby(["ORDER_MONTH", "COUNTRY"]).agg({"SALES":"sum"}).reset_index()
    df_monthly["ORDER_MONTH"] = df_monthly["ORDER_MONTH"].dt.to_timestamp()

    # 绘制折线图 / Line chart
    chart = alt.Chart(df_monthly).mark_line(point=True).encode(
        x="ORDER_MONTH:T",
        y="SALES:Q",
        color="COUNTRY:N",
        tooltip=["ORDER_MONTH:T", "SALES:Q", "COUNTRY:N"]
    ).interactive()

    st.altair_chart(chart, use_container_width=True)
    
    

    # -------------------------
    # Sales Quantity Map by Month
    # -------------------------
    st.subheader("Sales Quantity Map by Month")

    df_clean["MONTH_STR"] = df_clean["ORDERDATE"].dt.to_period("M").astype(str)
    months = df_clean["MONTH_STR"].sort_values().unique()
    selected_month = st.selectbox("Select Month for Map", months)

    df_month = df_clean[df_clean["MONTH_STR"] == selected_month]
    df_country_qty = df_month.groupby("COUNTRY").agg({"QUANTITYORDERED": "sum"}).reset_index()

    fig = px.choropleth(
        df_country_qty,
        locations="COUNTRY",
        locationmode="country names",
        color="QUANTITYORDERED",
        hover_name="COUNTRY",
        color_continuous_scale="Blues",
        title=f"Sales Quantity by Country ({selected_month})"
    )
    st.plotly_chart(fig, use_container_width=True)

    """
    Display side-by-side heatmaps of sales by country and month for 2018 and 2019
    分别显示 2018 年和 2019 年每个月各国家的销量热力图
    """
    st.subheader("Sales Heatmap by Country and Month")
    
    # 确保 ORDERDATE 是 datetime
    df_clean["ORDERDATE"] = pd.to_datetime(df_clean["ORDERDATE"], dayfirst=True)
    df_clean["YEAR"] = df_clean["ORDERDATE"].dt.year
    df_clean["MONTH"] = df_clean["ORDERDATE"].dt.month

    # 聚合每月每国家销量
    df_monthly = df_clean.groupby(["YEAR", "MONTH", "COUNTRY"]).agg({"SALES": "sum"}).reset_index()

    # 筛选 2018 和 2019
    df_2018 = df_monthly[df_monthly["YEAR"] == 2018]
    df_2019 = df_monthly[df_monthly["YEAR"] == 2019]

    # 创建 Altair 热力图函数
    def make_heatmap(data, year):
        return alt.Chart(data).mark_rect().encode(
            x=alt.X("MONTH:O", title="Month"),
            y=alt.Y("COUNTRY:N", title="Country"),
            color=alt.Color("SALES:Q", title="Total Sales", scale=alt.Scale(scheme="greens")),
            tooltip=["COUNTRY:N", "MONTH:O", "SALES:Q"]
        ).properties(
            width=300,
            height=400,
            title=f"Sales Heatmap {year}"
        )

    heatmap_2018 = make_heatmap(df_2018, 2018)
    heatmap_2019 = make_heatmap(df_2019, 2019)

    # 左右显示
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
    
    # 计算比例差
    df_clean["PRICE_DIFF_RATIO"] = (df_clean["PRICEEACH"] - df_clean["MSRP"]) / df_clean["MSRP"]
    
    # 可选横轴字段
    options = ["QUANTITYORDERED", "SALES", "DAYS_SINCE_LASTORDER", "MSRP", "PRICEEACH", "ORDERDATE"]
    x_axis = st.selectbox("Select X-axis ", options)

    df_plot = df_clean.copy()
    if x_axis == "ORDERDATE":
        df_plot["ORDERDATE"] = pd.to_datetime(df_plot["ORDERDATE"], dayfirst=True)
        df_plot["MONTH"] = df_plot["ORDERDATE"].dt.to_period("M").astype(str)
        x_axis = "MONTH"
    
    # 绘制散点图
    chart = alt.Chart(df_clean).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X(f"{x_axis}:Q", title=x_axis),
        y=alt.Y("PRICE_DIFF_RATIO:Q", title="Price vs MSRP Ratio"),
        color="PRODUCTLINE:N",
        tooltip=[x_axis, "PRICEEACH", "MSRP", "PRICE_DIFF_RATIO", "PRODUCTLINE"]
    ).interactive()
    
    st.altair_chart(chart, use_container_width=True)
    
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