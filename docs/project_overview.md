# Project overview

## Business goal

The goal of this project is to analyse Telco customer churn, understand which segments are at higher risk of leaving, and estimate the monthly revenue at risk. The final output is a set of KPIs and dashboards that can help a retention team prioritise actions.

## Architecture

- Python ingestion script reads the Telco churn CSV file and writes data to Azure Blob Storage in `raw/` and `processed/` layers.
- Azure Data Factory loads the processed files into an Azure SQL database table `dbo.TelcoCustomers` on a daily schedule.
- SQL views and stored procedures calculate churn KPIs, risk segments and revenue at risk.
- Power BI connects to the SQL views to build interactive reports.

## Main deliverables

- Clean Telco churn dataset with documented fields.
- SQL views for overall churn, churn by contract, and risk-based segments.
- Power BI report with executive overview, segment analysis and a risk & retention page.
- Documentation in this `docs` folder to explain the data, decisions and architecture.

