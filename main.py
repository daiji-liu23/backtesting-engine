import argparse
import functools
import os

from data import load_price_data, Backtest, Moving_Average_Strategy, buy_and_hold, rsi_strategy
from engine import extract_trades
from metrics import sharpe_ratio, max_drawdown, win_rate
from charts import plot_equity_curve

STRATEGIES = {
    "ma_crossover": Moving_Average_Strategy,
    "buy_and_hold": buy_and_hold,
    "rsi": rsi_strategy,
}

# Each strategy takes different parameters, so build its kwargs from args separately.
STRATEGY_PARAMS = {
    "ma_crossover": lambda args: {"fast": args.fast, "slow": args.slow},
    "buy_and_hold": lambda args: {},
    "rsi": lambda args: {
        "period": args.rsi_period,
        "oversold": args.rsi_oversold,
        "overbought": args.rsi_overbought,
    },
}


def parse_args():
    parser = argparse.ArgumentParser(description="Run a backtest against historical price data.")
    parser.add_argument("--tickers", nargs="+", required=True, help="One or more ticker symbols, e.g. AAPL MSFT")
    parser.add_argument("--start", required=True, help="Start date, YYYY-MM-DD")
    parser.add_argument("--end", required=True, help="End date, YYYY-MM-DD")
    parser.add_argument("--strategy", choices=STRATEGIES.keys(), default="ma_crossover")
    parser.add_argument("--fast", type=int, default=20, help="Fast moving average window (ma_crossover)")
    parser.add_argument("--slow", type=int, default=50, help="Slow moving average window (ma_crossover)")
    parser.add_argument("--rsi-period", type=int, default=14, help="RSI lookback window (rsi)")
    parser.add_argument("--rsi-oversold", type=float, default=30, help="RSI entry threshold (rsi)")
    parser.add_argument("--rsi-overbought", type=float, default=70, help="RSI exit threshold (rsi)")
    parser.add_argument("--capital", type=float, default=100_000, help="Starting capital")
    parser.add_argument("--output-dir", default="output", help="Folder for chart PNGs")
    return parser.parse_args()


def main():
    args = parse_args()
    os.makedirs(args.output_dir, exist_ok=True)

    price_data = load_price_data(args.tickers, args.start, args.end)
    strategy_kwargs = STRATEGY_PARAMS[args.strategy](args)
    strategy_fn = functools.partial(STRATEGIES[args.strategy], **strategy_kwargs)

    for ticker in args.tickers:
        data = price_data[ticker]
        bt = Backtest(data, strategy_fn, args.capital).run()
        trades = extract_trades(bt.equity_curve)

        sharpe = sharpe_ratio(bt.equity_curve["return"])
        mdd = max_drawdown(bt.equity_curve["equity"])
        wr = win_rate(trades)

        print(f"\n{ticker}")
        print(f"  Sharpe ratio:   {sharpe:.2f}")
        print(f"  Max drawdown:   {mdd:.2%}")
        print(f"  Win rate:       {wr:.2%} ({len(trades)} trades)")

        chart_path = os.path.join(args.output_dir, f"{ticker}_equity.png")
        plot_equity_curve(bt.equity_curve, chart_path)
        print(f"  Chart saved:    {chart_path}")


if __name__ == "__main__":
    main()
