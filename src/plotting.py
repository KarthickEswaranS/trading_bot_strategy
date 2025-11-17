from src.execution import Execution
# from src.strategy import Strategy
import mplfinance as mplf
import pandas as pd

class Plotting(Execution):

    def __init__(self):
        super().__init__()

    def plot_data(self):
        df = self.long_signal()
    
        adsmma = [
            mplf.make_addplot(df["jaw"], color='red'),
            mplf.make_addplot(df["teeth"], color='yellow'),
            mplf.make_addplot(df["lips"], color='blue'),
            mplf.make_addplot(df['buy_price'], type='scatter', markersize=50, marker='^', color='blue'),
            mplf.make_addplot(df['sell_price'], type='scatter', markersize=50, marker='v', color='red'),
            mplf.make_addplot(df['sl_long'], type='scatter', markersize=21, marker='_', color='black'),
            mplf.make_addplot(df['tp_long'], type='scatter', markersize=21, marker='_', color='orange'),
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
        )

pl = Plotting()
pl.plot_data()