import logging
import polars as pl
import plotly.express as px
from utils import setup_logging, get_connection, load_curated

setup_logging()
logger = logging.getLogger(__name__)

def plot_exposure_by_asset_class(df):
    if "asset_class" in df.columns and "exposure_at_default" in df.columns:
        report = (
            df.groupby_dynamic(index_column=None, by=["asset_class"]).agg([
                pl.col("exposure_at_default").sum().alias("Total_EAD")
            ])
            if hasattr(df, 'groupby_dynamic') else
            df.groupby("asset_class").agg([
                pl.col("exposure_at_default").sum().alias("Total_EAD")
            ])
        ) if hasattr(df, 'groupby') else None
        if report is not None:
            fig = px.bar(report.to_pandas(), x="asset_class", y="Total_EAD", title="Exposure at Default by Asset Class")
            fig.show()

def plot_time_series_exposure(df):
    if "event_date" in df.columns and "exposure_at_default" in df.columns:
        report = (
            df.groupby_dynamic(index_column=None, by=["event_date"]).agg([
                pl.col("exposure_at_default").sum().alias("Total_EAD")
            ])
            if hasattr(df, 'groupby_dynamic') else
            df.groupby("event_date").agg([
                pl.col("exposure_at_default").sum().alias("Total_EAD")
            ])
        ) if hasattr(df, 'groupby') else None
        if report is not None:
            fig = px.line(report.to_pandas(), x="event_date", y="Total_EAD", title="Exposure Over Time")
            fig.show()

def plot_high_risk_transactions(df):
    if set(["probability_default", "exposure_at_default"]).issubset(df.columns):
        high_risk = df.filter((pl.col("probability_default") > 0.5) | (pl.col("exposure_at_default") > 1000))
        if high_risk.height > 0:
            fig = px.scatter(
                high_risk.to_pandas(),
                x="probability_default",
                y="exposure_at_default",
                color="asset_class" if "asset_class" in high_risk.columns else None,
                hover_data=["transaction_id"] if "transaction_id" in high_risk.columns else None,
                title="High Risk Transactions"
            )
            fig.show()

def plot_curated_metrics(df):
    import plotly.express as px
    # Plot expected loss by asset class
    if "asset_class" in df.columns and "expected_loss" in df.columns:
        report = (
            df.groupby("asset_class").agg([
                pl.col("expected_loss").sum().alias("Total_Expected_Loss")
            ])
        )
        fig = px.bar(report.to_pandas(), x="asset_class", y="Total_Expected_Loss", title="Expected Loss by Asset Class")
        fig.show()
    # Plot risk-weighted assets by asset class
    if "asset_class" in df.columns and "risk_weighted_asset" in df.columns:
        report = (
            df.groupby("asset_class").agg([
                pl.col("risk_weighted_asset").sum().alias("Total_RWA")
            ])
        )
        fig = px.bar(report.to_pandas(), x="asset_class", y="Total_RWA", title="Risk-Weighted Assets by Asset Class")
        fig.show()
    # Plot bid-ask spread distribution
    if "bid_ask_spread_pct" in df.columns:
        fig = px.histogram(df.to_pandas(), x="bid_ask_spread_pct", nbins=30, title="Bid-Ask Spread (%) Distribution")
        fig.show()
    # Plot scenario loss over time if available
    if "event_date" in df.columns and "scenario_loss" in df.columns:
        report = (
            df.groupby("event_date").agg([
                pl.col("scenario_loss").sum().alias("Total_Scenario_Loss")
            ])
            .sort("event_date")
        )
        fig = px.line(report.to_pandas(), x="event_date", y="Total_Scenario_Loss", title="Scenario Loss Over Time")
        fig.show()

def main() -> None:
    """Generate interactive charts from curated risk data."""
    with get_connection() as con:
        df = load_curated(con)
    logger.info("Loaded curated_risk_data with %d rows", df.height)

    plot_exposure_by_asset_class(df)
    plot_time_series_exposure(df)
    plot_high_risk_transactions(df)
    plot_curated_metrics(df)

if __name__ == "__main__":
    main()
