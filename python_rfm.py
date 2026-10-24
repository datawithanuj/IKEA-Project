# ================================================================
# IKEA CUSTOMER ANALYTICS | RFM Analysis & Customer Segmentation
# Input:   retail_cleaned.csv (prepared from the SQL workflow)
# Outputs: rfm_transactions_powerbi.csv, rfm_customer_summary.csv, rfm_segment_summary.csv
# ================================================================

import pandas as pd
import numpy as np
from datetime import timedelta

# ----------------------------------------------------------------
# 1. LOAD DATA
# ----------------------------------------------------------------
print("=" * 55)
print("  IKEA CUSTOMER ANALYTICS — RFM SEGMENTATION ANALYSIS")
print("=" * 55)

# Update path if needed
df = pd.read_csv("retail_cleaned.csv", parse_dates=["InvoiceDate"])

print(f"\n✅ Loaded {len(df):,} rows | {df['Customer_ID'].nunique():,} customers")
print(f"   Date range: {df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}")

# ----------------------------------------------------------------
# 2. SET SNAPSHOT DATE
# We use 1 day after last transaction as "today" for recency calc
# ----------------------------------------------------------------
SNAPSHOT_DATE = df["InvoiceDate"].max() + timedelta(days=1)
print(f"\n📅 Snapshot date (reference for Recency): {SNAPSHOT_DATE.date()}")

# ----------------------------------------------------------------
# 3. CALCULATE RFM METRICS PER CUSTOMER
# ----------------------------------------------------------------
rfm = df.groupby("Customer_ID").agg(
    Last_Purchase  = ("InvoiceDate",  "max"),
    Frequency      = ("Invoice",      "nunique"),   # unique orders, not rows
    Monetary       = ("TotalAmount",  "sum"),
    Total_Items    = ("Quantity",      "sum"),
    Avg_Order_Val  = ("TotalAmount",  "mean"),
    First_Purchase = ("InvoiceDate",  "min"),
    Countries      = ("Country",      "nunique"),
    Unique_Products= ("StockCode",    "nunique"),
).reset_index()

# Recency = days since last purchase
rfm["Recency"] = (SNAPSHOT_DATE - rfm["Last_Purchase"]).dt.days

# Customer lifespan in days
rfm["Lifespan_Days"] = (rfm["Last_Purchase"] - rfm["First_Purchase"]).dt.days

# Round monetary values
rfm["Monetary"]      = rfm["Monetary"].round(2)
rfm["Avg_Order_Val"] = rfm["Avg_Order_Val"].round(2)

print(f"\n📊 RFM Metrics Summary:")
print(rfm[["Recency", "Frequency", "Monetary"]].describe().round(1))

# ----------------------------------------------------------------
# 4. RFM SCORING (1-5 scale)
# R: Lower recency = better → score 5
# F: Higher frequency = better → score 5
# M: Higher monetary = better → score 5
# ----------------------------------------------------------------

# Custom quantile scorer that handles ties cleanly
def score_quantile(series, reverse=False, labels=[1, 2, 3, 4, 5]):
    """Assign scores using quantile bins. reverse=True means low value = high score."""
    try:
        scored = pd.qcut(
            series.rank(method="first", ascending=not reverse),
            q=5,
            labels=labels
        ).astype(int)
    except Exception:
        scored = pd.cut(series, bins=5, labels=labels).astype(int)
    return scored

rfm["R_Score"] = score_quantile(rfm["Recency"],   reverse=True)   # low recency → score 5
rfm["F_Score"] = score_quantile(rfm["Frequency"],  reverse=False)  # high freq → score 5
rfm["M_Score"] = score_quantile(rfm["Monetary"],   reverse=False)  # high spend → score 5

# Composite RFM Score (weighted: R=35%, F=35%, M=30%)
rfm["RFM_Score"] = (
    rfm["R_Score"] * 0.35 +
    rfm["F_Score"] * 0.35 +
    rfm["M_Score"] * 0.30
).round(2)

