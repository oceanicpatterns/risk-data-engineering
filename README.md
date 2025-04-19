# Financial Risk & Data Engineering

---

## Key Formulas

This repository contains code and resources for financial risk analytics, including dynamic computation of risk metrics, backtesting, and data engineering workflows. Below is a comprehensive, clearly labeled table summarizing key formulas, their sections, and descriptions.

| **Section** | **Formula** | **Description** |
|:------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------|
| Basic Statistics | Mean: μ = (1/n) Σᵢ₌₁ⁿ xᵢ | Arithmetic average of a data set. |
| Basic Statistics | Variance: σ² = (1/n) Σᵢ₌₁ⁿ (xᵢ − μ)² | Measure of dispersion around the mean. |
| Basic Statistics | Standard Deviation: σ = √(Variance) | Measure of volatility around the mean. |
| Basic Statistics | Covariance: Cov(X,Y) = E[(X − μₓ)(Y − μᵧ)] | Degree to which two variables move together. |
| Basic Statistics | Correlation: ρ = Cov(X,Y)/(σₓσᵧ) | Standardized measure of linear association. |
| Probability Distributions | Normal PDF: f(x) = 1/√(2πσ²) exp[−(x − μ)²/(2σ²)] | Probability density function for a normal distribution. |
| Probability Distributions | Standard Normal PDF: f(z) = 1/√(2π) exp(−z²/2) | PDF for a normal distribution with μ = 0 and σ = 1. |
| Probability Distributions | Binomial PMF: P(X=k) = C(n,k) pᵏ (1−p)^(n−k) | Probability mass function for a binomial variable. |
| Probability Distributions | Poisson PMF: P(X=k)= (λᵏ exp(−λ))/k! | PMF for a Poisson‐distributed variable. |
| Time Value of Money | Future Value (FV): FV = PV (1 + r)ⁿ | Value in the future given present value PV and interest rate r. |
| Time Value of Money | Present Value (PV): PV = FV/(1 + r)ⁿ | Discounting future cash flows back to the present. |
| Time Value of Money | Annuity PV: PV = C [1 − (1 + r)^(−n)]/r | Present value of equal periodic cash flows. |
| Time Value of Money | Growing Annuity PV: PV = C [1 − ((1+g)/(1+r))ⁿ] / (r − g) | PV when cash flows grow at constant rate g. |
| Regression Analysis | OLS Slope: β = Σ(xᵢ −  x̄)(yᵢ −ȳ)/Σ(xᵢ − x̄)² | Estimator of slope in simple linear regression. |
| Regression Analysis | R² = 1 − (SS_res/SS_tot) | Proportion of variance explained by the regression. |
| Time Series | AR(1) Process: Xₜ = φXₜ₋₁ + εₜ | First-order autoregressive model. |
| Time Series | GARCH(1,1): σₜ² = ω + αεₜ₋₁² + βσₜ₋₁² | Model capturing volatility clustering in time series. |
| Portfolio Theory | Expected Return: E(Rₚ) = Σ wᵢ E(Rᵢ) | Portfolio’s weighted average return. |
| Portfolio Theory | Portfolio Variance: σₚ² = Σᵢ Σⱼ wᵢwⱼ Cov(Rᵢ,Rⱼ) | Variance combining individual risks and their covariances. |
| Portfolio Theory | CAPM: E(Rᵢ) = R_f + βᵢ (E(Rₘ) − R_f) | Expected return based on systematic risk. |
| Portfolio Theory | Beta: βᵢ = Cov(Rᵢ,Rₘ)/σₘ² | Measure of asset sensitivity to market movements. |
| Portfolio Theory | Efficient Frontier, Sharpe Ratio, etc. | Optimization formulas to select portfolios with maximum reward per unit risk. (Specific formulas depend on the model formulation.) |
| Risk Measures - VaR | Parametric VaR (Normal): VaR = μₚ − z₍α₎σₚ | Value at Risk assuming normally distributed returns. |
| Risk Measures - VaR | Historical Simulation VaR: (Empirical quantile of losses) | Non-parametric VaR using historical return distribution. |
| Risk Measures - VaR | Monte Carlo VaR: Simulated loss quantile from return distribution | VaR derived from simulated scenarios. |
| Risk Measures - Expected Shortfall | Expected Shortfall (ES): ES = E(loss | loss > VaR) | Average loss given that the loss exceeds VaR at a specified confidence level. |
| Risk Measures - Incremental/Marginal VaR | Incremental VaR: iVaR = VaR (portfolio + position) − VaR (portfolio) | Additional risk due to a new position. |
| Risk Measures - Incremental/Marginal VaR | Marginal VaR: ∂VaR/∂wᵢ | The sensitivity of portfolio VaR to a small change in asset weight. |
| Risk Measures - Stress Testing | Stress Loss: Loss_{stress} = Σ (Exposureᵢ × ΔRiskFactorᵢ) | Portfolio loss under a specified stress scenario (typically bespoke per institution). |
| Risk Measures - Stress Testing | Scenario Analysis: Change risk factors based on historical/crisis scenarios | Apply extreme but plausible changes to assess portfolio vulnerability. |
| Risk Measures - Liquidity Adjusted VaR | Liquidity-Adjusted VaR: LA–VaR = VaR (base) + (Additional liquidity risk term) | Adjust VaR to account for potential losses due to market illiquidity. |
| Derivatives | Black-Scholes Call Price: C = S₀N(d₁) − K exp(−rT) N(d₂) | Price of European call options under Black-Scholes assumptions. |
| Derivatives | d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T) | Intermediate variable in Black-Scholes for option pricing. |
| Derivatives | d₂ = d₁ − σ√T | Second intermediate variable in option pricing. |
| Derivatives | Put-Call Parity: C − P = S₀ − K exp(−rT) | Relationship linking call and put prices for European options. |
| Options Greeks | Delta (Δ): Δ = ∂V/∂S | Sensitivity of option price to small changes in the underlying asset price. |
| Options Greeks | Gamma (Γ): Γ = ∂²V/∂S² | Rate of change of delta as the underlying asset price changes. |
| Options Greeks | Theta (Θ): Θ = ∂V/∂t | Time decay of an option’s value. |
| Options Greeks | Vega: Vega = ∂V/∂σ | Sensitivity to changes in the volatility of the underlying asset. |
| Options Greeks | Rho: ρ = ∂V/∂r | Sensitivity to changes in the risk‐free interest rate. |
| Fixed Income | Bond Price: P = Σₜ [CFₜ/(1 + y)ᵗ] | Price of a bond as the sum of discounted future cash flows. |
| Fixed Income | Macaulay Duration: D = Σₜ [t × (CFₜ/(1+y)ᵗ)]/P | Weighted average time until cash flow receipt. |
| Fixed Income | Modified Duration: D_mod = D/(1+y) | Price sensitivity to yield changes. |
| Fixed Income | Convexity: Convexity = (1/P) Σₜ [t(t+1) CFₜ/(1+y)^(t+2)] | Measure of the curvature in the price-yield relationship. |
| Credit Risk | Expected Loss (EL): EL = PD × LGD × EAD | Average loss expectancy on a credit exposure. |
| Credit Risk | Distance to Default (Merton/KMV): DD = [ln(Assets/Liabilities) + (μ − σ²/2)T] / (σ√T) | Estimate of how far a firm is from default. |
| Credit Risk | Credit Spread (Approx.): Spread ≈ f(PD, LGD, Recovery Rate) | Model-dependent approximation connecting credit risk measures to yields. |
| Operational Risk | Basic Indicator Approach: Capital = α × Gross Income | Simplistic capital charge for operational risk based on income. |
| Operational Risk | Advanced Measurement Approach (AMA): Based on internal loss data & risk factors | No single formula; results are typically modelled via statistical loss distributions. |
| Risk-Adjusted Performance | Sharpe Ratio: SR = (E(Rₚ) − R_f)/σₚ | Performance per unit of total risk. |
| Risk-Adjusted Performance | Treynor Ratio: TR = (E(Rₚ) − R_f)/βₚ | Performance per unit of systematic risk. |
| Risk-Adjusted Performance | Jensen’s Alpha: α = Rₚ − [R_f + βₚ (Rₘ − R_f)] | Excess return over CAPM expected return. |
| Risk-Adjusted Performance | Information Ratio: IR = (Active Return)/(Tracking Error) | Reward to risk relative to a benchmark. |
| Multi-Factor Models | Fama-French 3-Factor: Rᵢ − R_f = α + β₁(Rₘ − R_f) + β₂SMB + β₃HML + ε | Asset returns explained by market, size, and value factors. |
| Risk Scaling | Time Scaling of Volatility: σ_T = σ_(1 day) √T | Scaling volatility for different time horizons under IID assumptions. |
| Returns | Log Return: r = ln(Pₜ/Pₜ₋₁) | Continuously compounded return over one period. |
| Returns | Arithmetic Return: r = (Pₜ − Pₜ₋₁)/Pₜ₋₁ | Simple return calculation for discrete periods. |
| Liquidity Risk | Bid-Ask Spread Models, Illiquidity Metrics | Formulas vary; often involve ratios of spread width to mid-price or adjustments to VaR. |
| Stress Test Metrics | Scenario Loss = Σ (Exposure_i × [Base Value_i − Stressed Value_i]) | Estimate of portfolio loss under a specified stress scenario. |
| Capital Adequacy | Risk-Weighted Assets (RWA): Sum (Exposure × Risk Weight) | Used to determine regulatory capital requirements. |
| Capital Adequacy | Minimum Capital Ratio: Capital/ RWA | Ensures banks have enough capital to absorb losses. |

