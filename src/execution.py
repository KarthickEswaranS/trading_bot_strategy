from src.strategy import Strategy
import numpy as np
import mplfinance as mplf

class Execution(Strategy):

    def __init__(self):
        super().__init__()
    
    def buy_sell_signal(self):

        df = self.stg_smma()
        
        df['long_signal'] = (
            (df['lips'].shift(1) < df['teeth'].shift(1)) &
            (df['lips'] > df['teeth']) &
            (df['lips'] > df['jaw']) 
        )

        df['short_signal'] = (
            (df['lips'].shift(1) > df['teeth'].shift(1)) &
            (df['lips'] < df['teeth']) &
            (df['lips'] < df['jaw']) 
        )

        df["buy_price"] = np.where(df["long_signal"], df["Close"], np.nan)
        df["sell_price"] = np.where(df["short_signal"], df["Close"], np.nan)

        df["stoploss_long"]= np.where(df["long_signal"],df["Low"].shift(1), np.nan)
        df["stoploss_short"]= np.where(df["short_signal"],df["High"].shift(1), np.nan)

        # df["target_long"]= np.where(df["long_signal"],df["Low"].shift(1), np.nan)
        # df["target_short"]= np.where(df["short_signal"],df["High"].shift(1), np.nan)
    
        return df
    
    def plotting(self):
        df = self.buy_sell_signal()
        print(df)

        adsmma = [
            mplf.make_addplot(df["jaw"], color='red'),
            mplf.make_addplot(df["teeth"], color='yellow'),
            mplf.make_addplot(df["lips"], color='blue'),
            mplf.make_addplot(df["buy_price"], type='scatter', markersize=120, marker='^', color='green'),
            mplf.make_addplot(df["sell_price"], type='scatter', markersize=120, marker='v', color='red'),
            mplf.make_addplot(df["stoploss_long"], type='scatter', marker='_', markersize=80, color='purple'),
            mplf.make_addplot(df["stoploss_short"], type='scatter', marker='_', markersize=80, color='purple'),
        ]

        mplf.plot(
            df,
            type='candle',
            style='yahoo',
            title="Candlestick + SMMA Alligator (Lips cross Teeth & Jaw)",
            addplot=adsmma,
            volume=False,
            ylabel='Price',
            figratio=(12, 8),
            figscale=1.2,
            tight_layout=True,
        )

ex = Execution()
ex.plotting()