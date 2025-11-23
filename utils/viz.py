import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

def line_chart(df):
    """
    Draw line chart with sales and quantity / 折线图（双轴）
    """
    base = alt.Chart(df).encode(x='ORDERDATE:T')

    # 销售额折线
    line_sales = base.mark_line(color='blue').encode(
        y=alt.Y('SALES:Q', axis=alt.Axis(title='Sales ($)', titleColor='blue'))
    )

    # 销售量折线
    line_qty = base.mark_line(color='orange').encode(
        y=alt.Y('QUANTITYORDERED:Q', axis=alt.Axis(title='Quantity', titleColor='orange'))
    )

    chart = alt.layer(line_sales, line_qty).resolve_scale(y='independent').interactive()
    st.altair_chart(chart, use_container_width=True)


def bar_chart(df):
    """
    Draw bar chart with sales by country / 条形图
    """
    df_melt = df.melt(
        id_vars=['COUNTRY'],
        value_vars=['SALES'],
        var_name='Metric',
        value_name='Value'
    )

    chart = alt.Chart(df_melt).mark_bar().encode(
        x=alt.X('COUNTRY:N', title='Country'),
        y=alt.Y('Value:Q', title='Sales ($)'),
        color=alt.Color('Metric:N', title='Metric', scale=alt.Scale(range=['blue'])),
        tooltip=['COUNTRY', 'Metric', 'Value']
    ).interactive()

    st.altair_chart(chart, use_container_width=True)


