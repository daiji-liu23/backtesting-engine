import pandas as pd
import pytest

from data import Backtest, buy_and_hold


def test_backtest_shifts_position_and_compounds_equity():
    dates = pd.date_range("2024-01-01", periods=4)
    data = pd.DataFrame({"Close": [100, 110, 121, 133.1]}, index=dates)

    bt = Backtest(data, buy_and_hold, 1000).run()
    curve = bt.equity_curve

    # first bar's position must be 0 -- can't act on day 0's signal until day 1 (lookahead avoidance)
    assert curve["position"].iloc[0] == 0
    assert curve["position"].iloc[1:].tolist() == [1, 1, 1]

    assert curve["equity"].tolist() == pytest.approx([1000, 1100, 1210, 1331])
