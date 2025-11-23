import streamlit as st
import pandas as pd

def show():
    """
    Intro page for Auto Sales Dashboard
    / 汽车销售数据介绍页
    """

    # 页面标题 / Page title
    st.title("Auto Sales Dashboard")

    # Logo 行 / Logos row
    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/EFREI-logo.png", width=180)  # EFREI logo
    with col2:
        st.image("assets/WUT-Logo.png", width=180)    # WUT logo

    st.markdown("---")  # 分割线 / separator

    # 项目简介 / Project description
    st.subheader("About this Project")
    st.markdown("""
    This dashboard provides an interactive analysis of the **Auto Sales dataset** (`data/Auto Sales data.csv`).  
    Users can explore sales trends, pricing patterns, regional differences, and product performance.
    """)

    # 主要功能 / Key features
    st.subheader("Key Features")
    st.markdown("""
    - View **KPIs** such as total sales, average price, and quantity sold  
    - Explore **sales by country and product line**  
    - Conduct **deep dives** into seasonal trends and regional performance  
    - Perform **clustering analysis** to identify markets with similar sales patterns
    """)

    # 使用说明 / How to use
    st.subheader("How to Use")
    st.markdown("""
    1. Use the **sidebar** to navigate between pages  
    2. Start with **Data Cleaning** to prepare the dataset  
    3. Explore **Overview** for key metrics and trends  
    4. Use **Deep Dives** for detailed analysis  
    5. Check **Country Clustering** to identify similar markets
    """)

    st.markdown("---")
    st.caption("Navigate using the sidebar to explore different analyses.")