---

> **Tip:** For LaTeX-style rendering of formulas, view this README on GitHub or in a Markdown viewer that supports math formatting.

---

## Usage of Python Scripts

 
- `src/formulas.py`: Compute and log core risk metrics (EAD, VaR, ES, Black-Scholes, liquidity, etc.) on curated data.
- `src/advanced_risk_analytics.py`: Provides predictive modeling (logistic regression for default risk) and time-series forecasting (ARIMA).
- `src/generate_bulk_seed_data.py`: Bulk-generate dummy seed data for backtesting and experiments.
- `seeds/seed_data.csv`: Sample risk data used as input for analytics scripts.
- `models/curated_risk_data.sql`: SQL model defining the curated risk data pipeline.

## SQLMesh Command Reference

Below are the most common SQLMesh commands and what they do:

### `sqlmesh plan`
- **Purpose:** Computes a migration plan based on changes in your models or configuration.
- **What it does:**
  - Detects what has changed (new/modified/removed models, schema changes, etc.).
  - Shows a summary of changes and potential impacts.
  - Can be run interactively to review and approve changes before applying.
- **When to use:**
  - After making changes to models or configs, before applying them to your data warehouse.

### `sqlmesh apply`
- **Purpose:** Applies the migration plan to your data warehouse/database.
- **What it does:**
  - Executes the changes computed by `sqlmesh plan`.
  - Updates tables, views, and other objects as needed.
  - Can be run non-interactively for automation.
