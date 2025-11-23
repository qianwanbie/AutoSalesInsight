import streamlit as st
import pandas as pd

def show():
    """
    Intro page for Auto Sales Dashboard / 汽车销售数据介绍页
    """

    # 页面标题 / Page title
    st.title(" Auto Sales Dashboard")

    # Logo 行 / Logos row
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("assets/EFREI-logo.png", width=160)
    with col2:
        st.image("assets/WUT-Logo.png", width=160)

    st.markdown("---")

    # 项目简介 / Project description
    st.subheader(" About this Project")
    st.markdown("""
    Welcome to the **Auto Sales Dashboard**.

    This dashboard offers an interactive exploration of the **Auto Sales dataset**  
    (`data/Auto Sales data.csv`).  
    Users can analyze sales trends, pricing patterns, regional variations, and product performance.

    ---
    **项目简介（中文）**  
    本仪表盘可互动式分析 **汽车销售数据集**，包括销量趋势、价格模式、地区差异和产品表现等内容。
    """)

    # 功能展示 / Key features
    st.subheader("✨ Key Features / 主要功能")
    st.markdown("""
    -  **KPIs Dashboard**: Total sales, average price, quantity sold  
    -  **Sales by Country / Region**  
    -  **Trends & Seasonality**  
    -  **Deep-dive Analysis** on product categories  
    -  **Country Clustering** using machine learning  

    **主要功能（中文）**：  
    - 查看 **关键指标（KPI）**：总销售额、平均销售价、数量等  
    - 分析 **各国和产品线的销售情况**  
    - 观察 **季节性趋势与变化**  
    - 进行 **深度分析**（如按产品、按地区）  
    - 使用 **聚类分析** 识别销售模式相似的国家
    """)

    # 使用说明 / How to use
    st.subheader("📌 How to Use / 使用说明")
    st.markdown("""
    1. Navigate using the **sidebar**  
    2. Start with **Data Cleaning** to understand the dataset  
    3. Use **Overview** for key metrics & trends  
    4. Check **Deep Dives** for detailed analytics  
    5. Try **Country Clustering** to group markets intelligently  

    **使用流程（中文）**：  
    1. 使用左侧 **侧边栏** 进行页面切换  
    2. 从 **数据清洗** 开始查看数据结构  
    3. 在 **概览页面** 获取关键指标  
    4. 使用 **深度分析** 查看更多细节  
    5. 通过 **聚类分析** 发现市场间的相似性
    """)

    st.markdown("---")
    st.caption("Use the sidebar to begin your analysis. / 请使用左侧侧边栏开始分析。")
