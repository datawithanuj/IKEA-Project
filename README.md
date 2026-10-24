# IKEA Customer Analytics & RFM Segmentation

An independent customer analytics project built with SQL, Python and Power BI. It uses the public Online Retail II transaction dataset to study customer purchasing behavior, customer value, retention and churn through RFM analysis.

> **Project note:** IKEA is used as a fictional case-study theme for this portfolio dashboard. This project is not affiliated with or endorsed by IKEA. All metrics come from the public, anonymized retail dataset and do not represent IKEA's actual business.

## Dashboard

Download [`IKEA_Project.pbix`](IKEA_Project.pbix) and open it in Power BI Desktop.

The report is organized into three pages:

- **Home** — dashboard landing page and navigation.
- **Business Overview** — customer and revenue overview, segment and churn summaries, and time/geography views.
- **RFM Analysis** — customer segmentation and RFM performance.

The PBIX is the interactive report. GitHub does not render Power BI reports in the browser; download the file to view and interact with it in Power BI Desktop.

## Analysis

The Python workflow calculates customer-level:

- **Recency:** days since the customer's latest purchase, measured from one day after the last transaction in the dataset.
- **Frequency:** number of distinct invoices.
- **Monetary:** total transaction value.

Each RFM component is scored from 1 to 5 using quantile groups. The composite score weights Recency at 35%, Frequency at 35% and Monetary at 30%. Customers are assigned to ten segments, including Champions, Loyal Customers, At Risk, Promising, Hibernating and Lost. Churn is flagged when Recency is over 90 days.

### Snapshot from the included summary

- **5,861 customers** are represented.
- **Champions:** 1,283 customers (21.9%) and 68.1% of recorded revenue.
- **90-day churn rule:** 2,700 customers are flagged as churned (about 46.1%).

These are results from this project's supplied data and logic; they are not IKEA business figures. See [`rfm_segment_summary.csv`](rfm_segment_summary.csv) for all ten segments and their metrics.

## Project files

- [`IKEA_Project.pbix`](IKEA_Project.pbix) — interactive Power BI report.
- [`python_rfm.py`](python_rfm.py) — customer RFM calculation, scoring, segmentation and export workflow.
- [`rfm_customer_summary.csv`](rfm_customer_summary.csv) — customer-level RFM metrics and segment assignments.
- [`rfm_segment_summary.csv`](rfm_segment_summary.csv) — aggregated metrics by segment.

Large raw and transaction-level exports are not included because they make the repository unnecessarily large. The Python script reads `retail_cleaned.csv` from its working directory and writes the detailed Power BI transaction export and both summaries there.

## Data and tools

The source is **Online Retail II** from the UCI Machine Learning Repository, donated by Daqing Chen. It contains anonymized transactions from December 2009 through December 2011. The dataset is licensed under CC BY 4.0; check the source license and attribution requirements before reuse.

Tools used: SQL Server / SSMS, Python (pandas and NumPy), Power BI Desktop and DAX.

## Reproduce the analysis

1. Get Online Retail II from the UCI Machine Learning Repository.
2. Use the SQL cleaning workflow to prepare `retail_cleaned.csv` with the columns `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer_ID`, `Country` and `TotalAmount`.
3. Install the Python dependencies: `pandas` and `numpy`.
4. Run `python python_rfm.py` from the directory containing `retail_cleaned.csv`.
5. In Power BI Desktop, point the report to the generated `rfm_transactions_powerbi.csv` and refresh.
