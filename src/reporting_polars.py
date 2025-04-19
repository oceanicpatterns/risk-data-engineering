import logging
import polars as pl
from utils import setup_logging, get_connection, load_curated, group_by_asset_class

logger = logging.getLogger(__name__)
setup_logging()

def main() -> None:
    """Generate summary reports from curated risk data."""
    with get_connection() as con:
        df = load_curated(con)
    logger.info("Loaded curated_risk_data with %d rows", df.height)

    logger.info("--- Summary ---")
    print(df.describe())

    # Show curated metrics
    curated_fields = [
        "log_return", "arithmetic_return", "portfolio_expected_return", "portfolio_variance_approx",
        "expected_loss", "bid_ask_spread_pct", "op_risk_basic_indicator_capital", "scenario_loss",
        "risk_weighted_asset", "stress_delta"
    ]
    present = [c for c in curated_fields if c in df.columns]
    if present:
        logger.info("--- Curated Metrics Summary ---")
        print(df.select(present).describe())

    # Asset class report
    if "asset_class" in df.columns:
        logger.info("--- Exposure & PD by Asset Class ---")
        agg = {'exposure_at_default':'sum', 'probability_default':'mean'}
        for col in ['expected_loss','risk_weighted_asset','op_risk_basic_indicator_capital']:
            if col in df.columns:
                agg[col] = 'sum'
        rename = {
            'exposure_at_default':'Total_EAD', 'probability_default':'Avg_PD',
            'expected_loss':'Total_EL', 'risk_weighted_asset':'Total_RWA',
            'op_risk_basic_indicator_capital':'Total_OpRisk_Capital'
        }
        report = group_by_asset_class(df, agg, rename)
        print(report)

    # Liquidity metrics
    if "bid_ask_spread_pct" in df.columns:
        logger.info("--- Liquidity Metrics ---")
        print(f"Avg Bid-Ask Spread (%): {100*df['bid_ask_spread_pct'].mean():.2f}%")

    # Stress loss
    if "scenario_loss" in df.columns:
        logger.info("--- Stress Test Loss ---")
        print(f"Total Scenario Loss: {df['scenario_loss'].sum():.2f}")

if __name__ == "__main__":
    main()
