import streamlit as st
import altair as alt
import plotly.express as px
import pandas as pd

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