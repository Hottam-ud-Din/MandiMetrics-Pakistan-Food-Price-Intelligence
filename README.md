# 🌾 MandiMetrics: Pakistan Food Price Intelligence

**Project by:** Hottam Ud Din  
**Data Source:** [World Food Programme (WFP)](https://data.humdata.org/dataset/wfp-food-prices-for-pakistan)

---

## 📌 Project Overview
**MandiMetrics** is a comprehensive data intelligence dashboard designed to monitor, analyze, and forecast food security trends in Pakistan. 

In a country facing economic volatility, understanding the difference between **supply-shock inflation** and **currency devaluation** is critical. This project utilizes historical data from **2004 to 2025** to provide actionable insights into price anomalies, seasonal harvest patterns, and regional disparities across Punjab, Sindh, Balochistan, and Khyber Pakhtunkhwa.

## 🚀 Live Demo
Check out the live application here:  
👉 **[Click to Open Dashboard]((https://mandimetrics-pakistan-food-price-intelligence-gzrtr4ywqzendcft.streamlit.app/))**

---

## 📊 Key Features

### 1. 📈 Inflation vs. Devaluation Analysis
* **The Problem:** Prices go up, but is it because of a wheat shortage or because the Rupee is weak?
* **The Solution:** We plot the price of commodities in both **PKR (Local Currency)** and **USD (Global Benchmark)**.
* **Insight:** If PKR spikes but USD remains flat, the issue is currency devaluation, not a food shortage.

### 2. 🤖 AI Price Forecasting (Prophet)
* **Technology:** Uses **Facebook Prophet**, a Machine Learning model optimized for time-series data with strong seasonal effects.
* **Capability:** Generates a **12-month forward-looking forecast** for staples like Wheat Flour, Sugar, and Rice.
* **Regional Specificity:** Trains separate models for each province to capture local market dynamics.

### 3. 🗺️ Geospatial Intelligence
* **Interactive Maps:** A heatmap visualizing the most expensive cities in Pakistan in real-time.
* **Regional Disparity:** Box plots that reveal the cost-of-living gap between agricultural hubs (e.g., Lahore) and remote areas (e.g., Quetta).

### 4. 📅 Seasonality Detection
* Automatic detection of price drops during **Rabi** (Spring) and **Kharif** (Autumn) harvest seasons.

---

## 📂 Project Structure
```text
MandiMetrics/
├── app.py                   # Main Streamlit Application code
├── analysis.ipynb           # Jupyter Notebook for deep-dive EDA & modeling
├── wfp_food_prices_pak.csv  # Raw dataset (WFP)
├── requirements.txt         # Project dependencies
└── README.md                # Documentation
````

## 🛠️ Tech Stack

  * **Python:** Core logic and data manipulation (Pandas, NumPy).
  * **Streamlit:** Frontend framework for the interactive web app.
  * **Plotly:** Interactive visualization engine (Maps, Line Charts).
  * **Facebook Prophet:** Time-series forecasting library.
  * **IPyWidgets:** Interactive components for the notebook analysis.

-----

## ⚙️ How to Run Locally

1.  **Clone the Repository**

    ```bash
    git clone [https://github.com/YourUsername/MandiMetrics.git](https://github.com/YourUsername/MandiMetrics.git)
    cd MandiMetrics
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.

    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the App**

    ```bash
    streamlit run app.py
    ```

-----

## 📅 Data Source & Credits

  * **Dataset:** [WFP Food Prices for Pakistan](https://data.humdata.org/dataset/wfp-food-prices-for-pakistan)
  * **Provider:** Humanitarian Data Exchange (HDX)
  * **Frequency:** Updated monthly covering major cities and commodities.

-----

## 👨‍💻 Author

**Hottam Ud Din** *Aspiring Data Scientist | Final Year BS Data Science Student*

[LinkedIn](https://www.google.com/search?q=YOUR_LINKEDIN_URL) | [GitHub](https://www.google.com/search?q=YOUR_GITHUB_URL)

```

### 🔔 Important Final Step:
Don't forget to **replace the placeholder links** (the parts that say `REPLACE_WITH_YOUR_...`) with your actual:
1.  Streamlit App URL.
2.  GitHub Profile URL.
3.  LinkedIn Profile URL.

This README is now fully documented and ready for professional review!
```

