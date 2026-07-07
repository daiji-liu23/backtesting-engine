import pandas as pd

from data import Moving_Average_Strategy, buy_and_hold, rsi_strategy


def _price_data(closes):
    dates = pd.date_range("2024-01-01", periods=len(closes))
    return pd.DataFrame({"Close": closes}, index=dates)


def test_buy_and_hold_always_long():
    data = _price_data([10, 20, 30, 5])
    signal = buy_and_hold(data)
    assert (signal == 1).all()
    assert list(signal.index) == list(data.index)


def test_moving_average_strategy_known_crossover():
    # fast(2)/slow(3) rolling means hand-traced: crosses up at idx 3, crosses back down (equal) at idx 5
    data = _price_data([10, 10, 10, 20, 20, 20, 20, 20])
    signal = Moving_Average_Strategy(data, fast=2, slow=3)
    assert signal.tolist() == [0, 0, 0, 1, 1, 0, 0, 0]


def test_rsi_strategy_enters_oversold_exits_overbought():
    # steady decline drives RSI to 0 (oversold -> enter long), steady rise drives it to 100 (overbought -> exit)
    # note: delta.diff()'s first NaN fails the `> 0`/`< 0` checks in .where(), so it's treated as 0
    # gain/loss (not NaN) -- RSI has a valid value one bar earlier than a naive hand-trace expects.
    data = _price_data([100, 90, 80, 70, 60, 70, 80, 90, 100, 110])
    signal = rsi_strategy(data, period=3, oversold=30, overbought=70)
    assert signal.tolist() == [0, 0, 1, 1, 1, 1, 1, 0, 0, 0]