# Combined score string e.g. "555", "321"
rfm["RFM_Code"] = (
    rfm["R_Score"].astype(str) +
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

# ----------------------------------------------------------------
# 5. CUSTOMER SEGMENTATION
# Segments are based on R + F scores (M adds nuance within)
# Slightly different segments vs standard model
# ----------------------------------------------------------------

def assign_segment(row):
    r = row["R_Score"]
    f = row["F_Score"]
    m = row["M_Score"]
    rfm = row["RFM_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"            # Best customers — recent, frequent, high spend
    elif r >= 3 and f >= 3 and m >= 3:
        return "Loyal Customers"      # Consistently good, not quite champions
    elif r >= 4 and f <= 2:
        return "Promising"            # Recently active but low orders — potential growth
    elif r >= 3 and f >= 2 and m <= 2:
        return "Potential Loyalists"  # Decent recency & frequency, lower spend
    elif r == 3 and f <= 2:
        return "Need Attention"       # Average recency, low engagement
    elif r == 2 and f >= 3:
        return "At Risk"              # Used to buy frequently, now gone quiet
    elif r == 2 and f <= 2:
        return "Slipping Away"        # Declining activity, need re-engagement
    elif r == 1 and f >= 3:
        return "Can't Lose Them"      # High frequency historically but gone dark
    elif r == 1 and f <= 2 and m >= 3:
        return "Hibernating"          # Spent well before, haven't returned
    else:
        return "Lost"                 # Low recency, low frequency, low spend


rfm["Segment"] = rfm.apply(assign_segment, axis=1)

# ----------------------------------------------------------------
# 6. CHURN FLAG
# Definition: No purchase in last 90 days
# ----------------------------------------------------------------
rfm["Is_Churned"] = (rfm["Recency"] > 90).astype(int)
rfm["Churn_Status"] = rfm["Is_Churned"].map({1: "Churned", 0: "Active"})

# ----------------------------------------------------------------
# 7. CUSTOMER VALUE TIER
# Based on Monetary percentile
# ----------------------------------------------------------------
rfm["Value_Tier"] = pd.qcut(
    rfm["Monetary"],
    q=[0, 0.25, 0.50, 0.75, 0.90, 1.0],
    labels=["Bronze", "Silver", "Gold", "Platinum", "Diamond"]
)

# ----------------------------------------------------------------
# 8. ANALYSIS SUMMARY
# ----------------------------------------------------------------
print("\n" + "=" * 55)
print("  SEGMENT BREAKDOWN")
print("=" * 55)

seg_summary = rfm.groupby("Segment").agg(
    Customers        = ("Customer_ID",  "count"),
    Pct_Customers    = ("Customer_ID",  lambda x: round(len(x)/len(rfm)*100, 1)),
    Avg_Recency      = ("Recency",      "mean"),
    Avg_Frequency    = ("Frequency",    "mean"),
    Total_Revenue    = ("Monetary",     "sum"),
    Pct_Revenue      = ("Monetary",     lambda x: round(x.sum()/rfm["Monetary"].sum()*100, 1)),
    Avg_Order_Value  = ("Avg_Order_Val","mean"),
    Churned_Count    = ("Is_Churned",   "sum"),
).reset_index()

seg_summary["Avg_Recency"]     = seg_summary["Avg_Recency"].round(0).astype(int)
seg_summary["Avg_Frequency"]   = seg_summary["Avg_Frequency"].round(1)
seg_summary["Total_Revenue"]   = seg_summary["Total_Revenue"].round(0)
seg_summary["Avg_Order_Value"] = seg_summary["Avg_Order_Value"].round(2)

print(seg_summary.to_string(index=False))

print("\n" + "=" * 55)
print("  CHURN SUMMARY")
print("=" * 55)
churn = rfm["Churn_Status"].value_counts()
churn_pct = round(rfm["Is_Churned"].mean() * 100, 2)
print(churn)
print(f"\nOverall Churn Rate: {churn_pct}%")

print("\n" + "=" * 55)
print("  VALUE TIER BREAKDOWN")
print("=" * 55)
print(rfm.groupby("Value_Tier")["Monetary"].agg(["count","sum","mean"]).round(2))

# ----------------------------------------------------------------
# 9. MERGE RFM BACK TO TRANSACTION LEVEL
# This is the table Power BI will use
# ----------------------------------------------------------------
df_final = df.merge(
    rfm[[
        "Customer_ID", "Segment", "RFM_Score", "RFM_Code",
        "R_Score", "F_Score", "M_Score",
        "Recency", "Frequency", "Monetary",
        "Avg_Order_Val", "Lifespan_Days",
        "Is_Churned", "Churn_Status", "Value_Tier"
    ]],
    on="Customer_ID",
    how="left"
)

# ----------------------------------------------------------------
# 10. SAVE OUTPUTS
# ----------------------------------------------------------------

# Main file for Power BI
df_final.to_csv("rfm_transactions_powerbi.csv", index=False)
print(f"\n✅ Saved: rfm_transactions_powerbi.csv ({len(df_final):,} rows)")

# Summary file for Power BI segment table
rfm.to_csv("rfm_customer_summary.csv", index=False)
print(f"✅ Saved: rfm_customer_summary.csv ({len(rfm):,} customers)")

# Segment summary
seg_summary.to_csv("rfm_segment_summary.csv", index=False)
print(f"✅ Saved: rfm_segment_summary.csv")

print("\n" + "=" * 55)
print("  DONE! Load these 2 files into Power BI:")
print("  1. rfm_transactions_powerbi.csv")
print("  2. rfm_customer_summary.csv")
print("=" * 55)
