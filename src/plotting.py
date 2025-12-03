from src.execution import Execution
import mplfinance as mplf


class Plotting(Execution):

    def __init__(self):
        super().__init__()
        self.plot_data()

    def plot_data(self):
        df = self.buy_sell_price()
    
        adsmma = [
            mplf.make_addplot(df["jaw"], color='red'),
            mplf.make_addplot(df["teeth"], color='yellow'),
            mplf.make_addplot(df["lip"], color='blue'),
            mplf.make_addplot(df['long_buy_price'], type='scatter', markersize=50, marker='^', color='blue'),
            mplf.make_addplot(df['long_sell_price'], type='scatter', markersize=50, marker='<', color='red'),
            mplf.make_addplot(df['short_buy_price'], type='scatter', markersize=50, marker='v', color='black'),
            mplf.make_addplot(df['short_sell_price'], type='scatter', markersize=50, marker='<', color='green'),
            mplf.make_addplot(df['long_tp'], type='scatter', markersize=21, marker='_', color='blue'),
            mplf.make_addplot(df['long_sl'], type='scatter', markersize=21, marker='_', color='red'),
            mplf.make_addplot(df['short_sl'], type='scatter', markersize=21, marker='_', color='black'),
            mplf.make_addplot(df['short_tp'], type='scatter', markersize=21, marker='_', color='green'),
        ]

        mplf.plot(
            df,
            type='candle',
            style='yahoo',
            title="Smoothed Moving Average",
            addplot=adsmma,
            volume=False,
            ylabel='Price',
            figratio=(12, 8),
            figscale=1.2,
        )

Plotting()
