import pandas as pd
import pytest

from metrics import sharpe_ratio, drawdown_series, max_drawdown, win_rate


def test_sharpe_ratio_known_values():
    returns = pd.Series([0.01, -0.01, 0.02, -0.02, 0.01])
    expected = (returns.mean() / returns.std()) * (252 ** 0.5)
    assert sharpe_ratio(returns) == pytest.approx(expected)


def test_sharpe_ratio_zero_std_returns_zero():
    returns = pd.Series([0.0, 0.0, 0.0, 0.0])
    assert sharpe_ratio(returns) == 0.0


def test_drawdown_series_known_case():
    equity = pd.Series([100, 110, 90, 95, 120])
    dd = drawdown_series(equity)
    assert dd.tolist() == pytest.approx([0.0, 0.0, -20 / 110, -15 / 110, 0.0])


def test_max_drawdown_is_worst_point():
    equity = pd.Series([100, 110, 90, 95, 120])
    assert max_drawdown(equity) == pytest.approx(-20 / 110)


def test_win_rate_basic():
    trades = pd.DataFrame({"return": [0.05, -0.02, 0.01, -0.01]})
    assert win_rate(trades) == 0.5


def test_win_rate_empty_trades():
    trades = pd.DataFrame({"return": []})
    assert win_rate(trades) == 0.0
