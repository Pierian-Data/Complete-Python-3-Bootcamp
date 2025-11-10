# FX Volatility Trading Analytics Prototype

## P&L Delta-Hedging Mockup (Call, 1-Day Tenor)
Using the required long-option perspective and r = 0, the example below follows a 100 million USD notional EURUSD call with strike 1.1000, initial spot 1.1000, **constant** implied volatility 10% (annualised), tenor 24 hours, and hedging every six hours. Spot path (in USD per EUR): 1.1000 → 1.1050 → 1.0950 → 1.1020 → 1.1070.

| Time (h) | Spot  | Tau (yrs) | σ (kept at 10%) | Delta | Hedge action (Δ) | Hedge P&L vs expiry (USD) | Cum. hedge P&L (USD) |
|---------:|:------|:----------|:----------------|:------|:-----------------|--------------------------:|---------------------:|
| 0        | 1.1000 | 0.002740 | 0.1000          | 0.5010 | Sell 0.5010 × 100m | -318,846.23 | -318,846.23 |
| 6        | 1.1050 | 0.002055 | 0.1000          | 0.8420 | Sell 0.3410 × 100m | -61,712.95 | -380,559.18 |
| 12       | 1.0950 | 0.001370 | 0.1000          | 0.1095 | Buy 0.7325 × 100m  | +802,722.31 | +422,163.12 |
| 18       | 1.1020 | 0.000685 | 0.1000          | 0.7566 | Sell 0.6471 × 100m | -293,591.15 | +128,571.97 |
| 24       | 1.1070 | 0        | –               | 1.0000 | Buy 0.2434 × 100m  |       0.00 | +128,571.97 |

- **Premium paid at t=0:** 0.00229697 × 100m = 229,697.26 USD
- **Hedge gains/losses:** Sum of expiry-referenced hedge P&Ls (–318,846.23 – 61,712.95 + 802,722.31 – 293,591.15) = +128,571.97 USD
- **Intrinsic value at expiry:** max(1.1070 – 1.1000, 0) × 100m = 700,000.00 USD
- **Total P&L:** -Premium + Hedge P&L + Intrinsic = -229,697.26 + 128,571.97 + 700,000.00 = **+598,874.71 USD**

For path-dependent monitoring before expiry you can still track `P&L(t) = -Premium_paid + Cumulative_hedge_P&L(t) + Option_MTM(t)` using the running delta-hedge P&L and option mark-to-market at each hedge timestamp.

### Realised Volatility Example
Using the same four six-hour log returns, the **sum of squared returns** is 0.000164313. For a one-day horizon (24 hours ≈ 1/365 years) the annualised realised volatility is:

```
σ_realised = sqrt((∑ r_i²) × 365) = 24.49%
```

This matches the standard realised-variance definition `∑ r_i² / Δt_years` where `Δt_years = 1/365` for a 24-hour sample.

### Notional Standardisation Logic
- Quote currency is USD (e.g. EURUSD, GBPUSD): **use 100 million USD notional**; P&L reported in USD.
- Base currency is USD (e.g. USDJPY, USDCHF): **use 100 million units of the quote currency** (JPY, CHF, etc.). P&L is produced in that quote currency and displayed as unitless for cross-comparison.
- Cross pairs without USD (e.g. AUDCHF, EURJPY): **use 100 million units of the quote currency**. Calculations occur in that currency, results shown as unitless multiples of the 100m-equivalent notionals.

These rules align every trade near a 100 million USD exposure so that P&L figures remain comparable across currency pairs.

---

The remainder of this README explains how to run the in-browser prototype once built.

## Running the Prototype
1. Open `index.html` in any modern browser (Chrome, Edge, Firefox, Safari). No server is required—the app runs entirely in the browser.
2. Upload the spot time-series workbook:
   - First sheet only is processed.
   - Include a column named `timestamp` (Excel datetime or ISO string) and one column per currency pair (e.g. `EURUSD`, `USDJPY`).
   - Provide at least the time range that covers the tenors you wish to analyse.
3. Upload the implied volatility workbook:
   - First sheet only is processed.
   - Required columns (case-insensitive): `pair`, `option_type` (`Call`/`Put`), `tenor_hours` (or `tenor_days`), `strike_label`, `implied_vol` (decimal, 0.10 = 10%).
   - `strike_label` is the bucket shown in the heatmap/ranking (e.g. `ATM`, `25D Call`, `10D Put`). If the column is left blank the app auto-labels using the provided strike/delta: `ATM` for ~50Δ, `25ΔC`/`25ΔP` for delta buckets, or `K=1.1050` when only an absolute strike exists.
   - Optional: `strike` (explicit strike) or `delta_target` (to back out the strike).
   - Any additional commentary columns are ignored.
4. Choose the currency pairs and strike buckets to analyse (leave empty to take all), select hedging frequency (10, 30, or 60 minutes), and pick the variance decay model.
5. Click **Run P&L Simulation** to generate the dashboard. Click any P&L cell to view its path-decomposition chart.
6. Download the Excel report for the full hedge-by-hedge breakdown and summary table.

### Variance Decay Options
- **Standard √t decay:** σ(t) = σ₀ × √(t_remaining / t_total).
- **Flat:** Keeps σ constant throughout the life of the trade.
- **Event-weighted window:** Allocate a chosen share of total variance to a specific hour-window (e.g. central-bank announcement). The remaining variance is distributed proportionally outside the window; the engine recomputes σ(t) from the residual variance budget.

### Output Overview
- **P&L heatmap:** Currency vs strike/tenor grid colour-coded by total P&L (per 100m notional).
- **P&L rankings:** Top and bottom five trades.
- **Volatility comparison:** Implied vs realised σ, with flags where P&L contradicts the vol differential (e.g. realised > implied but trade loses money).
- **Interactive chart:** Premium, hedge P&L, option MTM, and total P&L lines over time.
- **Excel export:** `Summary` (per-trade metrics) and `HedgePaths` (hedge-by-hedge records with timestamps, deltas, MTM, and cumulative P&L).

### Notes and Assumptions
- Risk-free and foreign rates are fixed at zero, matching the short-dated setup.
- Hedging is discrete at the chosen frequency and ignores transaction costs.
- Spot prices are assumed to be clean post any Monday-market filtering; pre-processing should remove stale values.
- If spot data ends before a tenor expires, that trade is flagged and excluded.
- All P&L values are shown both in the underlying currency (per the notional convention) and implicitly as a unitless number by dividing by 100 million.
- The browser loads SheetJS' `xlsx.full.min.js` automatically. If your environment blocks CDNs, download that file and place it alongside `index.html` so the local fallback is picked up.

### Future Enhancements
- Incorporate transaction costs and slippage controls.
- Allow custom strikes in delta or absolute terms directly inside the UI.
- Persist historical runs for longitudinal analysis.
- Add gamma-weighted realised volatility metrics.
- Connect to upstream APIs (Bloomberg, internal data lakes) once permissions are available.
