import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

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

    # 叠加折线并使用独立 y 轴
    chart = alt.layer(
        line_sales,
        line_qty
    ).resolve_scale(
        y='independent'
    ).interactive()

    st.altair_chart(chart, use_container_width=True)


def bar_chart(df):
    """
    Draw bar chart with sales and quantity / 条形图（分组柱状图）
    """
    # 将 SALES 和 QUANTITYORDERED 转成长格式
    df_melt = df.melt(
        id_vars=['COUNTRY'],
        value_vars=['SALES'],
        var_name='Metric',
        value_name='Value'
    )

    chart = alt.Chart(df_melt).mark_bar().encode(
        x=alt.X('COUNTRY:N', title='Country'),
        y=alt.Y('Value:Q', title='sales'),
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
    
    # 总销售额按产品线
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
    n_cols = 3  # 每行显示几个饼图
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
        # 将饼图放到对应列
        cols[i % n_cols].plotly_chart(fig_country, use_container_width=True)
        # 每行结束后重新生成列对象
        if (i + 1) % n_cols == 0:
            cols = st.columns(n_cols)