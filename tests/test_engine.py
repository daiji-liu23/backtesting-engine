import pandas as pd
import pytest

from engine import extract_trades


def _equity_curve(position, close):
    dates = pd.date_range("2024-01-01", periods=len(position))
    return pd.DataFrame({"position": position, "close": close}, index=dates)


def test_extract_trades_long_then_flat():
    ec = _equity_curve([0, 1, 1, 0], [100, 101, 105, 103])
    trades = extract_trades(ec)
    assert len(trades) == 1
    trade = trades.iloc[0]
    assert trade["entry_price"] == 101
    assert trade["exit_price"] == 103
    assert trade["return"] == pytest.approx(103 / 101 - 1)


def test_extract_trades_short_position_profits_when_price_falls():
    ec = _equity_curve([0, -1, -1, 0], [100, 95, 90, 92])
    trades = extract_trades(ec)
    assert len(trades) == 1
    assert trades.iloc[0]["return"] == pytest.approx(-1 * (92 / 95 - 1))


def test_extract_trades_still_open_closes_at_last_price():
    ec = _equity_curve([0, 1, 1], [100, 105, 110])
    trades = extract_trades(ec)
    assert len(trades) == 1
    assert trades.iloc[0]["exit_price"] == 110


def test_extract_trades_no_trades():
    ec = _equity_curve([0, 0, 0], [100, 101, 102])
    trades = extract_trades(ec)
    assert trades.empty


def test_extract_trades_multiple_trades():
    ec = _equity_curve([0, 1, 1, 0, 1, 1], [100, 101, 105, 103, 110, 115])
    trades = extract_trades(ec)
    assert len(trades) == 2
    assert trades.iloc[0]["entry_price"] == 101
    assert trades.iloc[0]["exit_price"] == 103
    assert trades.iloc[1]["entry_price"] == 110
    assert trades.iloc[1]["exit_price"] == 115
