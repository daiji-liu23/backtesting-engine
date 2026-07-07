import pandas as pd


def extract_trades(equity_curve):
    position = equity_curve["position"]
    close = equity_curve["close"]

    trades = []
    current_position = 0
    entry_price = None
    entry_date = None

    for date, pos in position.items():
        if pos != current_position:
            if current_position != 0:
                exit_price = close.loc[date]
                trades.append({
                    "entry_date": entry_date,
                    "exit_date": date,
                    "entry_price": entry_price,
                    "exit_price": exit_price,
                    "return": current_position * (exit_price / entry_price - 1),
                })
            if pos != 0:
                entry_price = close.loc[date]
                entry_date = date
            current_position = pos

    if current_position != 0:
        exit_price = close.iloc[-1]
        trades.append({
            "entry_date": entry_date,
            "exit_date": close.index[-1],
            "entry_price": entry_price,
            "exit_price": exit_price,
            "return": current_position * (exit_price / entry_price - 1),
        })

    return pd.DataFrame(trades)
