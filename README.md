# Backtesting Engine

Run a trading strategy against historical price data and get back Sharpe ratio, max drawdown, win rate, and an equity curve chart.

## Install

```
pip install -r requirements.txt
```

## Usage

```
python main.py --tickers AAPL --start 2018-01-01 --end 2024-01-01
python main.py --tickers AAPL MSFT --start 2018-01-01 --end 2024-01-01 --strategy ma_crossover --fast 10 --slow 30 --capital 50000
python main.py --tickers AAPL --start 2018-01-01 --end 2024-01-01 --strategy buy_and_hold
python main.py --tickers AAPL --start 2018-01-01 --end 2024-01-01 --strategy rsi --rsi-period 14 --rsi-oversold 30 --rsi-overbought 70
```

Output: metrics printed to the console, one chart PNG per ticker saved to `output/`.

## Strategies

| name | function | description |
|---|---|---|
| `ma_crossover` (default) | `Moving_Average_Strategy` | Long while the fast moving average is above the slow one, trend-following |
| `buy_and_hold` | `buy_and_hold` | Always long — baseline to compare other strategies against |
| `rsi` | `rsi_strategy` | Mean-reversion — enters long when RSI drops below `--rsi-oversold`, exits when it rises above `--rsi-overbought` |

## Writing a strategy

A strategy is a plain function that takes the price DataFrame and returns a position per bar (`1` = long, `0` = flat, `-1` = short):

```python
def my_strategy(data: pd.DataFrame, **params) -> pd.Series:
    ...
    return signal
```

To plug in a new one:
1. Add the function to `data.py` (where the other strategies currently live).
2. Register it in the `STRATEGIES` dict in `main.py`, and add a matching entry in `STRATEGY_PARAMS` that builds its kwargs from `args` (add any new CLI flags it needs to `parse_args()`).

## Running tests

```
pip install -r requirements-dev.txt
pytest
```

The suite (`tests/`) only covers the deterministic logic — `metrics.py`, `engine.py`'s trade extraction, the strategy functions, and `Backtest` — using small hand-built price series instead of live yfinance calls, so it runs instantly and doesn't depend on network access or market data changing. `load_price_data` itself isn't covered here; sanity-check it by actually running `main.py` (see Usage above).

## Gotchas

- `Backtest.run()` already shifts the position by one bar before applying it to returns (`signals.shift(1)`), so the strategy can't act on a signal until the bar after it fires — this avoids lookahead bias. Don't recompute or re-shift this elsewhere.
- Price data uses `auto_adjust=True`, so `Close` is already split/dividend-adjusted. Don't mix it with raw close values.
- `Backtest.run()` currently has no commission/slippage modeling — returns are gross, not net of trading costs.
