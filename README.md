# Auto Sales Analytics Dashboard

This project is an interactive **Auto Sales Analytics Dashboard** built with **Streamlit**.  
It provides a complete analytical workflow from **data preprocessing** to **advanced market segmentation**, 
enabling comprehensive exploration of automotive sales patterns and strategic business insights.

## FEATURES

### Data Pipeline
- **Data Introduction**: Dataset overview and structure explanation
- **Data Cleaning**: Automated preprocessing, duplicate removal, and format standardization
- **Quality Control**: Statistical summaries and data validation

### Analytical Modules
- **Overview Dashboard**: 
  - Real-time KPIs (total sales, average price, quantity metrics)
  - Interactive sales trends with dual-axis charts
  - Geographic performance analysis by country
  - Product line distribution and pricing scatter plots

- **Deep Dive Analysis**:
  - Country comparison: Australia vs France sales trends
  - Interactive choropleth maps by month
  - Seasonal heatmaps (2018 vs 2019)
  - Price vs MSRP ratio analysis
  - Customer retention and behavioral analytics

- **Country Clustering**:
  - Hierarchical clustering based on product preference patterns
  - Interactive dendrogram and heatmap visualizations
  - Cluster profiling with radar charts
  - Data-driven strategic recommendations

- **Strategic Conclusions**:
  - Consolidated insights from all analyses
  - Actionable business recommendations
  - Market segmentation strategies

## PROJECT ARCHITECTURE

auto_sales_dashboard/
├── app.py # Main application entry point
├── README.md # Project documentation
├── requirements.txt # Python dependencies
├── assets/ # Static resources (logos)
│ ├── EFREI-logo.png
│ └── WUT-Logo.png
├── data/ # Dataset storage
│ └── Auto Sales data.csv
├── sections/ # Application modules
│ ├── intro.py # Project introduction and navigation
│ ├── data_cleaning.py # Data preprocessing interface
│ ├── overview.py # Dashboard with KPIs and trends
│ ├── deep_dives.py # Advanced analytical insights
│ ├── country_cluster.py # Market segmentation analysis
│ └── conclusions.py # Strategic insights and recommendations
└── utils/ # Core functionality
├── io.py # Data loading utilities
├── prep.py # Data preprocessing functions
└── viz.py # Visualization components and charts


## QUICK START

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd auto_sales_dashboard

# Install dependencies
pip install -r requirements.txt
```
### Launch Application
```bash
streamlit run app.py
```
### TECHNICAL STACK
  - Frontend: Streamlit 1.51.0

  - Data Processing: Pandas, NumPy

  - Visualization: Plotly, Altair, Matplotlib, Seaborn

  - Clustering: SciPy, Scikit-learn

  - Interactive Components: Streamlit widgets

### DATA SOURCES
  - Primary dataset: Auto Sales data.csv

  - Automotive sales transactions across multiple countries

  - Product line information and pricing data

  - Temporal sales records

### CONTRIBUTORS
- **Boyuan Liu** - Primary Developer

- **Mano Mathew** - Project Supervisor