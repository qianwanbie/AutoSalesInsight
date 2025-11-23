import streamlit as st

def show():
    """
    Intro page with enhanced layout
    """
    # Title with emoji
    st.title("📊 Welcome to the Sales Dashboard")

    # Logo row (optional)
    col1, col2 = st.columns(2)
    with col1:
        st.image("assets/EFREI-logo.png", width=210)
    with col2:
        st.image("assets/WUT-Logo.png", width=210)

    st.markdown("---")  # separator

    # Intro description in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Key Features")
        st.markdown("""
        - **KPIs & Trends**: total sales, avg. price, quantity  
        - **Sales by Country & Product Line**  
        - **Deep Dives**: country-specific, seasonal, pricing  
        - **Clustering Analysis**: identify similar sales patterns  
        """)
    with col2:
        st.subheader("🛠 How to Use")
        st.markdown("""
        1. Use the **sidebar** to navigate pages  
        2. Start with **Data Cleaning**  
        3. Explore **Overview** for key metrics  
        4. Dive into **Deep Dives** for detailed insights  
        5. Check **Country Clustering** for patterns across regions  
        """)