-- Views for churn KPIs and risk segmentation

------------------------------------------------------------
-- 1) Risk segmentation view
------------------------------------------------------------
CREATE OR ALTER VIEW dbo.vwCustomersWithRiskSegment AS
SELECT
    customerID,
    gender,
    SeniorCitizen,
    Partner,
    Dependents,
    tenure,
    PhoneService,
    MultipleLines,
    InternetService,
    OnlineSecurity,
    OnlineBackup,
    DeviceProtection,
    TechSupport,
    StreamingTV,
    StreamingMovies,
    Contract,
    PaperlessBilling,
    PaymentMethod,
    MonthlyCharges,
    TotalCharges,
    Churn,
    segment_tenure,
    CASE 
        WHEN Contract = 'Month-to-month'
             AND tenure <= 12
             AND InternetService = 'Fiber optic'
             AND PaymentMethod = 'Electronic check'
        THEN 'High'
        WHEN Contract = 'Month-to-month'
             AND tenure BETWEEN 13 AND 24
        THEN 'Medium'
        WHEN InternetService = 'Fiber optic'
             AND PaymentMethod = 'Electronic check'
             AND tenure > 12
        THEN 'Medium'
        WHEN Contract IN ('One year', 'Two year')
             OR tenure >= 36
             OR PaymentMethod IN ('Bank transfer (automatic)', 'Credit card (automatic)')
        THEN 'Low'
        ELSE 'Medium'
    END AS RiskSegment
FROM dbo.TelcoCustomers;


------------------------------------------------------------
-- 2) Overall churn KPIs
--------------------------------------------
