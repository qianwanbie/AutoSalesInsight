import streamlit as st

def show():
    """
    Conclusions page
    """
    st.title(" Conclusions & Insights")
    
    st.markdown("""
    Based on the analysis conducted in this dashboard, we can summarize:

    - **Seasonal Trends**: All regions show higher sales toward the end of the year, likely due to Christmas and winter holidays. In some Asian countries, Lunar New Year also drives sales.
    - **Pricing Insights**: High MSRP products rarely have extreme markup, while lower MSRP products sometimes exceed the suggested price multiple times. During low season, actual prices stay close to MSRP.
    - **Country Differences**: Product line preferences vary significantly by region. Cultural and geographic factors may influence these differences.
    - **Clustering Analysis**: Countries with similar sales share profiles are grouped together, providing insight for regional strategies and inventory planning.

    """)
    
    st.subheader("Next Steps / Recommendations")
    st.markdown("""
    - Explore promotional strategies around peak sales months.
    - Analyze pricing adjustments for low-MSRP products to control excessive markup.
    - Investigate regional preferences for targeted marketing.
    - Use clustering results to optimize inventory allocation and regional campaigns.
    
    """)
