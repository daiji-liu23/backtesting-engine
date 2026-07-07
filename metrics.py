import numpy as np


def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
    excess_returns = returns - risk_free_rate / periods_per_year
    std = excess_returns.std()
    if std == 0:
        return 0.0
    return (excess_returns.mean() / std) * np.sqrt(periods_per_year)


def drawdown_series(equity):
    running_max = equity.cummax()
    return (equity - running_max) / running_max


def max_drawdown(equity):
    return drawdown_series(equity).min()


def win_rate(trades):
    if trades.empty:
        return 0.0
    return (trades["return"] > 0).mean()
