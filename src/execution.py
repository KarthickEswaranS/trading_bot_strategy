from src.strategy import Strategy
import numpy as np
import mplfinance as mplf

class Execution(Strategy):

    def __init__(self):
        super().__init__()
        self.initial_capital = 100000
        self.lot_size = 1
        self.balance = self.initial_capital
        self.data = self.stg_smma()

    def buy_sell_signal(self):

        df = self.data
        
        df['long_signal'] = (
            # Accumulation
            ((df['lips'] != df["teeth"]) & (df['lips'] != df["jaw"])) &
            (df['teeth'] != df["jaw"]) &

            # (df['lips'].shift(1) <= df['teeth'].shift(1)) &
            ((df['lips'] > df['teeth']) & (df['teeth'] > df['jaw'])) & 
            (df['Close'] > df['lips']) 
          
        )

        df['short_signal'] = (
            # Accumulation
            ((df['lips'] != df["teeth"]) & (df['lips'] != df["jaw"])) &
            (df['teeth'] != df["jaw"]) &

            # (df['lips'].shift(1) >= df['teeth'].shift(1)) &
            ((df['lips'] < df['teeth']) & (df['teeth'] < df['jaw'])) & 
            (df['Close'] < df['lips']) 
            
        )

        self.buy(df)
        # self.sell(df)

        return df
    
    def buy(self, buy_signal_data, ):
        df = buy_signal_data
        sl=0.01
        tp = 0.03

        df["in_trade"] = False
        in_trade = False
        entry_price = 0

        df["buy_price"] = np.where(df["long_signal"], df["Close"], np.nan)
        df["stoploss_long"]= np.where(df["long_signal"],df["Low"] * (1-sl), np.nan)
        entry_price = df.index[df['long_signal'] == True].tolist()

        for idx in entry_price:
           entry_price = df.loc[idx, "buy_price"]
           print(f"Entry at index {idx}, price: {entry_price}")
        # for i in range(len(df)):

        #     if not in_trade and entry_price.iloc[i]:
        #         in_trade = True
        #         df.loc[i, 'buy_price'] = entry_price
        #         df.loc[i , 'sl_long'] = df['Close'].iloc[i] * (1-sl)
        #         df.loc[i , 'in_trade'] = True
            
        #     elif in_trade :
        #         df.loc[i, 'in_trade'] = True
                 
        #         if df["lips"].iloc[i] < df['teeth'].iloc[i]:
        #             df.loc[i, 'exit_price'] = df['Close'].iloc[i]
        #         else:
        #             df.loc[i, "exit_price"] = np.nan

        # return df


        
        
        # for i  in  range(len(df)):
        #  exit_condition =
        #  if exit_condition:
        #    df["take_profit_long"]= np.where(df["long_signal"], df["Close"] * (1+tp), np.nan)

    
    # def sell(self, sell_signal_data, sl=0.01):
        # df = sell_signal_data
        # tp = 0.02

        # df['sell_price'] = np.nan
        # df['tp_short'] = np.nan
        # df['sl_short'] = np.nan
        # df['in_trade'] = np.nan

        # in_trade = False
        # entry_price = 0

        # for i in range(len(df)):
        #     if not in_trade and df['short_signal'].iloc[i]:
        #         in_trade = True
        #         entry_price = df['Close'].iloc[i]
        #         df.loc[i, 'sell_price'] = entry_price
        #         df.loc[i , 'sl_short'] = df['Close'].iloc[i] * (1+sl)
        #         df.loc[i, 'in_trade'] = True
        #     elif in_trade:
        #         df[i , 'in_trade'] = True
                
        #         if df["lips"].iloc[i] > df["teeth"].iloc[i]:
        #             df.loc[i, "exit_price"] = df["Close"].iloc[i]
        #             in_trade = False 
        #         else:
        #             df.loc[i, "exit_price"] = np.nan

        # return df

        # df["sell_price"] = np.where(df["short_signal"], df["Close"], np.nan)
        # df["stoploss_short"]= np.where(df["short_signal"],df["Close"] * (1+sl), np.nan)
        # # df["take_profit_short"]= np.where(df["short_signal"], tp, np.nan)
        # df["take_profit_short"]= np.where(df["short_signal"],df["Close"].shift(7) * (1-tp), np.nan)

    
    def backtest(self):
        """Simulate trades and compute performance metrics."""
        df = self.buy_sell_signal()
        balance = self.initial_capital
        lotsize = self.lot_size

        trades = []
        long_tp_trades = []
        long_sl_trades = []
        short_tp_trades = []
        short_sl_trades = []

        for i in range(len(df)):
            # --- LONG TRADE SIMULATION ---
            if df.iloc[i]['long_signal']:
                entry_price = df.iloc[i]['Close']
                exit_price_tp = df.iloc[i]['take_profit_long']  
                exit_price_sl = df.iloc[i]['stoploss_long']  

                tp = df.iloc[i]['take_profit_long']
                sl = df.iloc[i]['stoploss_long']
                print(f"Buy {self.lot_size} BTC at {entry_price} exit at TP:{exit_price_tp} exit at SL :{exit_price_sl} ")

                # simulate forward price movement
                for j in range(i + 1, len(df)):

                    # check TP hit first
                    if tp >= sl:
                        profit = (tp - entry_price) * lotsize
                        balance +=profit
                        trades.append(profit)
                        long_tp_trades.append(profit)  
                        print(f"✅ LONG TP hit! Buy at {entry_price:.2f}, exit {tp:.2f}, Profit: ${profit:.2f}, Balance: ${balance:.2f}")
                
                        break

                    # check SL hit
                    elif tp <= sl:
                        loss = (sl - entry_price) * lotsize
                        balance -=loss
                        trades.append(profit)
                        long_sl_trades.append(profit)
                        print(f"❌ LONG SL hit! Buy at {entry_price:.2f}, exit {sl:.2f}, Loss: ${loss:.2f}, Balance: ${balance:.2f}")
               
                        break

            # --- SHORT TRADE SIMULATION ---
            elif df.iloc[i]['short_signal']:
                entry_price = df.iloc[i]['Open']
                tp = df.iloc[i]['take_profit_short']
                sl = df.iloc[i]['stoploss_short']

                for j in range(i + 1, len(df)):
                    # check TP hit first (price falls)
                    if tp <= sl:
                        profit = (entry_price - tp) * lotsize
                        balance += profit
                        trades.append(profit)
                        short_tp_trades.append(profit) 
                        print(f"✅ SHORT TP hit! Sell at {entry_price:.2f}, exit {tp:.2f}, Profit: ${profit:.2f}, Balance: ${balance:.2f}")
                      
                        break

                    # check SL hit
                    elif tp >= sl:
                        loss = (entry_price - sl) * lotsize
                        balance -= loss
                        trades.append(profit)
                        short_sl_trades.append(profit)
                        print(f"❌ SHORT SL hit! Sell at {entry_price:.2f}, exit {sl:.2f}, Loss: ${loss:.2f}, Balance: ${balance:.2f}")
                      
                        break

        # --- Performance summary ---
        if len(trades) > 0:
            total_trades = len(trades)
            long_tp_trades = len(long_tp_trades )
            long_sl_trades = len(long_sl_trades)
            short_tp_trades = len(short_tp_trades)
            short_sl_trades = len(short_sl_trades)
            wins = len([p for p in trades if p > 0])
            losses = len([p for p in trades if p < 0])
            win_rate = (wins / total_trades) * 100
            total_profit = sum(trades)
            avg_profit = np.mean(trades)
            print("-----------------------------------")
            print(f"🏦 Starting Balance: ${self.initial_capital:,.2f}")
            print(f"💰 Ending Balance:   ${balance:,.2f}")
            print("-----------------------------------")
            print(f"📊 Total Trades: {total_trades}")
            print("-----------------------------------")
            print(f"📊 long_tp Trades: {long_tp_trades}")
            print(f"📊 short_tp Trades: {short_tp_trades}")
            print("-----------------------------------")
            print(f"📊 long_sl Trades: {long_sl_trades}")
            print(f"📊 short_sl Trades: {short_sl_trades}")
            print("-----------------------------------")
            print(f"✅ Wins: {wins} | ❌ Losses: {losses}")
            print(f"🏆 Win Rate: {win_rate:.2f}%")
            print(f"💰 Total Profit: {total_profit:.2f}")
            print(f"📈 Average P/L per trade: {avg_profit:.4f}")
        else:
            print("No trades triggered.")

        return df
    
ex = Execution()
df = ex.buy_sell_signal()
ex.buy(df)