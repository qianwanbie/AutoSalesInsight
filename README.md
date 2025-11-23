readme: |
  # 🌍 Global Sales Analysis Dashboard  
  A Streamlit-based Interactive Data Visualization Project  
  *(EFREI Paris × WUT Joint Project)*

  ## 📌 Project Overview
  This project is an interactive **Streamlit dashboard** designed to explore and analyze global product sales data.
  It provides a complete workflow — from data cleaning to KPIs, visual insights, and clustering analysis across countries.

  The dashboard helps users understand:
  - Differences in sales across regions  
  - Pricing and product line patterns  
  - Country similarity using clustering  
  - Valuable insights for sales strategy  

  ## 🚀 Features
  ### 1. Intro Page
  High-level project overview and navigation guide.

  ### 2. Data Cleaning
  Includes:
  - Raw data preview  
  - Cleaning steps  
  - Cleaned dataset  

  ### 3. Overview Dashboard
  Displays:
  - Total sales  
  - Average price  
  - Quantity  
  - Sales by country  
  - Sales by product line  
  - Trends, heatmaps, correlations  

  ### 4. Deep Dives
  Explore:
  - Country-specific patterns  
  - Seasonal behavior  
  - Price insights  
  - Product line performance  

  ### 5. Country Clustering
  Clustering using:
  - Agglomerative Hierarchical Clustering  
  - Euclidean distance + Ward linkage  

  Visuals:
  - Each cluster grouped together  
  - Country flags + names  
  - Correlation scores  

  ## 📁 Project Structure
final_project/
├── app.py
├── README.md
├── requirements.txt
├── assets/
├── data/
├── sections/
└── utils/

shell
复制代码

## 🛠 Installation
git clone https://github.com/yourname/sales-dashboard.git
pip install -r requirements.txt
streamlit run app.py

makefile
复制代码

## 🔍 Clustering Method
**Model:** AgglomerativeClustering  
**Features:** Sales share across product lines  
**Results:** Cluster assignment + correlation score + grouped flags  

## 👤 Author
**Boyuan Liu**  
Email: your_email@example.com  
GitHub: https://github.com/yourusername  

## 👨‍🏫 Supervisor
**Dr. XXX (EFREI Paris)**  
Email: teacher_email@example.com  

## ⭐ Acknowledgements
EFREI Paris, WUT, Streamlit, Pandas, Scikit-learn  

## 📌 License
MIT License