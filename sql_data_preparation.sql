-- ============================================================
-- IKEA CUSTOMER ANALYTICS
-- SQL data preparation | MySQL 8.0+ / MySQL Workbench
--
-- Workflow:
-- 1. Update the two CSV paths below.
-- 2. Run this script with MySQL 8.0+ and LOCAL INFILE enabled.
-- 3. Export the final SELECT result as retail_cleaned.csv.
-- 4. Place retail_cleaned.csv beside python_rfm.py and run the Python script.
--
-- The raw data files are not included in this repository.
-- ============================================================

-- 1. Create and select the project database
CREATE DATABASE IF NOT EXISTS ikea_project;
USE ikea_project;

-- 2. Create staging tables for the two source CSV files
CREATE TABLE IF NOT EXISTS page1 (
    Invoice      VARCHAR(20),
    StockCode    VARCHAR(30),
    Description  VARCHAR(300),
    Quantity     INT,
    InvoiceDate  VARCHAR(30),
    Price        DECIMAL(12,4),
    Customer_ID  VARCHAR(20),
    Country      VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS page2 LIKE page1;

-- Clear staging tables so rerunning the imports does not duplicate rows.
TRUNCATE TABLE page1;
TRUNCATE TABLE page2;

-- 3. Import the two CSV files
-- Replace C:/path/to/ with the folder containing your downloaded source files.
LOAD DATA LOCAL INFILE 'C:/path/to/online_retail_II page 1.csv'
INTO TABLE page1
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

LOAD DATA LOCAL INFILE 'C:/path/to/online_retail_II page 2.csv'
INTO TABLE page2
CHARACTER SET latin1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- 4. Combine both imported files
DROP TABLE IF EXISTS combined;

CREATE TABLE combined AS
SELECT * FROM page1
UNION ALL
SELECT * FROM page2;

SELECT COUNT(*) AS total_rows
FROM combined;

-- 5. Clean and enrich the transaction data
DROP TABLE IF EXISTS retail_cleaned;

CREATE TABLE retail_cleaned AS
SELECT
    Invoice,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    Price,
    Customer_ID,
    Country,
    TotalAmount,
    InvoiceDay,
    InvoiceYear,
    InvoiceMonth,
    InvoiceQuarter
FROM (
    SELECT
        Invoice,
        StockCode,
        TRIM(Description) AS Description,
        Quantity,
        STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i') AS InvoiceDate,
        ROUND(Price, 2) AS Price,
        TRIM(Customer_ID) AS Customer_ID,
        Country,
        ROUND(Quantity * Price, 2) AS TotalAmount,
        DATE(STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i')) AS InvoiceDay,
        YEAR(STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i')) AS InvoiceYear,
        MONTH(STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i')) AS InvoiceMonth,
        QUARTER(STR_TO_DATE(InvoiceDate, '%d-%m-%Y %H:%i')) AS InvoiceQuarter,
        ROW_NUMBER() OVER (
            PARTITION BY Invoice, StockCode, Quantity, InvoiceDate, Customer_ID
            ORDER BY Invoice
        ) AS rn
    FROM combined
    WHERE Customer_ID IS NOT NULL
      AND TRIM(Customer_ID) <> ''
      AND Description IS NOT NULL
      AND TRIM(Description) <> ''
      AND Invoice NOT LIKE 'C%'
      AND Quantity > 0
      AND Price > 0
      AND StockCode NOT IN (
          'POST', 'DOT', 'M', 'm', 'D', 'S', 'C2',
          'BANK CHARGES', 'AMAZONFEE'
      )
) AS cleaned_rows
WHERE rn = 1;

-- 6. Add a row ID and indexes for common customer/date lookups
ALTER TABLE retail_cleaned
    ADD COLUMN id INT AUTO_INCREMENT PRIMARY KEY FIRST;

CREATE INDEX idx_cust ON retail_cleaned (Customer_ID);
CREATE INDEX idx_date ON retail_cleaned (InvoiceDate);

-- 7. Validate the cleaned data
SELECT COUNT(*) AS clean_rows
FROM retail_cleaned;

SELECT
    MIN(InvoiceDate) AS from_date,
    MAX(InvoiceDate) AS to_date,
    COUNT(DISTINCT Customer_ID) AS customers
FROM retail_cleaned;

-- 8. Export this result set as retail_cleaned.csv for python_rfm.py
SELECT
    Invoice,
    StockCode,
    Description,
    Quantity,
    InvoiceDate,
    Price,
    Customer_ID,
    Country,
    TotalAmount,
    InvoiceDay,
    InvoiceYear,
    InvoiceMonth,
    InvoiceQuarter
FROM retail_cleaned
ORDER BY InvoiceDate;
