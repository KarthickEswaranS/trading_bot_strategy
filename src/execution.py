from src.strategy import Strategy   
import numpy as np

class Execution(Strategy):

    def __init__(self):
        super().__init__()
        self.initial_balance = 100000
        self.balance =  self.initial_balance
        self.lot_size = 1
        self.risk = 0.03
        self.reward = 0.06
        
        self.long_profit_trades = []
        self.long_loss_trades = []
        self.short_profit_trades = []
        self.short_loss_trades = []
  
    def signal(self):

        df = self.stg_smma()

        df['enter_long'] = (
            (df['Close'].shift(1) > df['teeth'].shift(1)) &
            (df['Close'].shift(1) > df['lip'].shift(1)) &
            (df['Close'].shift(1) > df['jaw'].shift(1)) 
           
        )

        df['enter_short'] = (
            (df['Close'].shift(1) < df['teeth'].shift(1)) &
            (df['Close'].shift(1) < df['lip'].shift(1)) &
            (df['Close'].shift(1) < df['jaw'].shift(1)) 
            
        )

        df['exit_long'] = (
            ((df['Close'] < df['lip']) & (df['Close'] < df['teeth'])) 
           
        )
        
        df['exit_short'] = (
            ((df['Close'] > df['lip']) & (df['Close'] > df['teeth'])) 
           
        )

     
        return df
       
   
    def buy_sell_price(self):
        df = self.signal()
        cols = ['long_buy_price','long_sell_price','short_buy_price','short_sell_price',
        'long_sl', 'long_tp','short_tp','short_sl','position']

        for col in cols:
            df[col] = np.nan
            df['position'] = 0
        
        position = 0
        entry_price = None
        exit_price = None
        long_tp = None
        long_sl = None
        short_tp = None
        short_sl = None
        pnl = None

        for i in range(len(df)):
            close = df.iloc[i]['Close']
            enter_long = df.iloc[i]['enter_long']
            enter_short = df.iloc[i]['enter_short']
            
            #Entry
            if position == 0 and enter_long :    
                entry_price = close
             
                long_sl =  round(entry_price * (1 - self.risk), 2)
                long_tp =  round(entry_price *(1 + self.reward), 2)

                # long_tp =  entry_price *(1 + 0.08)
                # long_sl =  entry_price * (1 - 0.01)
        
                df.at[df.index[i], 'long_buy_price'] = entry_price
                df.at[df.index[i], 'position'] = 1
                df.at[df.index[i], 'long_tp'] = long_tp
                df.at[df.index[i], 'long_sl'] = long_sl  
                position = 1

                continue
            elif position == 0 and enter_short:
                entry_price = close

                short_sl =  round(entry_price * (1 + self.risk), 2)
                short_tp =  round(entry_price *(1 - self.reward), 2)
        
                df.at[df.index[i], 'short_buy_price'] = entry_price
                df.at[df.index[i], 'position'] = -1
                df.at[df.index[i], 'short_tp'] = short_tp
                df.at[df.index[i], 'short_sl'] = short_sl
                position = -1

                continue
            
            # long Target / sl  Hit
            if position == 1 and close <= long_sl:
                exit_price = long_sl
                df.at[df.index[i], 'long_sl'] = exit_price
                df.at[df.index[i], 'long_sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0

                pnl = (exit_price - entry_price) * self.lot_size
                self.long_loss_trades.append(abs(pnl))
                self.balance += pnl
                continue
            elif position == 1 and close >= long_tp:
                exit_price = long_tp
                df.at[df.index[i], 'long_tp'] = exit_price
                df.at[df.index[i], 'long_sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0
                
                pnl = (exit_price - entry_price) * self.lot_size
                self.long_profit_trades.append(pnl)
                self.balance += pnl
               
                continue
            

            # short Target / sl  Hit 
            if position == -1 and close >= short_sl:
                exit_price = short_sl
                df.at[df.index[i], 'short_sl'] = exit_price
                df.at[df.index[i], 'short_sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0

                pnl = (exit_price - entry_price) * self.lot_size
                self.short_loss_trades.append(abs(pnl))
                self.balance += pnl
                continue
            elif position == -1 and close <= short_tp:
                exit_price = short_tp
                df.at[df.index[i], 'short_tp'] = exit_price
                df.at[df.index[i], 'short_sell_price'] = exit_price
                df.at[df.index[i], 'position'] = 0
                position = 0
                
                pnl = (exit_price - entry_price) * self.lot_size
                self.short_profit_trades.append(pnl)
                self.balance += pnl
                continue

        # print(df)
        self.results()
        
        return df
    
    def results(self):
        print("================ FINAL RESULTS ================")
        print(f"Balance: {round(self.balance, 2)}")

        total_profit = round(sum(self.long_profit_trades) + sum(self.short_profit_trades), 2)
        print(f"Total Profit: + {total_profit}")

        total_loss = round(sum(self.long_loss_trades)  + sum(self.short_loss_trades), 2)
        print(f"Total Loss: - {round(total_loss,2)}")

        npl =   round(total_profit - total_loss , 2)
        print(f"Net Profit/Loss: {npl}")

        trades = [len(self.long_profit_trades), len(self.long_loss_trades), len(self.short_profit_trades), len(self.short_loss_trades)]
        total_no_of_trades = sum(trades)

        profit_trades = [len(self.long_profit_trades), len(self.short_profit_trades)]
        win = ( sum(profit_trades) / total_no_of_trades) * 100
        print(f"Win Rate %: {win:.2f}%")

        print("-------------------------------------------------")
        print(f"Total No Of Long Profit Trades: {len(self.long_profit_trades)}")
        print(f"Total No Of Long Loss Trades: {len(self.long_loss_trades)}")
        print(f"Total No Of Short Profit Trades: {len(self.short_profit_trades)}")
        print(f"Total No Of Short Loss Trades: {len(self.short_loss_trades)}")
       
Execution()