def show_all_country_pies(df):
    """
    Draw overall product line pie + per-country product line pies
    总销售占比 + 每个国家车型占比饼图
    """
    st.subheader("Overall Sales by Product Line")
    df_total = df.groupby("PRODUCTLINE").agg({"SALES": "sum"}).reset_index()
    fig_total = px.pie(
        df_total,
        names="PRODUCTLINE",
        values="SALES",
        title="Total Sales Share by Product Line",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig_total, use_container_width=True)

    st.subheader("Sales Share by Product Line per Country")
    countries = df["COUNTRY"].unique()
    n_cols = 4
    cols = st.columns(n_cols)

    for i, country in enumerate(countries):
        df_country = df[df["COUNTRY"] == country]
        df_country_group = df_country.groupby("PRODUCTLINE").agg({"SALES": "sum"}).reset_index()
        fig_country = px.pie(
            df_country_group,
            names="PRODUCTLINE",
            values="SALES",
            title=country,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        cols[i % n_cols].plotly_chart(fig_country, use_container_width=True)
        if (i + 1) % n_cols == 0:
            cols = st.columns(n_cols)

def scatter_price(df, x_axis):
    """
    Draw PRICEEACH vs selected X scatter plot / 价格散点图
    """
    df_plot = df.copy()
    if x_axis == "ORDERDATE":
        df_plot["ORDERDATE"] = pd.to_datetime(df_plot["ORDERDATE"], dayfirst=True)
        df_plot["MONTH"] = df_plot["ORDERDATE"].dt.to_period("M").astype(str)
        x_axis = "MONTH"

    fig = px.scatter(
        df_plot,
        x=x_axis,
        y="PRICEEACH",
        color="PRODUCTLINE",
        hover_data=["CUSTOMERNAME", "COUNTRY", "ORDERNUMBER"],
        title=f"PRICEEACH vs {x_axis}",
        labels={"PRICEEACH": "Price Each ($)", x_axis: x_axis},
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)


# -------------------------
# Line chart: Australia vs France
# -------------------------
def line_chart_au_fr(df_clean):
    df_clean["ORDER_MONTH"] = pd.to_datetime(df_clean["ORDERDATE"], dayfirst=True).dt.to_period("M")
    df_countries = df_clean[df_clean["COUNTRY"].isin(["Australia", "France"])]
    df_monthly = df_countries.groupby(["ORDER_MONTH", "COUNTRY"]).agg({"SALES":"sum"}).reset_index()
    df_monthly["ORDER_MONTH"] = df_monthly["ORDER_MONTH"].dt.to_timestamp()
    chart = alt.Chart(df_monthly).mark_line(point=True).encode(
        x="ORDER_MONTH:T",
        y="SALES:Q",
        color="COUNTRY:N",
        tooltip=["ORDER_MONTH:T", "SALES:Q", "COUNTRY:N"]
    ).interactive().properties(width=700, height=400)
    return chart

# -------------------------
# Choropleth: Sales quantity map by month
# -------------------------
def choropleth_sales(df_clean, selected_month):
    df_clean["MONTH_STR"] = df_clean["ORDERDATE"].dt.to_period("M").astype(str)
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
    return fig

# -------------------------
# Heatmaps: Sales by country and month for a year
# -------------------------
def heatmap_sales(df_clean, year):
    df_clean["YEAR"] = df_clean["ORDERDATE"].dt.year
    df_clean["MONTH"] = df_clean["ORDERDATE"].dt.month
    df_monthly = df_clean.groupby(["YEAR", "MONTH", "COUNTRY"]).agg({"SALES": "sum"}).reset_index()
    df_year = df_monthly[df_monthly["YEAR"] == year]
    chart = alt.Chart(df_year).mark_rect().encode(
        x=alt.X("MONTH:O", title="Month"),
        y=alt.Y("COUNTRY:N", title="Country"),
        color=alt.Color("SALES:Q", title="Total Sales", scale=alt.Scale(scheme="greens")),
        tooltip=["COUNTRY:N", "MONTH:O", "SALES:Q"]
    ).properties(width=300, height=400, title=f"Sales Heatmap {year}")
    return chart

# -------------------------
# Scatter plot: Price vs MSRP difference
# -------------------------
def scatter_price_msrp(df_clean, x_axis):
    df_plot = df_clean.copy()
    if x_axis == "ORDERDATE":
        df_plot["ORDERDATE"] = pd.to_datetime(df_plot["ORDERDATE"], dayfirst=True)
        df_plot["MONTH"] = df_plot["ORDERDATE"].dt.to_period("M").astype(str)
        x_axis = "MONTH"
    df_plot["PRICE_DIFF_RATIO"] = (df_plot["PRICEEACH"] - df_plot["MSRP"]) / df_plot["MSRP"]
    chart = alt.Chart(df_plot).mark_circle(size=60, opacity=0.6).encode(
        x=alt.X(f"{x_axis}:Q", title=x_axis),
        y=alt.Y("PRICE_DIFF_RATIO:Q", title="Price vs MSRP Ratio"),
        color="PRODUCTLINE:N",
        tooltip=[x_axis, "PRICEEACH", "MSRP", "PRICE_DIFF_RATIO", "PRODUCTLINE"]
    ).interactive().properties(width=700, height=400)
    return chart

# =========================
# NEW VISUALIZATIONS 新增可视化
# =========================

def sales_treemap(df_clean):
    """树状图显示销售层级结构"""
    # 国家 -> 产品线 -> 具体产品
    df_hierarchy = df_clean.groupby(['COUNTRY', 'PRODUCTLINE', 'PRODUCTCODE']).agg({
        'SALES': 'sum',
        'QUANTITYORDERED': 'sum'
    }).reset_index()
    
    fig = px.treemap(
        df_hierarchy,
        path=['COUNTRY', 'PRODUCTLINE', 'PRODUCTCODE'],
        values='SALES',
        color='QUANTITYORDERED',
        color_continuous_scale='Blues',
        title="Sales Hierarchy Treemap (Country → Product Line → Product Code)"
    )
    fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    return fig

def customer_retention_heatmap(df_clean):
    """客户留存热力图"""
    # 确保日期列是 datetime 类型
    df_clean['ORDERDATE'] = pd.to_datetime(df_clean['ORDERDATE'])
    
    # 使用字符串格式的月份而不是 Period 对象
    df_clean['ORDER_MONTH'] = df_clean['ORDERDATE'].dt.to_period('M').astype(str)
    customer_first_month = df_clean.groupby('CUSTOMERNAME')['ORDER_MONTH'].min().reset_index()
    customer_first_month.columns = ['CUSTOMERNAME', 'FIRST_MONTH']
    
    # 合并数据
    df_with_cohort = df_clean.merge(customer_first_month, on='CUSTOMERNAME')
    
    # 计算月份差异 - 转换为时间戳计算
    df_with_cohort['ORDER_MONTH_TS'] = pd.to_datetime(df_with_cohort['ORDER_MONTH'])
    df_with_cohort['FIRST_MONTH_TS'] = pd.to_datetime(df_with_cohort['FIRST_MONTH'])
    df_with_cohort['COHORT_INDEX'] = (
        (df_with_cohort['ORDER_MONTH_TS'].dt.year - df_with_cohort['FIRST_MONTH_TS'].dt.year) * 12 + 
        (df_with_cohort['ORDER_MONTH_TS'].dt.month - df_with_cohort['FIRST_MONTH_TS'].dt.month)
    )
    
    # 创建留存矩阵
    cohort_data = df_with_cohort.groupby(['FIRST_MONTH', 'COHORT_INDEX']).agg({
        'CUSTOMERNAME': 'nunique'
    }).reset_index()
    
    cohort_pivot = cohort_data.pivot_table(
        index='FIRST_MONTH', 
        columns='COHORT_INDEX', 
        values='CUSTOMERNAME'
    ).fillna(0)
    
    # 计算留存率
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    # 创建热力图
    fig = px.imshow(
        retention_matrix,
        title="Customer Retention Heatmap",
        color_continuous_scale="Blues",
        aspect="auto",
        labels=dict(x="Months Since First Purchase", y="Cohort Month", color="Retention Rate")
    )
    
    return fig

def product_sales_funnel(df_clean):
    """产品销售漏斗图"""
    # 计算每个产品线的转化指标
    product_funnel = df_clean.groupby('PRODUCTLINE').agg({
        'ORDERNUMBER': 'nunique',  # 订单数量
        'QUANTITYORDERED': 'sum',  # 总销量
        'SALES': 'sum',           # 总销售额
        'CUSTOMERNAME': 'nunique' # 客户数量
    }).reset_index()
    
    # 创建漏斗图
    fig = px.funnel(
        product_funnel, 
        x='SALES', 
        y='PRODUCTLINE',
        title="Product Line Sales Funnel",
        labels={'SALES': 'Total Sales ($)', 'PRODUCTLINE': 'Product Line'}
    )
    
    return fig

def correlation_heatmap(df_clean):
    """数值变量相关性热力图"""
    # 选择数值列
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    numeric_df = df_clean[numeric_cols]
    
    # 计算相关性矩阵
    corr_matrix = numeric_df.corr()
    
    # 创建热力图
    fig = px.imshow(
        corr_matrix,
        title="Numerical Variables Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        aspect="auto",
        text_auto=True
    )
    
    return fig

def cluster_dendrogram(df_features_pct, linkage_method='ward'):
    """绘制层次聚类树状图"""
    Z = linkage(df_features_pct, method=linkage_method)
    
    plt.figure(figsize=(10, 8))
    dendrogram(Z, labels=df_features_pct.index, leaf_font_size=10, orientation='left')
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Distance")
    plt.ylabel("Country")
    
    return plt.gcf(), Z

def cluster_heatmap(df_features_with_cluster, dendro_order):
    """绘制聚类热力图"""
    # Order by dendrogram
    df_features_ordered = df_features_with_cluster.loc[dendro_order]
    
    plt.figure(figsize=(14, 10))
    sns.heatmap(
        df_features_ordered.iloc[:, :-2],  # Exclude cluster and Total_Sales columns
        annot=True,
        fmt=".1%",
        cmap="YlGnBu",
        linewidths=0.5,
        cbar_kws={'label': 'Sales Percentage'}
    )
    plt.title("Product Line Sales Share by Country (Clustered)", fontsize=14)
    plt.xlabel("Product Line", fontsize=12)
    plt.ylabel("Country", fontsize=12)
    plt.xticks(rotation=45)
    
    return plt.gcf()

def cluster_radar_chart(cluster_profile, cluster_id):
    """绘制聚类雷达图"""
    categories = cluster_profile.index.tolist() + [cluster_profile.index.tolist()[0]]
    values = cluster_profile.values.tolist() + [cluster_profile.values.tolist()[0]]
    
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'Cluster {cluster_id}'
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 0.4])),
        showlegend=False,
        title=f"Product Preference Profile - Cluster {cluster_id}",
        height=400
    )
    
    return fig_radar

def cluster_distribution_pie(cluster_df):
    """绘制聚类分布饼图"""
    cluster_counts = cluster_df['cluster'].value_counts().sort_index()
    fig_pie = px.pie(
        values=cluster_counts.values,
        names=[f"Cluster {i}" for i in cluster_counts.index],
        title="Countries per Cluster"
    )
    return fig_pie