import streamlit as st
from utils.io import load_data
from utils.viz import line_chart, bar_chart
from sections import intro, data_cleaning, overview, deep_dives, country_cluster, conclusions
from utils.prep import preprocess_data
from utils.prep import make_tables
st.set_page_config(page_title="Car Sales Dashboard", layout="wide")

@st.cache_data
def get_raw_data():
    """
    Load raw dataset 
    """
    df = load_data()
    return df
def get_clean_data():
    df_raw = load_data()
    df_clean = preprocess_data(df_raw)
    return df_clean

df_clean = get_clean_data()

df_raw = get_raw_data()

# Sidebar logos
st.sidebar.image("assets/EFREI-logo.png", use_container_width=True)
st.sidebar.image("assets/WUT-Logo.png", use_container_width=True)

# Sidebar contact info
st.sidebar.markdown(
    """
    **Author**  
    Boyuan Liu  
    boyuan.liu@efrei.net
    https://github.com/qianwanbie/AutoSalesInsight  
    """
)

st.sidebar.markdown(
    """
    **Supervisor**  
    Mano Mathew 
    mano.mathew@efrei.fr
    """
)

# Sidebar navigation / 侧边栏导航
st.sidebar.title("Navigation ")
page = st.sidebar.radio(
    "Select page ",
    ["Intro", "Data Cleaning", "Overview", "Deep Dives", "Country Cluster", "conclusions"]  # 新增 Country Cluster
)

# Page display / 页面显示
if page.startswith("Intro"):
    intro.show()
elif page.startswith("Data Cleaning"):
    df_clean = data_cleaning.show(df_raw)
elif page.startswith("Overview"):
    if 'df_clean' not in locals():
        st.warning("Please clean the data first")
    else:
        tables = make_tables(df_clean)
        overview.show(df_clean, tables)
elif page.startswith("Deep Dives"):
    if 'df_clean' not in locals():
        st.warning("Please clean the data first")
    else:
        deep_dives.show(df_clean)
elif page.startswith("Country Cluster"): 
    if 'df_clean' not in locals():
        st.warning("Please clean the data first")
    else:
        country_cluster.show(df_clean)
elif page.startswith("conclusions"):
    conclusions.show()