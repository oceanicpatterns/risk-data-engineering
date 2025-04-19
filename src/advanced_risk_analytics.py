import warnings
import logging
import polars as pl
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from pandas.errors import PerformanceWarning
from utils import setup_logging, get_connection, load_curated

# Suppress common statsmodels and convergence warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
try:
    from pandas.errors import PerformanceWarning
    warnings.filterwarnings("ignore", category=PerformanceWarning)
except ImportError:
    pass

logger = logging.getLogger(__name__)
setup_logging()

def predictive_modeling_default(df):
    required_cols = ["exposure_at_default", "loss_given_default", "asset_volatility", "probability_default"]
    if not all(col in df.columns for col in required_cols):
        print("[Predictive Modeling] Skipped: required columns missing.")
        print("Explanation: The predictive model requires the columns 'exposure_at_default', 'loss_given_default', 'asset_volatility', and 'probability_default'. Please ensure your data includes these fields.")
        return
    pdf = df.select(required_cols).to_pandas().dropna()
    X = pdf[["exposure_at_default", "loss_given_default", "asset_volatility"]]
    y = (pdf["probability_default"] > 0.5).astype(int)
    if len(np.unique(y)) < 2:
        print("[Predictive Modeling] Only one class present in target; skipping model training.")
        print("Explanation: All observations in your data are either defaults or non-defaults (but not both). The model cannot learn to distinguish risk levels. For meaningful predictive analytics, ensure your data contains both risky and non-risky exposures.")
        return
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    print(f"[Predictive Modeling] Logistic Regression Test Accuracy: {score:.3f}")
    print("Explanation: This test accuracy measures how well the model can distinguish between risky and non-risky exposures based on your data. Higher accuracy means better predictive power. Feature importance is visualized below.")
    plt.bar(X.columns, model.coef_[0])
    plt.title("Feature Importance (Logistic Regression)")
    plt.ylabel("Coefficient")
    plt.tight_layout()
    plt.show()

def value_at_risk(df):
    # Now also works with curated_risk_data fields
    if "portfolio_return" not in df.columns:
        print("[Risk Aggregation] Skipped: 'portfolio_return' not found.")
        print("Explanation: VaR calculation requires a 'portfolio_return' column representing portfolio returns or losses. Please ensure this field is present in your data.")
        return
    returns = df["portfolio_return"].to_numpy()
    var_95 = np.percentile(returns, 5)
    print(f"[Risk Aggregation] Portfolio 95% Value-at-Risk (VaR): {var_95:.4f}")
    print("Explanation: Value-at-Risk (VaR) estimates the maximum expected portfolio loss at a 95% confidence level. Here, there is a 95% chance your portfolio loss will not exceed this value over the specified period. For example, if your portfolio is worth $10 million and VaR is 0.0320, you do not expect to lose more than $32,000 (3.2% of $1M) in 95 out of 100 periods.")
    # Show new curated fields if present
    if "expected_loss" in df.columns:
        print(f"[Credit Risk] Expected Loss (EL): {df['expected_loss'].sum():.2f}")
        print("Explanation: Expected Loss (EL) is the average loss expectancy on a credit exposure, calculated as PD × LGD × EAD. This is the total expected loss for all exposures in the dataset.")
    if "risk_weighted_asset" in df.columns:
        print(f"[Capital Adequacy] Risk-Weighted Assets (RWA): {df['risk_weighted_asset'].sum():.2f}")
        print("Explanation: RWA is the sum of exposures weighted by regulatory risk weights, used to determine capital requirements.")
    if "op_risk_basic_indicator_capital" in df.columns:
        print(f"[Op Risk] Basic Indicator Capital: {df['op_risk_basic_indicator_capital'].sum():.2f}")
        print("Explanation: This is the required capital for operational risk, calculated as 15% of gross income (Basic Indicator Approach).")
    if "bid_ask_spread_pct" in df.columns:
        print(f"[Liquidity] Avg Bid-Ask Spread (%): {100 * df['bid_ask_spread_pct'].mean():.2f}%")
        print("Explanation: The bid-ask spread as a % of mid-price, indicating market liquidity.")
    if "scenario_loss" in df.columns:
        print(f"[Stress Test] Total Scenario Loss: {df['scenario_loss'].sum():.2f}")
        print("Explanation: Scenario loss is the estimated loss under a specified stress scenario.")
    if "portfolio_expected_return" in df.columns:
        print(f"[Portfolio] Avg Expected Return: {df['portfolio_expected_return'].mean():.4f}")
        print("Explanation: The expected return of the portfolio, weighted by asset weights.")
    if "portfolio_variance_approx" in df.columns:
        print(f"[Portfolio] Avg Variance (approx): {df['portfolio_variance_approx'].mean():.4f}")
        print("Explanation: Approximated portfolio variance using weighted squared deviations.")

def time_series_forecast(df):
    if "event_date" not in df.columns or "exposure_at_default" not in df.columns:
        print("[Time Series Forecast] Skipped: required columns missing.")
        print("Explanation: Time series forecasting requires both 'event_date' and 'exposure_at_default' columns. Please ensure your data includes these fields.")
        return
    ts = (
        df.select(["event_date", "exposure_at_default"])
          .sort("event_date")
          .to_pandas()
    )
    if not np.issubdtype(ts["event_date"].dtype, np.datetime64):
        ts["event_date"] = pl.Series(ts["event_date"]).str.strptime(pl.Date, "%Y-%m-%d", strict=False).to_numpy()
    ts = ts.dropna().sort_values("event_date")
    ts_grouped = ts.groupby("event_date")["exposure_at_default"].sum()
    if len(ts_grouped) < 10:
        print("[Time Series Forecast] Skipped: not enough data points for ARIMA.")
        print("Explanation: ARIMA forecasting requires a sufficient history of data. If you see this message, consider collecting more data or aggregating to a coarser frequency (e.g., monthly).")
        return
    model = ARIMA(ts_grouped, order=(1,1,1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)
    plt.plot(ts_grouped.index, ts_grouped.values, label="Observed")
    plt.plot(
        range(len(ts_grouped), len(ts_grouped)+len(forecast)),
        forecast,
        label="Forecast",
        marker="o"
    )
    plt.title("Exposure at Default - ARIMA Forecast")
    plt.xlabel("Date Index")
    plt.ylabel("Exposure at Default")
    plt.legend()
    plt.tight_layout()
    plt.show()
    print("Explanation: The ARIMA model forecasts future values of Exposure at Default based on historical trends. Use this to anticipate risk levels and plan capital needs ahead.")

def main() -> None:
    """Run advanced risk analytics on curated data."""
    with get_connection() as con:
        df = load_curated(con)
    logger.info("Loaded curated_risk_data with %d rows", df.height)
    # Run analytics
    predictive_modeling_default(df)
    value_at_risk(df)
    time_series_forecast(df)

if __name__ == "__main__":
    main()
