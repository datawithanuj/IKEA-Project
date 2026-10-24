# IKEA Gifting | Customer Analytics & RFM Segmentation

An end-to-end customer analytics portfolio project using SQL, Python and Power BI. This independent learning project is inspired by the linked Mansi Goel tutorial; its implementation, analysis and dashboard are the author's own work. “IKEA Gifting” is fictional, not affiliated with or endorsed by IKEA. Findings come from the public, anonymized dataset and do not describe IKEA's actual business.

## Dashboard

Download [`IKEA_Project.pbix`](IKEA_Project.pbix) and open it in Power BI Desktop. The report includes a home/navigation page, business overview and RFM analysis.

## Questions explored

- Which customer segments contribute most to revenue?
- Which previously valuable customers may be at risk of lapsing?
- How do customer value and churn vary over time and geography?
- What retention actions suit each RFM segment?

## Analysis snapshot

The supplied segment summary reports 5,861 customers. Champions are 21.9% of customers and contribute 68.1% of revenue. Churn is defined as more than 90 days of inactivity; segment counts total 2,700 churned customers (about 46.1%). These figures come from the supplied exports and may differ from the tutorial.

See [`rfm_segment_summary.csv`](rfm_segment_summary.csv) for all segments and measures.

## Files

- `IKEA_Project.pbix` — Power BI dashboard
- `python_rfm.py` — RFM analysis and segmentation script
- `rfm_customer_summary.csv`, `rfm_segment_summary.csv` — compact derived summaries

Large raw and transaction-level CSV exports are not committed. This keeps the repository practical to clone; the raw dataset is publicly available from UCI and derived files can be regenerated locally.

## Data source and tools

Online Retail II, UCI Machine Learning Repository, donated by Daqing Chen. The dataset covers December 2009–December 2011 and is licensed under CC BY 4.0. Review the license before reuse. The project uses SQL Server/SSMS, Python (pandas and NumPy), Power BI Desktop and DAX.

## Reproduction

1. Download Online Retail II from the UCI Machine Learning Repository.
2. Use the SQL cleaning workflow to create `retail_cleaned.csv` with `Invoice`, `StockCode`, `Description`, `Quantity`, `InvoiceDate`, `Price`, `Customer_ID`, `Country`, and `TotalAmount` columns.
3. Install Python 3, pandas and NumPy.
4. Place `retail_cleaned.csv` in the current directory and run `python python_rfm.py`.
5. In Power BI Desktop, update the source path to the generated `rfm_transactions_powerbi.csv` and refresh.

Tutorial reference: [Mansi Goel's IKEA Gifting project walkthrough](https://youtu.be/LQa0SiuZfhA). This is an independently implemented learning project based on ideas and workflow studied in that walkthrough.
