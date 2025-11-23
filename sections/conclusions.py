import streamlit as st

def show():
    """
    Conclusions page
    """
    st.title("CONCLUSIONS AND INSIGHTS")
    
    # Key Findings Section
    st.header("KEY FINDINGS")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales Patterns")
        st.markdown("""
        • Year-end sales peaks across all regions  
        • Consistent seasonal trends 2018-2019  
        • Holiday-driven purchasing patterns  
        • Geographic performance variations
        """)
        
        st.subheader("Pricing Behavior") 
        st.markdown("""
        • Low MSRP products show markup potential  
        • High MSRP products maintain price stability  
        • Seasonal price fluctuations present  
        • Category-specific pricing sensitivities
        """)
    
    with col2:
        st.subheader("Market Segmentation")
        st.markdown("""
        • Four distinct customer clusters identified  
        • Product preference-based segmentation  
        • Clusters transcend geographic boundaries  
        • Clear strategic grouping patterns
        """)
        
        st.subheader("Product Preferences")
        st.markdown("""
        • Regional variations in product line favorability  
        • Classic/vintage focus in mature markets  
        • Practical vehicles in balanced markets  
        • Luxury specialization in premium markets
        """)

    # Strategic Recommendations Section
    st.header("STRATEGIC RECOMMENDATIONS")
    
    rec_col1, rec_col2 = st.columns(2)
    
    with rec_col1:
        st.subheader("Cluster Strategy")
        st.markdown("""
        • Prioritize Cluster 1 for major investments  
        • Develop cluster-specific product features  
        • Implement differentiated pricing approaches  
        • Optimize inventory using preference patterns
        """)
    
    with rec_col2:
        st.subheader("Operational Actions") 
        st.markdown("""
        • Target promotions around seasonal peaks  
        • Manage pricing for low-MSRP products  
        • Customize marketing by regional preferences  
        • Use clustering for expansion planning
        """)

    # Final Insight
    st.markdown("---")
    st.info("""
    **Strategic Insight**: Market segmentation based on product preferences provides 
    more actionable intelligence than traditional geographic grouping, enabling 
    targeted resource allocation and personalized market approaches.
    """)