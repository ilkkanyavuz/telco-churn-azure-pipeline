# Telco churn data dictionary

This table describes the main fields used in the Telco Customer Churn project.

- **customerID**: Unique customer identifier.
- **gender**: Customer gender (from the original Telco dataset).
- **SeniorCitizen**: 1 if the customer is a senior citizen, otherwise 0.
- **Partner**: Whether the customer has a partner (Yes/No).
- **Dependents**: Whether the customer has dependents (Yes/No).
- **tenure**: Number of months the customer has stayed with the company.
- **PhoneService**: Whether the customer has phone service (Yes/No).
- **MultipleLines**: Whether the customer has multiple lines.
- **InternetService**: Internet service provider (DSL, Fiber optic, No).
- **OnlineSecurity**, **OnlineBackup**, **DeviceProtection**, **TechSupport**:
  Optional add-on services (Yes/No/No internet).
- **StreamingTV**, **StreamingMovies**: Streaming services (Yes/No/No internet).
- **Contract**: Contract type (Month-to-month, One year, Two year).
- **PaperlessBilling**: Whether the customer uses paperless billing (Yes/No).
- **PaymentMethod**: Billing method (Electronic check, Mailed check, Bank transfer, Credit card).
- **MonthlyCharges**: Current monthly bill amount.
- **TotalCharges**: Total amount charged over the lifetime of the contract.
- **Churn**: 'Yes' if the customer has churned, otherwise 'No'.

Derived fields:
- **segment_tenure**: Tenure bucket (0–12, 13–24, 25–36, 36+ months).
- **RiskSegment**: Rule-based churn risk band (High, Medium, Low) created in SQL.
