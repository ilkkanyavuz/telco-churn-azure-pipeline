# Azure Data Factory pipeline

## Pipeline

- Name: `pl_blob_to_sql_telco`
- Type: Copy pipeline that loads processed churn files from Azure Blob into Azure SQL.

Main activity:
- `CopyProcessedToTelcoCustomers` (Copy Data activity)
  - Source: `processed/` folder in `telco-churn` Blob container
  - Sink: Azure SQL table `dbo.TelcoCustomers`
  - Pre-copy script: `TRUNCATE TABLE dbo.TelcoCustomers;`

## Trigger

- Name: `tr_daily_telco_refresh`
- Type: Schedule trigger
- Frequency: Daily
- Action: Runs `pl_blob_to_sql_telco` once per day to refresh the TelcoCustomers table.