- **When to use:**
  - After reviewing the plan, to make your changes take effect.

### `sqlmesh run` / `sqlmesh run --verbose`
- **Purpose:** Executes the entire SQLMesh project pipeline.
- **What it does:**
  - Builds and materializes all models, in dependency order.
  - Applies all transformations and scheduling as defined in your project.
  - `--verbose` gives detailed logs for debugging or understanding execution.
- **When to use:**
  - To fully build or refresh your project, especially after initialization or major changes.
  - For debugging or CI/CD pipelines.

---

| Command                  | What it does                                       | When to use                        |
|--------------------------|---------------------------------------------------|------------------------------------|
| `sqlmesh plan`           | Shows migration plan for model/config changes      | After edits, before applying       |
| `sqlmesh apply`          | Applies the migration plan to your warehouse       | After reviewing/approving the plan |
| `sqlmesh run`            | Runs the full pipeline, builds all models          | Full builds, refresh, CI/CD        |
| `sqlmesh run --verbose`  | Same as above, with detailed logs                  | Debugging, troubleshooting         |

---

## SQLMesh Project Initialization Steps

If you encounter errors about missing SQL dialect or project config, follow these steps:

1. **Check your `config.yaml` file:**
   - It should match your actual `config.yaml`, for example:
     ```yaml
     gateways:
       duckdb:
         connection:
           type: duckdb
           database: db.db

     default_gateway: duckdb

     model_defaults:
       dialect: duckdb
       start: '2025-04-16'
     ```
   - Ensure indentation uses spaces (no tabs) and the file ends with a newline.

2. **Initialize SQLMesh:**
   - Run:
     ```sh
     sqlmesh init
     ```
   - If you see an error about missing SQL dialect, try:
     ```sh
     sqlmesh init duckdb
     ```
   - This explicitly sets the dialect for initialization and can bypass config parsing issues.

3. **Run your project:**
   - Use:
     ```sh
     sqlmesh run --verbose
     ```

**Tip:** Once your config is correct, you should not need to specify the dialect every time.

---

## Requirements

- Python 3.9+

---

## Usage

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd risk_management
   ```
2. (Recommended) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

---

## About

This project is designed for students in risk management, finance, and data engineering. It provides a quick reference to formulas and concepts used in quantitative finance and risk analysis.

---

## License

MIT License
