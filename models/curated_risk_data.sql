MODEL (
    name main.curated_risk_data,
    kind FULL,
    dialect duckdb
);

SELECT
    *

    -- ================================
    -- Returns
    -- ================================
    , LN(NULLIF(Current_Time_Series_Value, 0) / NULLIF(Time_Series_Lag_Value, 0))                        AS log_return
    , (Current_Time_Series_Value - Time_Series_Lag_Value) / NULLIF(Time_Series_Lag_Value, 0)             AS arithmetic_return

    -- ================================
    -- Portfolio Theory & Risk
    -- ================================
    , (Weight_Asset1 * Return_Asset1 + Weight_Asset2 * Return_Asset2 + Weight_Asset3 * Return_Asset3)    AS portfolio_expected_return
    , (Weight_Asset1 * POW((Return_Asset1 - Portfolio_Return), 2)
      + Weight_Asset2 * POW((Return_Asset2 - Portfolio_Return), 2)
      + Weight_Asset3 * POW((Return_Asset3 - Portfolio_Return), 2))                                      AS portfolio_variance_approx
    , Probability_Default * Loss_Given_Default * Exposure_At_Default                                     AS expected_loss
    , (Ask_Price - Bid_Price) / NULLIF((Ask_Price + Bid_Price)/2, 0)                                     AS bid_ask_spread_pct
    , Gross_Income * 0.15                                                                                AS op_risk_basic_indicator_capital
    , Stress_Exposure                                                                                    AS scenario_loss
    , Asset_Risk_Weight * Exposure_At_Default                                                            AS risk_weighted_asset
    , Base_Asset_Value - Stressed_Asset_Value                                                            AS stress_delta

FROM 
    main.transformed_risk_data;
