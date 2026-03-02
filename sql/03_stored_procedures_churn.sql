-- Stored procedures for churn KPIs by contract and risk segment

------------------------------------------------------------
-- 1) Churn metrics by contract type
------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.sp_Churn_By_Contract
    @ContractType VARCHAR(50)
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        @ContractType AS Contract,
        COUNT(*) AS TotalCustomers,
        SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
        CAST(
            100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*)
            AS DECIMAL(5,2)
        ) AS ChurnRatePct,
        SUM(MonthlyCharges) AS TotalMonthlyRevenue,
        SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) AS ChurnedMonthlyRevenue
    FROM dbo.TelcoCustomers
    WHERE Contract = @ContractType;
END;
GO


------------------------------------------------------------
-- 2) Churn metrics by risk segment (High / Medium / Low)
------------------------------------------------------------
CREATE OR ALTER PROCEDURE dbo.sp_GetChurnMetricsByRiskSegment
    @Risk VARCHAR(20)
AS
BEGIN
    SET NOCOUNT ON;

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
    WHERE RiskSegment = LTRIM(RTRIM(@Risk))
    GROUP BY RiskSegment;
END;
GO
