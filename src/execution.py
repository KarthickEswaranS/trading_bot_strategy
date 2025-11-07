from src.strategy import Strategy
import numpy as np
import mplfinance as mplf

class Execution(Strategy):

    def __init__(self):
        super().__init__()
    
    def buy_sell_signal(self):

        df = self.stg_smma()
        
        df['long_signal'] = (
            (df['lips'].shift(1) < df['teeth']) &
            (df['lips'] > df['teeth']) &
            (df['lips'] > df['jaw']) 
        )

        df['short_signal'] = (
            (df['lips'].shift(1) > df['teeth']) &
            (df['lips'] < df['teeth']) &
            (df['lips'] < df['jaw']) 
        )

        self.buy(df)
        self.sell(df)

        return df
    
    def buy(self, buy_signal, tp=0.03, sl=0.01):
        df = buy_signal
        df["buy_price"] = np.where(df["long_signal"], df["Open"], np.nan)
        df["stoploss_long"]= np.where(df["long_signal"],df["Open"] * (1-sl), np.nan)
        df["take_profit_long"]= np.where(df["long_signal"],df["Close"] * (1+tp), np.nan)

        return df
    
    def sell(self, sell_signal, tp=0.03, sl=0.01):
        df = sell_signal
        df["sell_price"] = np.where(df["short_signal"], df["Open"], np.nan)
        df["stoploss_short"]= np.where(df["short_signal"],df["Open"] * (1+sl), np.nan)
        df["take_profit_short"]= np.where(df["short_signal"],df["Close"] * (1-tp), np.nan)

        return df
    

    def backtest(self):
        """Simulate trades and compute performance metrics."""
        df = self.buy_sell_signal()
        trades = []

        for i in range(len(df)):
            # --- LONG TRADE SIMULATION ---
            if df.iloc[i]['long_signal']:
                entry = df.iloc[i]['Close']
                tp = df.iloc[i]['take_profit_long']
                sl = df.iloc[i]['stoploss_long']

                # simulate forward price movement
                for j in range(i + 1, len(df)):
                    low = df.iloc[j]['Low']
                    high = df.iloc[j]['High']

                    # check TP hit first
                    if high >= tp:
                        profit = (tp - entry)
                        trades.append(profit)
                        break

                    # check SL hit
                    elif low <= sl:
                        profit = (sl - entry)
                        trades.append(profit)
                        break

            # --- SHORT TRADE SIMULATION ---
            elif df.iloc[i]['short_signal']:
                entry = df.iloc[i]['Close']
                tp = df.iloc[i]['take_profit_short']
                sl = df.iloc[i]['stoploss_short']

                for j in range(i + 1, len(df)):
                    low = df.iloc[j]['Low']
                    high = df.iloc[j]['High']

                    # check TP hit first (price falls)
                    if low <= tp:
                        profit = (entry - tp)
                        trades.append(profit)
                        break

                    # check SL hit
                    elif high >= sl:
                        profit = (entry - sl)
                        trades.append(profit)
                        break

        # --- Performance summary ---
        if len(trades) > 0:
            total_trades = len(trades)
            wins = len([p for p in trades if p > 0])
            losses = len([p for p in trades if p < 0])
            win_rate = (wins / total_trades) * 100
            total_profit = sum(trades)
            avg_profit = np.mean(trades)

            print(f"📊 Total Trades: {total_trades}")
            print(f"✅ Wins: {wins} | ❌ Losses: {losses}")
            print(f"🏆 Win Rate: {win_rate:.2f}%")
            print(f"💰 Total Profit: {total_profit:.2f}")
            print(f"📈 Average P/L per trade: {avg_profit:.4f}")
        else:
            print("No trades triggered.")

        return df
