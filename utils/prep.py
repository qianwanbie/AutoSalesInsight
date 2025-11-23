import pandas as pd

def preprocess_data(df_raw):
    """
    Clean raw dataset / 清洗原始数据
    """

    df = df_raw.copy()

    # 去掉字符串前后空格 / Trim whitespace
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # 删除重复行 / Drop duplicate rows
    df = df.drop_duplicates()

    # 日期列转换 / Convert date columns
    datetime_cols = [col for col in df.columns if "date" in col.lower()]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')

    return df

def make_tables(df_clean):
    """
    Generate summary tables for dashboard / 为仪表盘生成汇总表
    Returns a dict with tables for KPIs, time trends, regions etc.
    """
    tables = {}

    #  KPI 总览
    tables["kpi"] = {
        "total_sales": df_clean["SALES"].sum(),
        "total_quantity": df_clean["QUANTITYORDERED"].sum(),
        "avg_price": df_clean["PRICEEACH"].mean()
    }

    

    # 按月份汇总 / Sales by month
    df_time = df_clean.groupby(df_clean["ORDERDATE"].dt.to_period("M")).agg({
        "SALES": "sum",
        "QUANTITYORDERED": "sum",
        "ORDERNUMBER": "nunique"        
    }).reset_index()
    df_time["ORDERDATE"] = df_time["ORDERDATE"].dt.to_timestamp()  # 转回 Timestamp，方便绘图
    tables["timeseries"] = df_time

    #  按国家汇总 / Sales by country
    df_region = df_clean.groupby("COUNTRY").agg({
        "SALES": "sum",
        "ORDERNUMBER": "nunique"
    }).reset_index()
    tables["by_region"] = df_region

    return tables
