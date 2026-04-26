# Hotel Companies Financial & Stock Performance Dashboard

## 1. Project Overview

This project is an interactive Streamlit dashboard that analyzes how the financial performance of major global hotel companies aligns with their stock market performance over time.

The dashboard focuses on four hotel companies:

- Hilton Worldwide Holdings
- Hyatt Hotels Corporation
- Marriott International
- InterContinental Hotels Group (IHG)

## 2. Analytical Problem

The main analytical question is:

**Do stronger financial fundamentals appear to align with stronger annual stock returns for major hotel companies?**

The project compares annual financial metrics with annual stock returns to evaluate whether accounting performance and market performance move in similar or different directions.

## 3. Target Audience

The target audience is students, instructors, and beginner investors who want to understand how company financial performance can be compared with stock market performance.

The dashboard is designed to make financial ratios and stock returns easier to explore through interactive charts and short interpretation outputs.

## 4. Data Sources

The project uses data from WRDS:

- **Compustat**: annual financial fundamentals
- **CRSP**: monthly stock returns

Monthly stock returns are compounded into annual returns so that stock performance can be compared with annual financial performance.

## 5. Methods

The project uses Python to clean, transform, analyze, and visualize the data.

Main steps include:

- selecting four major hotel companies
- cleaning and preparing financial and stock data
- calculating financial metrics such as ROA, ROE, profit margin, EPS, P/E ratio, P/B ratio, asset turnover, and free cash flow
- compounding monthly stock returns into annual returns
- aligning financial metrics and stock returns by company and year
- building an interactive Streamlit dashboard

## 6. App Features

The Streamlit app includes:

- company selection
- year range filtering
- financial metric selection
- financial performance comparison charts
- annual stock return comparison charts
- financial-market performance alignment analysis
- interpretation summary for selected company, year, and metric
- methodology section
- filtered dataset preview

## 7. What to Expect

When you open the dashboard, you can:

- choose a hotel company and a year range
- select a financial metric to compare across companies
- view interactive charts for both financial metrics and annual stock returns
- examine how percentage-based metrics like ROA, ROE, and profit margin align with market performance
- explore an interpretation summary that explains trends and relative performance

## 8. Prerequisites

- Python 3.10 or newer
- `pip` installed
- a working Python environment (virtualenv, venv, or conda recommended)

## 8. Project Structure

- `app.py` — main Streamlit dashboard
- `requirements.txt` — Python dependencies
- `top4_hotels_annual_2018_2025.csv` — input data file
- `.streamlit/` — optional Streamlit configuration folder

## 9. How to Run the App

Install the required packages and run the app:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure the data file `top4_hotels_annual_2018_2025.csv` is located in the project root next to `app.py`.

## 10. Limitations

- This project focuses only on four hotel companies, so the results should not be generalized to the whole hotel industry.
- Stock return data for 2025 are not available because full-year market data are not yet complete.
- Some financial metrics, such as EPS, P/E ratio, P/B ratio, and free cash flow, are useful for analysis but are not directly comparable with stock returns on the same scale. Therefore, the alignment section focuses on percentage-based metrics such as ROA, ROE, and profit margin.

## 11. Author
Karina Ermakova
