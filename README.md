# Data files and refresh

This folder contains compact summary outputs from the supplied project: one row per customer in the customer summary and aggregate metrics in the segment summary.

Large data files are intentionally excluded:

- `retail_cleaned.csv` (~110 MB): cleaned transaction export.
- `rfm_transactions_powerbi.csv` (~140 MB): transaction-level Power BI source with RFM attributes.
- Raw Online Retail II CSVs / ZIP (~15 MB): available from the UCI Machine Learning Repository.

To regenerate, obtain the UCI data, recreate `retail_cleaned.csv` with the SQL cleaning workflow, then run `python/python_rfm.py` from a directory containing that input. The script writes generated CSVs to its current working directory. Point Power BI to the newly generated transaction export and refresh.

The summary CSVs are derived outputs; their values may change if the source data or RFM logic changes.
