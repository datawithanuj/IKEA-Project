# IKEA Customer Analytics & RFM Segmentation

> An end-to-end customer analytics project using **SQL**, **Python**, and **Power BI** to explore retail transactions, customer value, RFM segments, and churn.

![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black) ![Python](https://img.shields.io/badge/Python-RFM%20Analysis-3776AB?logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-Data%20Preparation-336791) ![Status](https://img.shields.io/badge/Project-Completed-2ea44f)

## Project Overview

This project turns online retail transaction data into a customer-focused analytics dashboard. SQL is used to prepare the data, Python calculates RFM metrics and customer segments, and Power BI presents the results in an interactive report.

IKEA is used as a fictional case-study theme for the dashboard. The project is not affiliated with or endorsed by IKEA, and the metrics below are not IKEA business results.

## Dashboard Preview

The Power BI report contains three pages: Sales Pulse, Customer Intelligence, and Retention Action Plan.

[![Combined preview of all three Power BI report pages](https://raw.githubusercontent.com/datawithanuj/IKEA-Project/main/IKEA_Dashboard_Preview.png)](https://raw.githubusercontent.com/datawithanuj/IKEA-Project/main/IKEA_Dashboard_Preview.png)

## Dashboard Highlights

- Sales Pulse summarizes revenue, orders, customers, and average order value.
- Customer Intelligence compares customer counts, revenue, and purchase frequency across segments.
- Retention Action Plan highlights inactive customers, value tiers, and segments for follow-up.

## Key Metrics

| KPI | Value |
|---|---:|
| Customers analyzed | **5,861** |
| Customer segments | **10** |
| Champions | **1,283 (21.9%)** |
| Champions' share of revenue | **68.1%** |
| Customers flagged as churned | **2,700 (46.1%)** |

These figures are calculated from the project's Online Retail II data and RFM logic.

## Business Questions

- Which customer segments contribute the most revenue?
- Which customers are becoming inactive or may need retention attention?
- How do recency, order frequency, and customer spending differ by segment?
- Where should customer retention efforts be prioritized?

## RFM Method

- **Recency:** days since the customer's latest purchase, using the day after the dataset's last transaction as the snapshot date.
- **Frequency:** number of distinct invoices per customer.
- **Monetary:** sum of transaction value per customer.
- Each measure receives a 1–5 quantile score. The weighted RFM score uses 35% Recency, 35% Frequency, and 30% Monetary.
- Customers are assigned to ten segments, from Champions and Loyal Customers to At Risk, Hibernating, and Lost.
- A customer is flagged as churned when Recency is greater than 90 days.

## Tools Used

- **SQL Server / SSMS** — transaction data preparation and validation
- **Python (pandas, NumPy)** — RFM calculations, scoring, segmentation, and output generation
- **Microsoft Power BI** — interactive dashboard and report pages
- **DAX** — report measures and KPI calculations

## Project Workflow

1. Prepared and cleaned the Online Retail II transaction data with SQL.
2. Calculated customer-level RFM metrics in Python.
3. Scored and assigned customers to behavioral segments.
4. Applied a 90-day inactivity rule to identify churned customers.
5. Built a Power BI report to explore overall performance and segment details.

## Repository Contents

| File | Description |
|---|---|
| [`IKEA_Project.pbix`](IKEA_Project.pbix) | Interactive Power BI dashboard; download and open in Power BI Desktop |
| [`python_rfm.py`](python_rfm.py) | Python workflow for RFM analysis and customer segmentation |
| [`README.md`](README.md) | Project overview and reproduction notes |

The raw and transaction-level CSV exports, along with generated summary CSVs, are not included. The Python script expects a locally prepared `retail_cleaned.csv` and generates the detailed Power BI transaction export and summary files in its working directory.

## Dataset

The analysis uses **Online Retail II** from the UCI Machine Learning Repository, donated by Daqing Chen. It contains anonymized online retail transactions from December 2009 through December 2011. The dataset is licensed under CC BY 4.0; review its license and attribution requirements before reuse.

## Skills Demonstrated

Data cleaning · SQL analysis · Python data processing · RFM analysis · Customer segmentation · Churn identification · Power BI dashboarding · KPI design · Business storytelling

## Conclusion

This project demonstrates a complete analytics workflow—from preparing transaction data to identifying high-value and at-risk customer segments, then presenting the results in Power BI. The analysis highlights how customer-level behavior can support more focused retention decisions.

## Author

**Anuj Devrani** · [GitHub](https://github.com/datawithanuj) · [LinkedIn](https://www.linkedin.com/in/anujdevrani)

---

*Built as part of my data analytics portfolio.*
