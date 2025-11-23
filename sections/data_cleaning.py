import streamlit as st
import pandas as pd
from utils.prep import preprocess_data

def show(df_raw):
    """
    Dataset introduction and cleaning / 数据集介绍与清理
    """
    # 页面标题
    st.title("Dataset Introduction")

    # 数据来源提示 / Data source caption
    st.caption("Source: data/Auto Sales data.csv")

    st.markdown("---")  # 分隔线 / separator

    # -------------------------
    # Dataset overview / 数据集概览
    # -------------------------
    st.subheader("Dataset Overview")
    col1, col2 = st.columns(2)
    col1.metric("Number of Rows", df_raw.shape[0])
    col2.metric("Number of Columns", df_raw.shape[1])
    st.markdown(f"**Columns:** {', '.join(df_raw.columns)}")

    st.markdown("---")

    # -------------------------
    # Data cleaning steps / 数据清理步骤
    # -------------------------
    st.subheader("Data Cleaning Steps")
    st.info("""
    The main cleaning operations include:
    1. Trim whitespace from string columns
    2. Remove duplicate rows
    3. Convert date columns to datetime
    4. Additional cleaning steps can be added as needed
    """)

    st.markdown("---")

    # -------------------------
    # Preprocess data / 调用预处理函数
    # -------------------------
    df_clean = preprocess_data(df_raw)
    st.success("Data cleaned successfully ✅")

    st.markdown("---")

    # -------------------------
    # Column-wise summary / 每列数据统计
    # -------------------------
    st.subheader("Column-wise Summary")

    # 分离数值列和分类列 / Separate numerical and categorical columns
    num_cols = df_clean.select_dtypes(include='number').columns
    cat_cols = df_clean.select_dtypes(exclude='number').columns

    st.markdown("**Numerical Columns Summary**")
    st.dataframe(df_clean[num_cols].describe().T.style.format("{:.2f}"), use_container_width=True)

    st.markdown("**Categorical Columns Summary**")
    st.dataframe(df_clean[cat_cols].describe().T, use_container_width=True)

    st.markdown("---")

    # 页面底部提示下一步 / Next step hint
    st.success("✅ Data cleaning completed. Proceed to the Overview page.")

    return df_clean
