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

4. Pipeline flow
The Python script loads the Telco Customer Churn dataset, saves a raw copy, applies cleaning (type fixes, tenure segments, SeniorCitizen mapping) and writes a processed CSV.

Raw and processed files are uploaded to Azure Blob Storage under raw/ and processed/ folders.

An Azure Data Factory pipeline (pl_blob_to_sql_telco) truncates the TelcoCustomers table and copies the latest processed file from Blob into Azure SQL.

SQL views calculate churn rate, churned monthly revenue, tenure buckets and a rule-based risk segment (High / Medium / Low).

Power BI connects to the SQL views and exposes churn KPIs through several report pages, including a Risk & Retention page focused on high-risk customers.

A daily ADF trigger (tr_daily_telco_refresh) keeps the SQL layer and Power BI reports up to date.

5. Key features
Production-style Python ingestion with JSON configuration, structured logging and separate raw/processed layers.

API-ready design for the ingestion script using a requests-style pattern.

Rule-based High / Medium / Low risk segment using contract type, tenure, internet service and payment method.

Parameterised SQL stored procedures for churn KPIs by contract and by risk segment.

Azure Data Factory copy pipeline with daily schedule and truncate-before-load strategy.

Power BI Risk & Retention page showing churn rate and lost monthly revenue by risk segment, plus drill-through customer details.

6. How to run locally (simplified)
Clone this repository.

Download the Telco Customer Churn dataset from Kaggle and place the CSV in python_pipeline/data_source/.

Copy python_pipeline/config.template.json to config.json and fill in your own Azure Blob connection string and container names.


Install Python dependencies:


pip install -r python_pipeline/requirements.txt
Run the ingestion script:


python python_pipeline/main.py
Deploy the SQL scripts in the sql/ folder to your Azure SQL Database.

Point your Power BI report to the Azure SQL views used in this project.

This project is designed as a portfolio piece to demonstrate end-to-end data skills across Python, Azure, SQL and Power BI for churn analysis.



3. Sayfanın en altına in, “Commit changes” bölümünde:
   - Commit message: `Add project README`  
   - “Commit directly to the main branch” seçili kalsın.  
   - **Commit changes** butonuna tıkla.
