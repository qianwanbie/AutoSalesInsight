import streamlit as st
import pandas as pd
from utils.prep import preprocess_data

def show(df_raw):
    """
    Intro page: dataset overview and cleaning steps
    """
    st.title("📊 Dataset Introduction")

    # -------------------------
    # Dataset overview
    # -------------------------
    st.subheader("Dataset Overview")
    st.markdown("""
    - **Number of rows:** {}  
    - **Number of columns:** {}  
    - **Columns:** {}  
    """.format(df_raw.shape[0], df_raw.shape[1], ", ".join(df_raw.columns)))

    # -------------------------
    # Data cleaning steps description
    # -------------------------
    st.subheader("Data Cleaning Steps")
    st.markdown("""
    The main cleaning operations include:
    - Trim whitespace from string columns
    - Remove duplicate rows 
    - Convert date columns to datetime
    - Additional cleaning steps can be added as needed
    """)

    # -------------------------
    # Call the preprocessing function
    # -------------------------
    df_clean = preprocess_data(df_raw)
    st.success("✅ Data cleaned successfully")

    # -------------------------
    # Column-wise summary
    # -------------------------
    st.subheader("Column-wise Summary")
    st.markdown("Shows statistics for both numerical and categorical columns：")
    st.dataframe(df_clean.describe(include='all').T)

    return df_clean
