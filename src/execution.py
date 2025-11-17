from src.strategy import Strategy   
import numpy as np

class Execution(Strategy):

    def __init__(self):
        super().__init__()
        self.initial_balance = 100000
        self.lot_size = 1
        self.balance = 0
        self.profit = 0
        self.loss = 0
        self.profit_trades = []
        self.loss_trades = []

    
    def long_signal(self):

        df = self.stg_smma()

        df['enter_long'] = (
            # (df['lips'].shift(1) < df['teeth'].shift(1)) &
            ((df['Close'].shift(1) > df['lips'].shift(1)) & (df['Close'].shift(1) >= df['teeth'].shift(1))) &
            ((df['lips'].shift(1)  > df['teeth'].shift(1)) & (df['lips'].shift(1)  > df['jaw'].shift(1)))
        )

        df['exit_long'] = (
            ((df['Close'] < df['lips']) & (df['Close'] < df['teeth']))
        )
     
        self.buy_sell_price(df)
        return df
       
   
    def buy_sell_price(self, dataframe):
        df = dataframe
        df['buy_price'] = np.nan
        df['sell_price'] = np.nan
        df['position'] = 0
        df['tp_long'] = np.nan
        df['sl_long'] = np.nan

        position = 0
        entry_price = None
        tp = None
        sl = None

        for i in range(len(df)):

            if position == 0:
                if df.iloc[i]['enter_long'] == True:
                   
                    entry_price = df.iloc[i]['Open']
                    tp =  entry_price * (1 + 0.1)  # 2% Take Profit
                    sl =  entry_price *  (1 - 0.05)  # 1% Stop Loss
            
                    df.at[df.index[i], 'buy_price'] = entry_price
                    df.at[df.index[i], 'position'] = 1
                    df.at[df.index[i], 'tp_long'] = tp
                    df.at[df.index[i], 'sl_long'] = sl  

                    position = 1
                    continue


            elif position == 1 and df.iloc[i]['exit_long'] == True:
                exit_price = df.iloc[i]['Close']
                df.at[df.index[i], 'sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0

                if exit_price <= sl:
                    self.loss = self.balance - (entry_price - sl) * self.lot_size
                    self.loss_trades.append(self.loss)
                    self.balance  = self.loss
                    print(f"""--------------  LOSS EXIT CONDITONS --------------
                    Stop Loss hit: {sl:.2f}
                    Entry Price: {entry_price}
                    Loss: {self.loss:.2f}
                    Balance: {self.balance:.2f}
                    """)
                    continue
                    

                elif exit_price >= tp:
                    self.profit = self.balance + (tp + entry_price) * self.lot_size
                    self.profit_trades.append(self.profit)
                    self.balance  = self.profit
                    print(f"""--------------  PROFIT EXIT CONDITONS --------------
                    Stop Loss hit: {tp:.2f}
                    Entry Price: {entry_price}
                    Loss: {self.profit:.2f}
                    Balance: {self.balance:.2f}
                    """)     
                    continue      

            elif position == 1 and df.iloc[i]['Close'] >= tp:
                df.at[df.index[i], 'sell_price'] = tp
                df.at[df.index[i], 'position'] = 0
                position = 0
                self.profit = self.balance + (tp + entry_price) * self.lot_size
                self.profit_trades.append(self.profit)
                self.balance  = self.profit
            
                print(f"""-------------- TP HIT --------------
                Stop Loss hit: {tp:.2f}
                Entry Price: {entry_price}
                Profit: {self.profit:2f}
                Balance: {self.balance:.2f}
                """)           
                continue

            elif position == 1 and df.iloc[i]['Close'] <= sl:
                df.at[df.index[i], 'sell_price'] = sl
                df.at[df.index[i], 'position'] = 0
                position = 0
                self.loss = self.balance - (entry_price - sl) * self.lot_size
                self.loss_trades.append(self.loss)
                self.balance  = self.loss

                print(f"""-------------- SL HIT --------------
                Stop Loss hit: {sl:.2f}
                Entry Price: {entry_price}
                Loss: {self.loss:.2f}
                Balance: {self.balance:.2f}
                """)
                continue
        
            continue

        self.results()
 
        return df
    
    def results(self):
        print("================ FINAL RESULTS ================")
        total_profit = sum(self.profit_trades)
        print(f"Total Profit: + {total_profit:.2f}")

        total_loss = sum(self.loss_trades)
        print(f"Total Loss: - {total_loss:.2f}")

        pl = total_profit - total_loss
        print(f"Profit - Loss: {pl:.2f}")

        print(f"Balance: {self.initial_balance  + pl:.2f}")

        total_no_of_trades = self.profit_trades.__len__() +  self.loss_trades.__len__()
        win = (self.profit_trades.__len__()  / total_no_of_trades) * 100
        print(f"Win Rate %: {win:.2f}%")

      
        
        print("-------------------------------------------------")
        print(f"Total No Of Profit Trades: {self.profit_trades.__len__()}")
        print(f"Total No Of Loss Trades: {self.loss_trades.__len__()}")
        print("-------------------------------------------------")
        for i in range(len(self.profit_trades)):
            print(f" + {self.profit_trades[i]:.2f}")
        print("-------------------------------------------------")
        for i in range(len(self.loss_trades)):
            print(f" - {self.loss_trades[i]:.2f}")
       

ex = Execution()
ex.long_signal()
