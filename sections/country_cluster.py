# sections/country_cluster.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import fcluster, dendrogram
from utils.viz import cluster_dendrogram, cluster_heatmap, cluster_radar_chart, cluster_distribution_pie

def show(df_clean):
    """
    Country Clustering based on Product Line Sales Share
    """
    st.title("Country Clustering Analysis by Product Line Preferences")

    st.markdown(
        """
        ### ANALYSIS OBJECTIVE
        This analysis employs hierarchical clustering to group countries based on their automotive product line preferences. 
        The resulting clusters reveal underlying market patterns that inform global strategic planning.
        """
    )

    # -------------------------
    # Prepare feature matrix
    # -------------------------
    st.subheader("DATA PREPARATION")
    
    # Calculate sales share by product line for each country
    df_features = df_clean.groupby(["COUNTRY", "PRODUCTLINE"])["SALES"].sum().unstack(fill_value=0)
    df_features_pct = df_features.div(df_features.sum(axis=1), axis=0)  # Convert to percentages
    
    st.info(f"DATASET OVERVIEW: {df_features_pct.shape[0]} countries × {df_features_pct.shape[1]} product lines")
    
    # Display raw data
    with st.expander("VIEW COUNTRY-PRODUCT MATRIX"):
        st.dataframe(df_features_pct.style.format("{:.2%}"), use_container_width=True)

    # -------------------------
    # Hierarchical clustering
    # -------------------------
    st.subheader("CLUSTERING ANALYSIS")
    
    # Fixed to 4 clusters based on analysis
    n_clusters = 4
    linkage_method = "ward"

    # Perform hierarchical clustering and get dendrogram
    dendro_fig, Z = cluster_dendrogram(df_features_pct, linkage_method)
    clusters = fcluster(Z, t=n_clusters, criterion='maxclust')
    
    # Create cluster results DataFrame
    cluster_df = pd.DataFrame({
        "COUNTRY": df_features_pct.index, 
        "cluster": clusters
    }).set_index("COUNTRY")
    
    df_features_with_cluster = df_features_pct.copy()
    df_features_with_cluster['cluster'] = cluster_df.loc[df_features_pct.index, 'cluster']
    df_features_with_cluster['Total_Sales'] = df_features.sum(axis=1)

    # Get dendrogram order for heatmap
    dendro_result = dendrogram(Z, labels=df_features_pct.index, leaf_font_size=10, orientation='left', no_plot=True)
    dendro_order = dendro_result['ivl']

    # -------------------------
    # Visualization Layout
    # -------------------------
    tab1, tab2, tab3, tab4 = st.tabs(["CLUSTERING RESULTS", "HEATMAP ANALYSIS", "CLUSTER PROFILES", "STRATEGIC ANALYSIS"])

    with tab1:
        # Dendrogram and cluster distribution
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("HIERARCHICAL CLUSTERING DENDOGRAM")
            st.pyplot(dendro_fig)
            plt.close()

        with col2:
            st.subheader("CLUSTER DISTRIBUTION")
            fig_pie = cluster_distribution_pie(cluster_df)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab2:
        # Clustered heatmap
        st.subheader("PRODUCT PREFERENCE HEATMAP")
        heatmap_fig = cluster_heatmap(df_features_with_cluster, dendro_order)
        st.pyplot(heatmap_fig)
        plt.close()

    with tab3:
        # Cluster characteristics analysis
        st.subheader("CLUSTER PROFILE ANALYSIS")
        
        # Calculate average sales share per cluster
        cluster_avg = df_features_with_cluster.groupby("cluster").mean().iloc[:, :-1]  # Exclude Total_Sales
        
        # Display cluster characteristics
        for cluster_id in sorted(cluster_avg.index):
            cluster_countries = cluster_df[cluster_df['cluster'] == cluster_id].index.tolist()
            cluster_profile = cluster_avg.loc[cluster_id]
            total_sales = df_features_with_cluster[df_features_with_cluster['cluster'] == cluster_id]['Total_Sales'].sum()
            
            st.markdown(f"### CLUSTER {cluster_id} - {len(cluster_countries)} COUNTRIES (TOTAL SALES: ${total_sales:,.0f})")
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Radar chart for cluster profile
                fig_radar = cluster_radar_chart(cluster_profile, cluster_id)
                st.plotly_chart(fig_radar, use_container_width=True)
            
            with col2:
                st.markdown("**COUNTRIES IN THIS CLUSTER:**")
                for country in cluster_countries:
                    country_sales = df_features_with_cluster.loc[country, 'Total_Sales']
                    st.write(f"- {country} (${country_sales:,.0f})")
                
                st.markdown("**TOP 3 PRODUCT PREFERENCES:**")
                top_products = cluster_profile.nlargest(3)
                for product, share in top_products.items():
                    st.write(f"- {product}: {share:.1%}")

    with tab4:
        # Strategic Analysis based on Clustering Results
        st.subheader("STRATEGIC ANALYSIS OF CLUSTERING RESULTS")
        
        # Calculate actual total sales and cluster sales
        total_sales_all = df_clean['SALES'].sum()
        
        # Calculate sales for each cluster based on actual clustering results
        cluster_sales = {}
        cluster_countries = {}
        cluster_product_preferences = {}
        
        for cluster_id in sorted(df_features_with_cluster['cluster'].unique()):
            cluster_countries[cluster_id] = df_features_with_cluster[df_features_with_cluster['cluster'] == cluster_id].index.tolist()
            cluster_sales[cluster_id] = df_features_with_cluster[df_features_with_cluster['cluster'] == cluster_id]['Total_Sales'].sum()
            
            # Calculate top product preferences for each cluster
            cluster_avg = df_features_with_cluster[df_features_with_cluster['cluster'] == cluster_id].iloc[:, :-2].mean()
            cluster_product_preferences[cluster_id] = cluster_avg.nlargest(3)
        
        st.markdown("### EXECUTIVE SUMMARY")
        
        st.markdown(f"""
        **MARKET SEGMENTATION OVERVIEW**: The hierarchical clustering analysis reveals four distinct market segments based on product line preferences. 
        **CLUSTER DISTRIBUTION PATTERN**: Cluster 1 contains major automotive markets, Cluster 3 represents balanced markets, while Clusters 2 and 4 are specialized markets.
        Each cluster demonstrates distinct characteristics in product preferences, market size, and growth potential.
        """)
        
        # Cluster 1 Analysis
        st.markdown("---")
        st.markdown("### CLUSTER 1: MAJOR AUTOMOTIVE MARKETS")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **CLUSTER CHARACTERISTICS**:
            - Contains {len(cluster_countries[1])} major automotive markets
            - Balanced product preferences with notable strength in classic and vintage cars
            - Mature automotive markets with established consumer bases
            - Strong brand awareness and purchasing power
            
            **PRODUCT STRATEGY FOCUS**:
            - Emphasize classic car and vintage car product lines
            - Maintain balanced product portfolio coverage
            - Strengthen market penetration in premium product lines
            """)
        
        with col2:
            st.metric("TOTAL CLUSTER SALES", f"${cluster_sales[1]:,.0f}")
            st.metric("MARKET COVERAGE", f"{len(cluster_countries[1])}/19 Countries")
            st.metric("STRATEGIC IMPORTANCE", "Core Markets")
        
        st.markdown("""
        **STRATEGIC RECOMMENDATIONS**:
        - **PRICING STRATEGY**: Consider appropriate premium pricing for classic and vintage models
        - **PRODUCT FOCUS**: Prioritize classic cars and vintage cars in product development
        - **RESOURCE ALLOCATION**: Focus marketing investments and expansion efforts in this cluster
        - **INVENTORY MANAGEMENT**: Ensure adequate supply of classic and vintage models
        """)
        
        # Cluster 3 Analysis
        st.markdown("---")
        st.markdown("### CLUSTER 3: BALANCED MARKETS")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"""
            **CLUSTER CHARACTERISTICS**:
            - Contains {len(cluster_countries[3])} markets with the most balanced product distribution
            - Relatively strong performance in trucks and buses categories
            - Consumer behavior偏向 practical and utility-focused
            - Mix of European developed markets and Asian emerging markets
            
            **PRODUCT STRATEGY FOCUS**:
            - Maintain balanced product portfolio
            - Strengthen commercial and utility vehicle product lines
            - Focus on value-oriented product development
            """)
        
        with col2:
            st.metric("TOTAL CLUSTER SALES", f"${cluster_sales[3]:,.0f}")
            st.metric("MARKET COVERAGE", f"{len(cluster_countries[3])}/19 Countries")
            st.metric("MARKET TYPE", "Balanced Development")
        
        st.markdown("""
        **STRATEGIC RECOMMENDATIONS**:
        - **PRICING STRATEGY**: Adopt competitive pricing with appropriate discounts
        - **PRODUCT FOCUS**: Emphasize trucks and buses in product offerings
        - **MARKET EXPANSION**: Maintain European markets while developing Asian markets
        - **INVENTORY OPTIMIZATION**: Adjust inventory levels based on actual demand patterns
        """)
        
        # Cluster 2 Analysis - Belgium
        st.markdown("---")
        st.markdown("### CLUSTER 2: SPECIALIZED MARKET - BELGIUM")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **CLUSTER CHARACTERISTICS**:
            - Single country forming independent cluster with highly specialized product preferences
            - Significant divergence from regional market patterns
            
            **PRODUCT STRATEGY FOCUS**:
            - Focus on depth in specific product categories
            """)
        
        with col2:
            st.metric("TOTAL SALES", f"${cluster_sales[2]:,.0f}")
            st.metric("MARKET POSITION", "Highly Specialized")
        
        st.markdown("""
        **STRATEGIC RECOMMENDATIONS**:
        - **PRICING STRATEGY**: Implement customized pricing for specialized products
        - **PRODUCT FOCUS**: Concentrate on dominant product categories identified in analysis
        - **MARKET RESEARCH**: Conduct detailed research to understand unique market drivers
        - **DISTRIBUTION REVIEW**: Analyze potential distribution hub effects
        """)
        
        # Cluster 4 Analysis - Switzerland
        st.markdown("---")
        st.markdown("### CLUSTER 4: PREMIUM SPECIALIST - SWITZERLAND")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            **CLUSTER CHARACTERISTICS**:
            - Premium specialist market with distinct product preferences
            - Affluent consumer base with quality-focused purchasing behavior
            - Luxury and high-performance vehicle orientation
            - High-value, quality-over-quantity market characteristics
            
            **PRODUCT STRATEGY FOCUS**:
            - Curate premium and limited edition models
            - Focus on luxury and high-performance segments
            - Emphasize quality and precision in product offerings
            """)
        
        with col2:
            st.metric("TOTAL SALES", f"${cluster_sales[4]:,.0f}")
            st.metric("MARKET POSITION", "Premium Specialist")
        
        st.markdown("""
        **STRATEGIC RECOMMENDATIONS**:
        - **PRICING STRATEGY**: Implement premium pricing strategies for luxury segments
        - **PRODUCT FOCUS**: Focus on high-margin luxury and performance vehicles
        - **MARKETING APPROACH**: Use exclusive marketing and distribution channels
        - **CUSTOMER RELATIONS**: Assign dedicated account management for premium clientele
        """)
        
        # Overall Strategic Recommendations
        st.markdown("---")
        st.subheader("OVERALL STRATEGIC RECOMMENDATIONS")
        
        recommendations = [
            "RESOURCE ALLOCATION: Prioritize Cluster 1 for major investments while maintaining appropriate coverage in other clusters",
            "PRODUCT DEVELOPMENT: Develop cluster-specific product features aligned with identified preference patterns", 
            "PRICING STRATEGY: Implement differentiated pricing approaches based on cluster characteristics and purchasing power",
            "INVENTORY MANAGEMENT: Optimize stock levels according to cluster-specific product preference patterns",
            "MARKET EXPANSION: Use cluster similarities to identify new market opportunities with comparable characteristics"
        ]
        
        for i, recommendation in enumerate(recommendations, 1):
            st.success(f"{i}. {recommendation}")

        # Cluster Performance Summary
        st.markdown("---")
        st.subheader("CLUSTER PERFORMANCE SUMMARY")
        
        performance_data = {
            'CLUSTER': ['Cluster 1', 'Cluster 3', 'Belgium', 'Switzerland'],
            'COUNTRIES': [len(cluster_countries[1]), len(cluster_countries[3]), 1, 1],
            'TOTAL SALES': [f"${cluster_sales[1]:,.0f}", f"${cluster_sales[3]:,.0f}", f"${cluster_sales[2]:,.0f}", f"${cluster_sales[4]:,.0f}"],
            'MARKET SHARE': [f"{(cluster_sales[1]/total_sales_all):.1%}", f"{(cluster_sales[3]/total_sales_all):.1%}", 
                           f"{(cluster_sales[2]/total_sales_all):.1%}", f"{(cluster_sales[4]/total_sales_all):.1%}"],
            'STRATEGIC FOCUS': ['Core Growth', 'Balanced Development', 'Niche Specialization', 'Premium Excellence']
        }
        
        performance_df = pd.DataFrame(performance_data)
        st.dataframe(performance_df, use_container_width=True)

    # -------------------------
    # Data Export
    # -------------------------
    st.subheader("DATA EXPORT")
    
    # Create detailed results table
    result_df = df_features_with_cluster.copy()
    result_df['Cluster_Size'] = result_df['cluster'].map(cluster_df['cluster'].value_counts())
    
    with st.expander("VIEW DETAILED CLUSTER ASSIGNMENT"):
        display_df = result_df.reset_index()[['COUNTRY', 'cluster', 'Total_Sales', 'Cluster_Size']]
        display_df['Total_Sales'] = display_df['Total_Sales'].map("${:,.0f}".format)
        st.dataframe(display_df.sort_values('cluster'), use_container_width=True)
    
    # Download button
    csv = result_df.reset_index().to_csv(index=False)
    st.download_button(
        label="DOWNLOAD CLUSTER RESULTS AS CSV",
        data=csv,
        file_name="country_cluster_analysis.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.caption("ANALYSIS INSIGHT: Market segmentation based on product preferences provides more strategic value than traditional geographic grouping.")