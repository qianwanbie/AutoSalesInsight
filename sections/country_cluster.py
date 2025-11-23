# sections/country_clusters.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster

def show(df_clean):
    """
    Country Clustering based on Product Line Sales Share
    """
    st.title("🌍 Country Clustering by Product Line Sales Share")

    st.markdown(
        """
        This analysis uses the **sales share** of each product line per country as features. 
        Similar countries are clustered together.
        """
    )

    # -------------------------
    # Prepare feature matrix
    # -------------------------
    df_features = df_clean.groupby(["COUNTRY", "PRODUCTLINE"])["SALES"].sum().unstack(fill_value=0)
    df_features = df_features.div(df_features.sum(axis=1), axis=0)  # 转为比例

    # -------------------------
    # Hierarchical clustering
    # -------------------------
    st.subheader("Hierarchical Clustering and Heatmap")

    # 固定聚类数量选择框
    n_clusters = st.selectbox("Select number of clusters", options=[2,3,4,5,6,7,8,9,10], index=3)

    Z = linkage(df_features, method='ward')
    clusters = fcluster(Z, t=n_clusters, criterion='maxclust')
    cluster_df = pd.DataFrame({"COUNTRY": df_features.index, "cluster": clusters}).set_index("COUNTRY")
    df_features['cluster'] = cluster_df.loc[df_features.index, 'cluster']

    # 获取 dendrogram 排序后的国家顺序
    plt.figure(figsize=(6, 8))
    dendro = dendrogram(Z, labels=df_features.index, leaf_font_size=10, orientation='left')
    plt.title("Dendrogram")
    plt.xlabel("Distance")
    plt.ylabel("Country")
    dendro_fig = plt.gcf()
    plt.close()

    df_features_ordered = df_features.loc[dendro['ivl']]

    # -------------------------
    # 左右两图布局
    # -------------------------
    col1, col2 = st.columns([1,1])

    with col1:
        st.subheader("Dendrogram")
        st.pyplot(dendro_fig)

    with col2:
        st.subheader("Clustered Heatmap")
        plt.figure(figsize=(8, 8))
        sns.heatmap(
            df_features_ordered.iloc[:, :-1],
            annot=True,
            fmt=".2f",
            cmap="YlGnBu",
            linewidths=0.5
        )
        plt.xlabel("Product Line")
        plt.ylabel("Country")
        st.pyplot(plt.gcf())
        plt.close()

    # -------------------------
    # Display cluster average
    # -------------------------
    st.subheader("Cluster Average Sales Share")
    cluster_avg = df_features_ordered.groupby("cluster").mean()
    st.dataframe(cluster_avg)

    # -------------------------
    # Display cluster assignment with correlation
    # -------------------------
    st.subheader("Cluster Assignment with Correlation")
    cluster_corr_list = []
    for idx, row in df_features_ordered.iterrows():
        cluster_id = row['cluster']
        avg_profile = cluster_avg.loc[cluster_id]
        corr = row.iloc[:-1].corr(avg_profile)
        cluster_corr_list.append(corr)

    df_features_ordered['correlation_with_cluster'] = cluster_corr_list
    st.dataframe(df_features_ordered[['cluster', 'correlation_with_cluster']].reset_index())

    # -------------------------
    # Add description & conclusions
    # -------------------------
    st.subheader("Clustering Description & Insights")
    st.markdown("""
    Based on the hierarchical clustering, countries are grouped into **{} clusters**. 
    The correlation values indicate how well each country's sales profile aligns with its cluster average.

    **Cluster interpretation:**
    - **Cluster 1**: Countries with diversified product line sales (e.g., classic cars, vintage cars, trucks/buses). Most correlations >0.78.
    - **Cluster 2**: Belgium – a unique market with distinct preferences.
    - **Cluster 3**: Northern European countries (Denmark, Germany, Finland, Austria, Norway, Ireland) and Philippines, showing strong alignment (>0.94) with cluster profile.
    - **Cluster 4**: Switzerland – highly specialized product line pattern.

    **Conclusions:**
    1. Majority of countries belong to clusters showing common trends in sales distribution.
    2. Outliers (Clusters 2 & 4) require tailored marketing strategies.
    3. Regional trends can guide inventory planning and campaign strategies.
    """.format(n_clusters))
