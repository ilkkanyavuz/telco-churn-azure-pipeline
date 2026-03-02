-- Telco customer base table used for churn analysis

CREATE TABLE dbo.TelcoCustomers (
    customerID        VARCHAR(50)    NOT NULL PRIMARY KEY,
    gender            VARCHAR(10)    NULL,
    SeniorCitizen     VARCHAR(3)     NULL,   -- 'Yes' / 'No' after transform
    Partner           VARCHAR(10)    NULL,
    Dependents        VARCHAR(10)    NULL,
    tenure            INT            NULL,
    PhoneService      VARCHAR(20)    NULL,
    MultipleLines     VARCHAR(30)    NULL,
    InternetService   VARCHAR(30)    NULL,
    OnlineSecurity    VARCHAR(30)    NULL,
    OnlineBackup      VARCHAR(30)    NULL,
    DeviceProtection  VARCHAR(30)    NULL,
    TechSupport       VARCHAR(30)    NULL,
    StreamingTV       VARCHAR(30)    NULL,
    StreamingMovies   VARCHAR(30)    NULL,
    Contract          VARCHAR(30)    NULL,
    PaperlessBilling  VARCHAR(10)    NULL,
    PaymentMethod     VARCHAR(40)    NULL,
    MonthlyCharges    DECIMAL(10,2)  NULL,
    TotalCharges      DECIMAL(10,2)  NULL,
    Churn             VARCHAR(10)    NULL,
    segment_tenure    VARCHAR(10)    NULL    -- '0-12', '13-24', '25-36', '36+'
);
