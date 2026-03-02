# Telco Customer Churn – End-to-End Azure Pipeline

This project implements an end-to-end customer churn analysis for a telecom company,
from Python ingestion and Azure data pipeline to SQL modelling and Power BI dashboards.

## 1. Business problem

Telecom providers lose a significant share of their recurring revenue when customers churn.  
The goal of this project is to:
- Measure churn and monthly revenue at risk.
- Identify high-risk customer segments.
- Provide interactive dashboards to support targeted retention actions.

## 2. Architecture overview

The solution is built with the following components:

- **Python ingestion pipeline** – Reads the Telco Customer Churn dataset, writes a raw CSV, applies cleaning in a transform step, and saves an analysis-ready processed CSV. Configuration is stored in a JSON file and the script uses structured logging.
- **Azure Blob Storage** – Stores raw and processed churn files in separate folders (`raw/` and `processed/`).
- **Azure Data Factory** – A `Copy Data` pipeline (`pl_blob_to_sql_telco`) that loads the latest processed file from Blob into Azure SQL and runs on a daily schedule via a trigger.
- **Azure SQL Database** – Hosts the `TelcoCustomers` table plus views and stored procedures for churn KPIs and risk segmentation.
- **Excel PivotTables** – Used to validate churn patterns by contract type, tenure segment and payment method before automating the pipeline.
- **Power BI** – Interactive dashboards including an executive overview, segment analysis, and a Risk & Retention page with drill-through customer details.

## 3. Repository structure

```text
python_pipeline/      # Python ingestion script, config template and dependencies
sql/                  # Table, view and stored procedure scripts
azure/                # Documentation and screenshots for Blob & ADF
powerbi/              # Power BI report files (pbix) and notes
docs/                 # Data dictionary and high-level project documentation
