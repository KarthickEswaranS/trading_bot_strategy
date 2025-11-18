from src.strategy import Strategy   
import numpy as np

class Execution(Strategy):

    def __init__(self):
        super().__init__()
        self.initial_balance = 100000
        self.lot_size = 1
        self.balance =  self.initial_balance
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
            close = df.iloc[i]['Close']
            
            #Entry
            if position == 0 and df.iloc[i]['enter_long']:    
                entry_price = df.iloc[i]['Open']
                tp =  entry_price *(1 + 0.08)
                sl =  entry_price * (1 - 0.01)
        
                df.at[df.index[i], 'buy_price'] = entry_price
                df.at[df.index[i], 'position'] = 1
                df.at[df.index[i], 'tp_long'] = tp
                df.at[df.index[i], 'sl_long'] = sl  

                position = 1
                continue
            
            if position == 1 and close >= tp:
                exit_price = tp
                df.at[df.index[i], 'sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0
                
                pnl = (exit_price - entry_price) * self.lot_size
                self.profit_trades.append(pnl)
                self.balance += pnl
               
                print(f"""-------------- TP HIT --------------
                    Entry Price: {entry_price}
                    Exit Price: {exit_price:.2f}
                    pnl: {pnl:.2f}
                    Balance: {self.balance:.2f}
                    """)
                continue

            #Stop Loss Hit
            if position == 1 and close <= sl:

                exit_price = sl
                df.at[df.index[i], 'sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0

                pnl = (exit_price - entry_price) * self.lot_size
                self.loss_trades.append(abs(pnl))
                self.balance += pnl
             
                print(f"""-------------- SL HIT --------------
                    Entry Price: {entry_price}
                    Exit Price: {exit_price:.2f}
                    pnl: {pnl:.2f}
                    Balance: {self.balance:.2f}
                    """)
                continue

        self.results()
 
        return df
    
    def results(self):
        print("================ FINAL RESULTS ================")
        total_profit = sum(self.profit_trades)
        print(f"Total Profit: + {total_profit:.2f}")

        total_loss = sum(self.loss_trades)
        print(f"Total Loss: - {total_loss:.2f}")

        npl =   total_profit - total_loss 
        print(f"Profit - Loss: {npl:.2f}")
        print(f"Balance: {self.initial_balance  + npl:.2f}")

        total_no_of_trades = self.profit_trades.__len__() +  self.loss_trades.__len__()
        win = (self.profit_trades.__len__()  / total_no_of_trades) * 100
        print(f"Win Rate %: {win:.2f}%")

        print("-------------------------------------------------")
        print(f"Total No Of Profit Trades: {self.profit_trades.__len__()}")
        print(f"Total No Of Loss Trades: {self.loss_trades.__len__()}")
        print("-------------------------------------------------")
        for p in range(len(self.profit_trades)):
            print(f" + {self.profit_trades[p]:.2f}")
        print("-------------------------------------------------")
        for l in range(len(self.loss_trades)):
            print(f" - {self.loss_trades[l]:.2f}")
       

# ex = Execution()
# ex.long_signal()
