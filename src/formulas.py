"""
formulas.py
-----------
This module contains functions for a comprehensive set of formulas used in Finance,
including basic statistics, probability distributions, time value of money, regression analysis,
portfolio theory, risk measures (VaR, Expected Shortfall, stress tests, etc.), derivatives pricing,
options Greeks, fixed income, credit risk, operational risk, performance measures, time series models,
multi-factor models, risk scaling, returns, liquidity risk, stress testing, and capital adequacy.
"""

import math
import logging
import pandas as pd
from utils import setup_logging, get_connection, load_curated
from advanced_risk_analytics import predictive_modeling_default, time_series_forecast
import numpy as np
from scipy.stats import norm
# =============================================================================
# Basic Statistics
# =============================================================================
def mean(series):
    """Calculate the arithmetic mean of a series."""
    return np.mean(series)

def variance(series):
    """Calculate the variance (population) of a series."""
    return np.var(series)

def standard_deviation(series):
    """Calculate the standard deviation of a series."""
    return np.std(series)

def covariance(series1, series2):
    """
    Calculate the covariance between two series.
    
    Uses the population covariance (bias=True).
    """
    return np.cov(series1, series2, bias=True)[0, 1]

def correlation(series1, series2):
    """Calculate the correlation coefficient between two series."""
    return np.corrcoef(series1, series2)[0, 1]

# =============================================================================
# Probability Distributions
# =============================================================================
def normal_pdf(x, mu, sigma):
    """
    Normal Probability Density Function.
    
    f(x) = 1/(sqrt(2*pi)*sigma) * exp(- (x-mu)^2/(2*sigma^2))
    """
    return 1 / (math.sqrt(2 * math.pi) * sigma) * math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))

def standard_normal_pdf(z):
    """
    Standard Normal PDF (mu = 0, sigma = 1).
    
    f(z) = 1/sqrt(2*pi) * exp(- z^2/2)
    """
    return 1 / math.sqrt(2 * math.pi) * math.exp(-z**2 / 2)

def binomial_pmf(k, n, p):
    """
    Binomial Probability Mass Function.
    
    P(X=k) = C(n, k) * p^k * (1-p)^(n-k)
    """
    from math import comb
    return comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

def poisson_pmf(k, lam):
    """
    Poisson Probability Mass Function.
    
    P(X=k) = (lam^k * exp(-lam)) / k!
    """
    return (lam ** k) * math.exp(-lam) / math.factorial(k)

# =============================================================================
# Time Value of Money
# =============================================================================
def future_value(PV, r, n):
    """
    Future Value.
    
    FV = PV * (1 + r)^n
    """
    return PV * (1 + r) ** n

def present_value(FV, r, n):
    """
    Present Value.
    
    PV = FV / (1 + r)^n
    """
    return FV / ((1 + r) ** n)

def annuity_present_value(C, r, n):
    """
    Present value of an annuity.
    
    PV = C * [1 - (1 + r)^(-n)] / r
    """
    if r == 0:
        return C * n
    return C * (1 - (1 + r) ** (-n)) / r

def growing_annuity_present_value(C, r, g, n):
    """
    Present value of a growing annuity.
    
    PV = C * [1 - ((1 + g)/(1 + r))^n] / (r - g)
    
    If r equals g, an alternative formulation is used.
    """
    if r == g:
        return C * n / (1 + r)
    return C * (1 - ((1 + g) / (1 + r)) ** n) / (r - g)

# =============================================================================
# Regression Analysis
# =============================================================================
def ols_slope(x, y):
    """
    Ordinary Least Squares slope estimation.
    
    β = Σ[(x_i - mean(x)) * (y_i - mean(y))] / Σ[(x_i - mean(x))^2]
    """
    x = np.array(x)
    y = np.array(y)
    return np.sum((x - np.mean(x)) * (y - np.mean(y))) / np.sum((x - np.mean(x)) ** 2)

