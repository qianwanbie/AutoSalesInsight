# 🌍 Global Sales Analysis Dashboard  
A Streamlit-based Interactive Data Visualization Project  
*(EFREI Paris × WUT Joint Project)*

---

## 📌 Project Overview

This project is an interactive **Streamlit dashboard** designed to explore and analyze global product sales data.  
The dashboard provides a complete workflow — from data cleaning to KPIs, visual insights, and clustering analysis across countries.

The goal is to help users understand:
- Differences in sales performance across regions  
- Pricing and product line variations  
- Similarity patterns between countries using clustering  
- Deep-dive visualizations for decision-making  

---

## 🚀 Features

### **1. Intro Page**
Provides a high-level summary of the dashboard, data, and navigation instructions.

---

### **2. Data Cleaning**
Includes:
- Preview of raw dataset  
- Cleaning steps  
- Final cleaned dataset used for all analysis  

Cleaning includes:
- Trimming whitespace  
- Removing duplicates  
- Converting date formats  
- Normalizing column types  

---

### **3. Overview Dashboard**
Shows the global sales performance including:
- Total sales  
- Average price  
- Total quantity sold  
- Sales by country  
- Sales by product line  
- Trend charts, heatmaps, and correlation analysis  

---

### **4. Deep Dives**
Drill down into specific areas:
- Country-based sales patterns  
- Seasonal/temporal trends  
- Product line behavior  
- Price distribution and relationship with quantity  

This section provides detailed business analysis and insights.

---

### **5. Country Clustering Analysis**
This module groups countries by similarity in:
- Sales distribution  
- Product line structure  
- Normalized revenue share  

Clustering method:
- **Agglomerative Hierarchical Clustering**
- **Euclidean distance + Ward linkage**
- **Correlation score for each country**

Visualization:
- Each cluster is shown as a block  
- Includes country name, flag, and correlation score  
- Helps identify similar markets  

---

## 📊 Example Visualizations (Placeholders)

| Page | Example |
|------|---------|
| Overview | ![overview](assets/example_overview.png) |
| Deep Dive | ![deepdive](assets/example_deepdive.png) |
| Clustering | ![cluster](assets/example_cluster.png) |

*(Replace with your actual screenshots)*

---

## 📁 Project Structure

final_project/
│
├── app.py # Main Streamlit application
├── README.md # Project documentation
├── requirements.txt # Dependencies
│
├── assets/ # Logo, flags, images
│ ├── EFREI-logo.png
│ ├── WUT-Logo.png
│ ├── flags/ # Downloaded flags
│
├── data/
│ └── sales.csv # Input dataset
│
├── sections/ # Modular page components
│ ├── intro.py
│ ├── cleaning.py
│ ├── overview.py
│ ├── deepdives.py
│ └── country_cluster.py
│
└── utils/
└── prep.py # Data cleaning utilities

---

## 🛠 Installation & Usage

### **1. Clone Repository**
```bash
git clone https://github.com/yourname/sales-dashboard.git
cd sales-dashboard
2. Install Dependencies
pip install -r requirements.txt
3. Run the Streamlit App
streamlit run app.py
📑 Dataset Description

The dataset includes:

Country

Product line

Price

Quantity

Date

Revenue

Market share metrics

And other related attributes

Size: ~ few thousand rows

Data is used to compare sales across regions and perform clustering.

🔍 Clustering Methodology

Model Used:

AgglomerativeClustering (Scikit-learn)

Features Used:

Sales share across each product line

Standardized country-level metrics

Output:

Cluster assignments 1 → 4

Correlation score for each country

Visual grouping + country flag display

This helps identify:

Similar markets

Outliers

Regional grouping patterns

👤 Author

Boyuan Liu
📧 Email: your_email@example.com

🌐 GitHub: https://github.com/yourusername

👨‍🏫 Supervisor

Dr. XXX (EFREI Paris)
📧 Email: teacher_email@example.com

⭐ Acknowledgements

Thanks to:

EFREI Paris

Wuhan University of Technology (WUT)

Streamlit

Pandas & Scikit-learn

Plotly

📌 License

MIT License.
Feel free to use and modify for study purposes.


---