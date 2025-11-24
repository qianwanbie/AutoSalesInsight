import streamlit as st
import pandas as pd

def show():
    """
    Intro page for Auto Sales Dashboard / 汽车销售数据介绍页
    """

    # 页面标题 / Page title
    st.title(" Auto Sales Dashboard")

    st.markdown("---")

    # 项目简介 / Project description
    st.subheader(" About this Project")
    st.markdown("""
    Welcome to the **Auto Sales Dashboard**.

    This dashboard offers an interactive exploration of the **Auto Sales dataset**  
    (`data/Auto Sales data.csv`).  
    Users can analyze sales trends, pricing patterns, regional variations, and product performance.

    """)

    # 功能展示 / Key features
    st.subheader("Key Features ")
    st.markdown("""
    -  **KPIs Dashboard**: Total sales, average price, quantity sold  
    -  **Sales by Country / Region**  
    -  **Trends & Seasonality**  
    -  **Deep-dive Analysis** on product categories  
    -  **Country Clustering** using machine learning  

    """)

    # 使用说明 / How to use
    st.subheader(" How to Use ")
    st.markdown("""
    1. Navigate using the **sidebar**  
    2. Start with **Data Cleaning** to understand the dataset  
    3. Use **Overview** for key metrics & trends  
    4. Check **Deep Dives** for detailed analytics  
    5. Try **Country Clustering** to group markets intelligently  

    """)

    st.markdown("---")
    st.caption("Use the sidebar to begin your analysis. ")
