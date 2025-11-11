from src.execution import Execution
# from src.strategy import Strategy
import mplfinance as mplf

class Plotting(Execution):

    def __init__(self):
        super().__init__()

    def plot_data(self):
        # df = self.stg_smma()
        df = self.buy_sell_signal()
        
        # print(df.tail())

        adsmma = [
            mplf.make_addplot(df["jaw"], color='red'),
            mplf.make_addplot(df["teeth"], color='yellow'),
            mplf.make_addplot(df["lips"], color='blue'),
            mplf.make_addplot(df["buy_price"], type='scatter', markersize=55, marker='^', color='green'),
        #     mplf.make_addplot(df["sell_price"], type='scatter', markersize=55, marker='v', color='black'),
            mplf.make_addplot(df["stoploss_long"], type='scatter', marker='_', markersize=80, color='red'),
        #     mplf.make_addplot(df["stoploss_short"], type='scatter', marker='_', markersize=80, color='red'),
            mplf.make_addplot(df["take_profit_long"], type='scatter', marker='_', markersize=80, color='blue'),
        #     mplf.make_addplot(df["take_profit_short"], type='scatter', marker='_', markersize=80, color='blue'),
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
# pl.backtest()