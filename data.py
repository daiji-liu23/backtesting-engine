import yfinance as yf
import pandas as pd
import numpy as np
import openpyxl

def load_price_data(ticker, start, end): 
    if isinstance(ticker, str): 
        ticker = [ticker]
    
    df = yf.download(ticker, start=start, end=end, interval = "1d", progress=True, auto_adjust=True,
                     group_by="Ticker")  

    result = {}
    for tickers in ticker:
        if isinstance(df.columns, pd.MultiIndex):
            df_clean = df[tickers].dropna().copy()
        else:
            df_clean = df

        df_clean.to_csv(f"{tickers}.csv")
        result[tickers] = df_clean
    return result  



def Moving_Average_Strategy(data, fast : int = 20, slow: int = 50):  # Fast -> short-term, # slow -> long-term

    fast_ma = data["Close"].rolling(window=fast).mean()
    slow_ma = data["Close"].rolling(window=slow).mean()

    signal = pd.Series(0, data.index)   
    signal[fast_ma > slow_ma] = 1 
    signal[fast_ma.isna() | slow_ma.isna()] = 0 


    return signal


def buy_and_hold(data):
    return pd.Series(1, index=data.index)


def rsi_strategy(data, period: int = 14, oversold: int = 30, overbought: int = 70):
    delta = data["Close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    signal = pd.Series(np.nan, index=data.index)
    signal[rsi < oversold] = 1   # oversold -> enter long, betting on a bounce
    signal[rsi > overbought] = 0  # overbought -> exit back to flat

    return signal.ffill().fillna(0)


class Backtest:
    def __init__(self, data, strategy, inital_position): 
        self.data = data
        self.strategy = strategy   
        self.inital_position = inital_position
    
    def run(self):
        signals = self.strategy(self.data)
        position = signals.shift(1).fillna(0) 

        daily_return = self.data["Close"].pct_change().fillna(0) 
        
        strategy_return = position * daily_return 
        equity = (1 + strategy_return).cumprod() * self.inital_position

        self.equity_curve = pd.DataFrame({
            "close": self.data["Close"],
            "position": position,
            "return": strategy_return,
            "equity": equity,
        }) 
        return self


if __name__ == "__main__":
    appl_df = load_price_data(["AAPL", "MSFT", "MU"], "2025-01-01", "2026-01-01")
    bt = Backtest(appl_df["AAPL"], Moving_Average_Strategy, 100000).run()














    



1