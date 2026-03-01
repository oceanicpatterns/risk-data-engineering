MODEL (
    name main.transformed_risk_data,
    kind FULL,
    dialect duckdb,
    audits (
        assert_no_null_transaction_id,
        assert_unique_transaction_event_date,
        assert_probability_in_range,
        assert_positive_exposure
    )
);

SELECT
    Transaction_ID::INTEGER         AS transaction_id,
    COALESCE(
        TRY_STRPTIME(event_date, '%d/%m/%Y'),
        TRY_STRPTIME(event_date, '%Y-%m-%d')
    ) AS event_date,
    Scenario, 
    Asset_Class, 
    Sub_Asset_Class, 
    Variable_X::DOUBLE              AS variable_x,
    Variable_Y::DOUBLE              AS variable_y,
    Underlying_Asset_Price::DOUBLE  AS underlying_asset_price,
    Option_Strike_Price::DOUBLE     AS option_strike_price,
    Risk_Free_Rate::DOUBLE          AS risk_free_rate,
    Time_To_Maturity::DOUBLE        AS time_to_maturity,
    Asset_Volatility::DOUBLE        AS asset_volatility,
    Return_Asset1::DOUBLE           AS return_asset1,
    Return_Asset2::DOUBLE           AS return_asset2,
    Return_Asset3::DOUBLE           AS return_asset3,
    Weight_Asset1::DOUBLE           AS weight_asset1,
    Weight_Asset2::DOUBLE           AS weight_asset2,
    Weight_Asset3::DOUBLE           AS weight_asset3,
    Portfolio_Return::DOUBLE        AS portfolio_return,
    Cash_Flow_Period1::DOUBLE       AS cash_flow_period1,
    Cash_Flow_Period2::DOUBLE       AS cash_flow_period2,
    Cash_Flow_Period3::DOUBLE       AS cash_flow_period3,
    Bond_Yield::DOUBLE              AS bond_yield,
    CashFlow_TimePeriod1::DOUBLE    AS cashflow_timeperiod1,
    CashFlow_TimePeriod2::DOUBLE    AS cashflow_timeperiod2,
    CashFlow_TimePeriod3::DOUBLE    AS cashflow_timeperiod3,
    Probability_Default::DOUBLE     AS probability_default,
    Loss_Given_Default::DOUBLE      AS loss_given_default,
    Exposure_At_Default::DOUBLE     AS exposure_at_default,
    Bid_Price::DOUBLE               AS bid_price,
    Ask_Price::DOUBLE               AS ask_price,
    Base_Asset_Value::DOUBLE        AS base_asset_value,
    Stressed_Asset_Value::DOUBLE    AS stressed_asset_value,
    Stress_Exposure::DOUBLE         AS stress_exposure,
    Gross_Income::DOUBLE            AS gross_income,
    Asset_Risk_Weight::DOUBLE       AS asset_risk_weight,
    Additional_Liquidity_Risk::DOUBLE AS additional_liquidity_risk,
    Time_Series_Lag_Value::DOUBLE   AS time_series_lag_value,
    Current_Time_Series_Value::DOUBLE AS current_time_series_value
FROM 
    main.raw_risk_data
WHERE 
    Transaction_ID IS NOT NULL;