def r_squared(y_true, y_pred):
    """
    Calculate R-squared value.
    
    R² = 1 - (SS_res / SS_tot)
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - ss_res / ss_tot

# =============================================================================
# Portfolio Theory
# =============================================================================
def expected_portfolio_return(weights, returns):
    """
    Calculate the expected portfolio return.
    
    E(Rp) = Σ(w_i * R_i)
    """
    weights = np.array(weights)
    returns = np.array(returns)
    return np.dot(weights, returns)

def portfolio_variance(weights, covariance_matrix):
    """
    Calculate the portfolio variance.
    
    σ_p² = w' * Σ * w
    """
    weights = np.array(weights)
    cov_matrix = np.array(covariance_matrix)
    return np.dot(weights, np.dot(cov_matrix, weights))

def capm_expected_return(R_f, beta, R_m):
    """
    CAPM Expected Return.
    
    E(R_i) = R_f + beta * (R_m - R_f)
    """
    return R_f + beta * (R_m - R_f)

def beta_from_covariance(cov_Ri_Rm, market_variance):
    """
    Calculate beta.
    
    β = Cov(R_i, R_m) / σ_m² (market variance)
    """
    return cov_Ri_Rm / market_variance

# =============================================================================
# Risk Measures
# =============================================================================
def parametric_var(mu_p, sigma_p, z_alpha):
    """
    Calculate Parametric VaR assuming a normal distribution.
    
    VaR = μ_p - z_(α) * σ_p
    """
    return mu_p - z_alpha * sigma_p

def historical_var(losses, alpha):
    """
    Calculate Historical Simulation VaR.
    
    Finds the (1-alpha)th quantile of the loss distribution.
    """
    return np.percentile(losses, 100 * (1 - alpha))

def monte_carlo_var(simulated_losses, alpha):
    """
    Calculate Monte Carlo VaR.
    
    Uses the simulated loss distribution to determine the VaR.
    """
    return np.percentile(simulated_losses, 100 * (1 - alpha))

def expected_shortfall(losses, var_threshold):
    """
    Calculate Expected Shortfall (ES).
    
    ES = average loss for losses greater than or equal to the VaR threshold.
    """
    losses = np.array(losses)
    tail_losses = losses[losses >= var_threshold]
    if len(tail_losses) == 0:
        return var_threshold
    return np.mean(tail_losses)

def incremental_var(var_portfolio_plus, var_portfolio):
    """
    Calculate Incremental VaR.
    
    iVaR = VaR (portfolio with new position) - VaR (portfolio without new position)
    """
    return var_portfolio_plus - var_portfolio

def marginal_var(var_func, weights, asset_index, delta=1e-5):
    """
    Calculate Marginal VaR using a finite difference approximation.
    
    var_func: function that takes portfolio weights and returns VaR.
    weights: numpy array of portfolio weights.
    asset_index: index of the asset to perturb.
    delta: small change in weight.
    """
    weights = np.array(weights)
    original_var = var_func(weights)
    weights_delta = weights.copy()
    weights_delta[asset_index] += delta
    var_with_delta = var_func(weights_delta)
    return (var_with_delta - original_var) / delta

def stress_loss(exposures, base_values, stressed_values):
    """
    Calculate Stress Loss.
    
    Stress Loss = Σ (Exposure_i * (Base Value_i - Stressed Value_i))
    """
    exposures = np.array(exposures)
    base_values = np.array(base_values)
    stressed_values = np.array(stressed_values)
    return np.sum(exposures * (base_values - stressed_values))

def liquidity_adjusted_var(base_var, additional_liquidity_term):
    """
    Calculate Liquidity-Adjusted VaR.
    
    LA-VaR = base VaR + additional liquidity risk term.
    """
    return base_var + additional_liquidity_term

# =============================================================================
# Derivatives & Options
# =============================================================================
def black_scholes_call(S, K, r, T, sigma):
    """
    Calculate the price of a European call option using the Black-Scholes formula.
    
    S: Underlying asset price.
    K: Strike price.
    r: Risk-free rate.
    T: Time to maturity.
    sigma: Volatility.
    """
    # Vectorized implementation using numpy
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return call_price

def d1_black_scholes(S, K, r, T, sigma):
    """
    Calculate d1 for the Black-Scholes formula.
    
    d1 = [ln(S/K) + (r + sigma^2/2) * T] / (sigma * sqrt(T))
    """
    return (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def d2_black_scholes(S, K, r, T, sigma):
    """
    Calculate d2 for the Black-Scholes formula.
    
    d2 = d1 - sigma * sqrt(T)
    """
    return d1_black_scholes(S, K, r, T, sigma) - sigma * math.sqrt(T)

def put_call_parity(call_price, S, K, r, T):
    """
    Calculate the put option price using Put-Call Parity for European options.
    
    C - P = S - K * exp(-r*T)   =>   P = C - S + K*exp(-r*T)
    """
    return call_price - S + K * math.exp(-r * T)

# Options Greeks based on the Black-Scholes model
def delta_call(S, K, r, T, sigma):
    """
    Calculate Delta for a call option.
    
    Delta = N(d1)
    """
    d1 = d1_black_scholes(S, K, r, T, sigma)
    return norm.cdf(d1)

def gamma_call(S, K, r, T, sigma):
    """
    Calculate Gamma for a call option.
    
    Gamma = N'(d1) / (S * sigma * sqrt(T))
    """
    d1 = d1_black_scholes(S, K, r, T, sigma)
    return norm.pdf(d1) / (S * sigma * math.sqrt(T))

def theta_call(S, K, r, T, sigma):
    """
    Calculate Theta (time decay) for a call option.
    
    Theta (annualized) = [ - (S * N'(d1)*sigma) / (2*sqrt(T)) - r*K*exp(-r*T)*N(d2) ] / 365
    """
    d1 = d1_black_scholes(S, K, r, T, sigma)
    d2 = d2_black_scholes(S, K, r, T, sigma)
    term1 = - (S * norm.pdf(d1) * sigma) / (2 * math.sqrt(T))
    term2 = - r * K * math.exp(-r * T) * norm.cdf(d2)
    return (term1 + term2) / 365

def vega_call(S, K, r, T, sigma):
    """
    Calculate Vega for a call option.
    
    Vega = S * N'(d1)*sqrt(T)
    """
    d1 = d1_black_scholes(S, K, r, T, sigma)
    return S * norm.pdf(d1) * math.sqrt(T)

def rho_call(S, K, r, T, sigma):
    """
    Calculate Rho for a call option.
    
    Rho = K * T * exp(-r*T) * N(d2)
    """
    d2 = d2_black_scholes(S, K, r, T, sigma)
    return K * T * math.exp(-r * T) * norm.cdf(d2)

# =============================================================================
# Fixed Income
# =============================================================================
def bond_price(cash_flows, y):
    """
    Calculate the price of a bond.
    
    Price = Σ [CF_t / (1 + y)^t]
    Assumes cash flows occur at equally spaced time intervals.
    """
    price = 0
    for t, cf in enumerate(cash_flows, start=1):
        price += cf / ((1 + y) ** t)
    return price

def macaulay_duration(cash_flows, y):
    """
    Calculate the Macaulay Duration of a bond.
    
    Duration = Σ [t * (CF_t/(1+y)^t)] / Price
    """
    P = bond_price(cash_flows, y)
    duration = 0
    for t, cf in enumerate(cash_flows, start=1):
        duration += t * (cf / ((1 + y) ** t))
    return duration / P

def modified_duration(cash_flows, y):
    """
    Calculate the Modified Duration of a bond.
    
    D_mod = Macaulay Duration / (1 + y)
    """
    return macaulay_duration(cash_flows, y) / (1 + y)

def bond_convexity(cash_flows, y):
    """
    Calculate the convexity of a bond.
    
    Convexity = (1/P) * Σ [t(t+1)*CF_t/(1+y)^(t+2)]
    """
    P = bond_price(cash_flows, y)
    convexity = 0
    for t, cf in enumerate(cash_flows, start=1):
        convexity += t * (t + 1) * cf / ((1 + y) ** (t + 2))
    return convexity / P

# =============================================================================
# Credit Risk
# =============================================================================
def expected_loss(PD, LGD, EAD):
    """
    Calculate Expected Loss.
    
    EL = PD * LGD * EAD
    """
    return PD * LGD * EAD

def distance_to_default(assets, liabilities, mu, sigma, T):
    """
    Calculate the distance to default using the Merton/KMV approach.
    
    DD = [ln(assets/liabilities) + (mu - sigma^2/2)*T] / (sigma*sqrt(T))
    """
    return (math.log(assets / liabilities) + (mu - 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))

def approximate_credit_spread(PD, LGD, recovery_rate):
    """
    Approximate the credit spread.
    
    This is a simplified placeholder:
    Spread ≈ PD * LGD / (1 - recovery_rate)
    """
    return PD * LGD / (1 - recovery_rate)

# =============================================================================
# Operational Risk
# =============================================================================
def basic_indicator_capital(gross_income, alpha=0.15):
    """
    Calculate operational risk capital using the Basic Indicator Approach.
    
    Capital = alpha * Gross Income
    Default alpha is 15% unless specified.
    """
    return alpha * gross_income

# =============================================================================
# Risk-Adjusted Performance Measures
# =============================================================================
def sharpe_ratio(portfolio_return, risk_free_rate, portfolio_std):
    """
    Calculate the Sharpe Ratio.
    
    Sharpe Ratio = (E(Rp) - R_f) / σ_p
    """
    return (portfolio_return - risk_free_rate) / portfolio_std

def treynor_ratio(portfolio_return, risk_free_rate, beta):
    """
    Calculate the Treynor Ratio.
    
    Treynor Ratio = (E(Rp) - R_f) / beta
    """
    return (portfolio_return - risk_free_rate) / beta

def jensens_alpha(portfolio_return, risk_free_rate, beta, market_return):
    """
    Calculate Jensen's Alpha.
    
    Jensen's Alpha = R_p - [R_f + beta * (R_m - R_f)]
    """
    return portfolio_return - (risk_free_rate + beta * (market_return - risk_free_rate))

def information_ratio(active_return, tracking_error):
    """
    Calculate the Information Ratio.
    
    Information Ratio = Active Return / Tracking Error
    """
    return active_return / tracking_error

# =============================================================================
# Time Series Models
# =============================================================================
def ar1_simulation(phi, sigma_e, X0, n):
    """
    Simulate an AR(1) process.
    
    X_t = φ * X_(t-1) + ε_t, where ε_t ~ N(0, sigma_e^2)
    Returns a list of simulated values.
    """
    X = [X0]
    for _ in range(n - 1):
        epsilon = np.random.normal(0, sigma_e)
        X.append(phi * X[-1] + epsilon)
    return X

def garch11_simulation(omega, alpha, beta, n, sigma0=1.0):
    """
    Simulate a GARCH(1,1) process for volatility and generate returns.
    
    σ_t^2 = ω + α * ε_(t-1)^2 + β * σ_(t-1)^2,
    and returns ε_t ~ N(0, σ_t^2).
    
    Returns a tuple: (list of volatilities, list of returns)
    """
    sigmas = [sigma0]
    returns = []
    for _ in range(n):
        epsilon = np.random.normal(0, sigmas[-1])
        returns.append(epsilon)
        sigma_t_sq = omega + alpha * (epsilon ** 2) + beta * (sigmas[-1] ** 2)
        sigmas.append(math.sqrt(sigma_t_sq))
    return sigmas[:-1], returns

# =============================================================================
# Multi-Factor Models
# =============================================================================
def fama_french_3_factor(R_m, R_f, SMB, HML, beta_market, beta_SMB, beta_HML, alpha=0):
    """
    Calculate the expected excess return using the Fama-French 3-Factor Model.
    
    R_i - R_f = α + β_m (R_m - R_f) + β_SMB * SMB + β_HML * HML + ε
    Returns the expected excess return.
    """
    return alpha + beta_market * (R_m - R_f) + beta_SMB * SMB + beta_HML * HML

# =============================================================================
# Risk Scaling
# =============================================================================
def volatility_scaling(sigma_one_day, T_days):
    """
    Scale one-day volatility to T days.
    
    σ_T = σ_1day * sqrt(T)
    """
    return sigma_one_day * math.sqrt(T_days)

# =============================================================================
# Returns
# =============================================================================
def log_return(P_t, P_t_minus_1):
    """
    Calculate the continuously compounded (log) return.
    
    r = ln(P_t / P_t_minus_1)
    """
    return math.log(P_t / P_t_minus_1)

def arithmetic_return(P_t, P_t_minus_1):
    """
    Calculate the arithmetic return.
    
    r = (P_t - P_t_minus_1) / P_t_minus_1
    """
    return (P_t - P_t_minus_1) / P_t_minus_1

# =============================================================================
# Liquidity Risk
# =============================================================================
def bid_ask_spread_metric(bid_price, ask_price):
    """
    Calculate the relative bid-ask spread.
    
    Relative Spread = (Ask Price - Bid Price) / Mid Price.
    """
    mid_price = (bid_price + ask_price) / 2
    return (ask_price - bid_price) / mid_price

# =============================================================================
# Stress Test Metrics
# =============================================================================
def scenario_loss(exposures, base_values, stressed_values):
    """
    Calculate the scenario loss.
    
    Scenario Loss = Σ (Exposure_i * (Base Value_i - Stressed Value_i))
    """
    exposures = np.array(exposures)
    base_values = np.array(base_values)
    stressed_values = np.array(stressed_values)
    return np.sum(exposures * (base_values - stressed_values))

# =============================================================================
# Capital Adequacy
# =============================================================================
def risk_weighted_assets(exposures, risk_weights):
    """
    Calculate Risk-Weighted Assets.
    
    RWA = Σ (Exposure_i * Risk Weight_i)
    """
    exposures = np.array(exposures)
    risk_weights = np.array(risk_weights)
    return np.sum(exposures * risk_weights)

def minimum_capital_ratio(capital, rwa):
    """
    Calculate the Minimum Capital Ratio.
    
    Ratio = Capital / RWA
    """
    if rwa == 0:
        return float('inf')
    return capital / rwa

# =============================================================================
# Main entrypoint
# =============================================================================
setup_logging()
logger = logging.getLogger(__name__)

def main() -> None:
    """Compute core metrics on curated data and log the results."""
    with get_connection() as con:
        df = load_curated(con)

    # Convert to pandas for grouped time/asset-class reporting
    df_pd = None
    if 'event_date' in df.columns:
        df_pd = df.to_pandas()
        df_pd['event_date'] = pd.to_datetime(df_pd['event_date'], errors='coerce')
        df_pd['year'] = df_pd['event_date'].dt.year.astype(str)

    # Exposure at Default
    if 'exposure_at_default' in df.columns:
        arr = df['exposure_at_default'].to_numpy()
        # Log mean, variance, and standard deviation of Exposure at Default
        logger.info("EAD mean=%.4f, var=%.4f, std=%.4f", arr.mean(), arr.var(), arr.std())
        # EAD by asset class and year
        if df_pd is not None and 'asset_class' in df_pd.columns:
            for ac, grp in df_pd.groupby('asset_class'):
                a = grp['exposure_at_default'].to_numpy()
                logger.info("EAD for %s: mean=%.4f, var=%.4f, std=%.4f", ac, a.mean(), a.var(), a.std())
        if df_pd is not None and 'year' in df_pd.columns:
            for yr, grp in df_pd.groupby('year'):
                a = grp['exposure_at_default'].to_numpy()
                logger.info("EAD for %s: mean=%.4f", yr, a.mean())
    else:
        logger.warning("'exposure_at_default' missing; skipping EAD stats.")

    # Returns
    if {'log_return','arithmetic_return'}.issubset(df.columns):
        lr = df['log_return'].to_numpy(); ar = df['arithmetic_return'].to_numpy()
        logger.info("Log Return mean=%.4f, Arith Return mean=%.4f", lr.mean(), ar.mean())
        # Returns by asset class and year
        if df_pd is not None and 'asset_class' in df_pd.columns:
            for ac, grp in df_pd.groupby('asset_class'):
                l = grp['log_return'].to_numpy(); r = grp['arithmetic_return'].to_numpy()
                logger.info("Returns for %s: log mean=%.4f, arith mean=%.4f", ac, l.mean(), r.mean())
        if df_pd is not None and 'year' in df_pd.columns:
            for yr, grp in df_pd.groupby('year'):
                l = grp['log_return'].to_numpy()
                logger.info("Log Return for %s mean=%.4f", yr, l.mean())
    else:
        logger.warning("Missing returns; skipping return metrics.")

    # Liquidity
    if 'bid_ask_spread_pct' in df.columns:
        arr = df['bid_ask_spread_pct'].to_numpy()
        logger.info("Bid-Ask Spread mean=%.4f", arr.mean())
    else:
        logger.warning("'bid_ask_spread_pct' missing; skipping liquidity metrics.")

    # Derived Liquidity from bid/ask
    if {'bid_price','ask_price'}.issubset(df.columns):
        bid = df['bid_price'].to_numpy(); ask = df['ask_price'].to_numpy()
        mid = (bid + ask) / 2
        sp_pct = (ask - bid) / mid
        logger.info("Derived Bid-Ask Spread pct mean=%.4f", sp_pct.mean())
    else:
        logger.warning("Cannot derive bid-ask spread, missing 'bid_price' or 'ask_price'.")

    # Capital Adequacy (fallback to curated single-column data)
    if {'exposures','risk_weights','capital'}.issubset(df.columns):
        rwa = risk_weighted_assets(df['exposures'].to_numpy(), df['risk_weights'].to_numpy())
        cap = df['capital'].sum()
        ratio = minimum_capital_ratio(cap, rwa)
        logger.info("RWA=%.4f, Capital Sum=%.4f, Ratio=%.4f", rwa, cap, ratio)
    elif 'risk_weighted_asset' in df.columns and 'op_risk_basic_indicator_capital' in df.columns:
        rwa2 = df['risk_weighted_asset'].sum()
        cap2 = df['op_risk_basic_indicator_capital'].sum()
        ratio2 = minimum_capital_ratio(cap2, rwa2)
        logger.info("[Fallback] RWA sum=%.4f, OpRisk Cap sum=%.4f, Ratio=%.4f", rwa2, cap2, ratio2)
    else:
        logger.warning("No suitable capital adequacy fields found; skipping.")

    # Portfolio metrics
    if 'portfolio_expected_return' in df.columns:
        per = df['portfolio_expected_return'].to_numpy()
        logger.info("Portfolio Expected Return mean=%.4f", per.mean())
    else:
        logger.warning("'portfolio_expected_return' missing; skipping portfolio return.")
    if 'portfolio_variance_approx' in df.columns:
        pv = df['portfolio_variance_approx'].to_numpy()
        logger.info("Portfolio Variance (approx) mean=%.4f", pv.mean())
    else:
        logger.warning("'portfolio_variance_approx' missing; skipping portfolio variance.")
    # Stress testing metrics
    if 'scenario_loss' in df.columns:
        sl = df['scenario_loss'].to_numpy()
        logger.info("Scenario Loss total=%.4f, mean=%.4f", sl.sum(), sl.mean())
    else:
        logger.warning("'scenario_loss' missing; skipping stress testing metrics.")

    # Additional credit & risk metrics
    if 'probability_default' in df.columns:
        pd_col = df['probability_default'].to_numpy()
        logger.info("Probability of Default mean=%.4f", pd_col.mean())
    if 'expected_loss' in df.columns:
        el = df['expected_loss'].to_numpy()
        logger.info("Expected Loss total=%.4f, mean=%.4f", el.sum(), el.mean())
    if 'stress_delta' in df.columns:
        sd = df['stress_delta'].to_numpy()
        logger.info("Stress Delta mean=%.4f", sd.mean())

    # Predictive Modeling (Logistic Regression)
    pm_cols = ["exposure_at_default","loss_given_default","asset_volatility","probability_default"]
    if set(pm_cols).issubset(df.columns):
        predictive_modeling_default(df)
    else:
        missing = [c for c in pm_cols if c not in df.columns]
        logger.warning("Skipping predictive modeling, missing cols: %s", missing)

    # Time Series Forecast (ARIMA)
    ts_cols = {"event_date","exposure_at_default"}
    if ts_cols.issubset(df.columns):
        time_series_forecast(df)
    else:
        logger.warning("Skipping time-series forecast, missing 'event_date' or 'exposure_at_default'")

    # Fama-French 3-Factor Model
    ff_cols = ['R_m','R_f','SMB','HML','beta_market','beta_SMB','beta_HML']
    if set(ff_cols).issubset(df.columns):
        inputs = [df[c].to_numpy() for c in ff_cols]
        arr = fama_french_3_factor(*inputs)
        arr = np.array(arr, dtype=float)
        logger.info("Fama-French 3F expected excess return mean=%.4f, std=%.4f", arr.mean(), arr.std())
    else:
        missing = [c for c in ff_cols if c not in df.columns]
        logger.warning("Skipping Fama-French, missing cols: %s", missing)

    # Risk Scaling (Annualized volatility)
    if 'asset_volatility' in df.columns:
        vol = df['asset_volatility'].to_numpy()
        ann_vol = volatility_scaling(vol, 252)
        logger.info("Annualized Volatility (252d) mean=%.4f", ann_vol.mean())
    else:
        logger.warning("Skipping volatility scaling, 'asset_volatility' missing.")

    # Options Pricing (Black-Scholes)
    opt_cols = ['underlying_asset_price','option_strike_price','risk_free_rate','time_to_maturity','asset_volatility']
    if set(opt_cols).issubset(df.columns):
        S = df['underlying_asset_price'].to_numpy(); K = df['option_strike_price'].to_numpy()
        r = df['risk_free_rate'].to_numpy(); T = df['time_to_maturity'].to_numpy()
        sigma = df['asset_volatility'].to_numpy()
        call = black_scholes_call(S, K, r, T, sigma)
        arr = np.array(call, dtype=float)
        logger.info("Black-Scholes Call Price mean=%.4f", arr.mean())
    else:
        missing = [c for c in opt_cols if c not in df.columns]
        logger.warning("Skipping Black-Scholes pricing, missing cols: %s", missing)

    # Grouped Stress Test Loss by Asset Class
    if 'scenario_loss' in df.columns and 'asset_class' in df.columns:
        pdf = df.to_pandas()
        grp = pdf.groupby('asset_class')['scenario_loss'].sum()
        for grp_name, val in grp.items():
            logger.info("Scenario Loss total for %s: %.4f", grp_name, val)
    else:
        logger.warning("Skipping grouped stress test, missing 'scenario_loss' or 'asset_class'.")

if __name__ == "__main__":
    main()
