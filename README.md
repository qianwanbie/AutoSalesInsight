# Sales Dashboard (Streamlit)

This project is an interactive **Sales Dashboard** built with **Streamlit**.  
It provides a complete workflow from **data cleaning** to **visual analytics**, 
including:

 ## 🚀 Features
- **Data Cleaning Page**: Upload, preview, and preprocess raw sales data.
    - **Overview Dashboard**:  
      - KPIs (total sales, average price, quantity)
      - Sales by product line  
      - Sales by country  
      - Time-series trends  
    - **Deep Dive Analysis**:
      - Specific country insights
      - Seasonal trends
      - Pricing exploration
    - **Country Clustering**:
      - Group countries by similarity in sales patterns  
      - Visualize clusters with charts

## 📁 Project Structure
    ```
    final_project/
    ├── app.py
    ├── README.md
    ├── requirements.txt
    ├── assets/
    ├── data/
    ├── sections/
    │   ├── overview.py
    │   ├── deep_dives.py
    │   ├── clustering.py
    │   └── cleaning.py
    └── utils/
        ├── loaders.py
        ├── charts.py
        └── helpers.py
    ```

## ▶️ Run the App

    streamlit run app.py


## 📦 Requirements
    See `requirements.txt` in this YAML file.

## ✨ Author
    Boyuan Liu