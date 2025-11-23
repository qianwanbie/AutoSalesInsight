import pandas as pd

def load_data(path="data\Auto Sales data.csv"):
    """
    Load dataset from CSV / 从 CSV 文件加载数据
    """
    df = pd.read_csv(path)
    return df
