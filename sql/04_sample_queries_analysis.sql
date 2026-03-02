-- Sample analysis queries for Telco churn project

------------------------------------------------------------
-- 1) Overall churn metrics
------------------------------------------------------------
SELECT *
FROM dbo.vwOverallChurn;


------------------------------------------------------------
-- 2) Churn by contract type
------------------------------------------------------------
SELECT *
FROM dbo.vwChurnByContract
ORDER BY ChurnRatePct DESC;


------------------------------------------------------------
-- 3) Churn metrics for each risk segment
------------------------------------------------------------
SELECT
    RiskSegment,
    COUNT(*) AS TotalCustomers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
    CAST(
        100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*)
        AS DECIMAL(5,2)
    ) AS ChurnRatePct,
    SUM(MonthlyCharges) AS TotalMonthlyRevenue,
    SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) AS ChurnedMonthlyRevenue
FROM dbo.vwCustomersWithRiskSegment
GROUP BY RiskSegment
ORDER BY ChurnRatePct DESC;


------------------------------------------------------------
-- 4) High-risk, month-to-month customers with high monthly charge
------------------------------------------------------------
SELECT TOP (50)
    customerID,
    Contract,
    segment_tenure,
    InternetService,
    PaymentMethod,
    MonthlyCharges,
    Churn
FROM dbo.vwCustomersWithRiskSegment
WHERE RiskSegment = 'High'
  AND Contract = 'Month-to-month'
  AND MonthlyCharges >= 80
ORDER BY MonthlyCharges DESC;


------------------------------------------------------------
-- 5) Revenue at risk by risk segment
------------------------------------------------------------
SELECT
    RiskSegment,
    SUM(MonthlyCharges) AS TotalMonthlyRevenue,
    SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) AS ChurnedMonthlyRevenue,
    SUM(CASE WHEN Churn = 'No' THEN MonthlyCharges ELSE 0 END) AS RetainedMonthlyRevenue
FROM dbo.vwCustomersWithRiskSegment
GROUP BY RiskSegment
ORDER BY TotalMonthlyRevenue DESC;
