from src.strategy import Strategy   
import numpy as np

class Execution(Strategy):

    def __init__(self):
        super().__init__()
        self.initial_balance = 100000
        self.lot_size = 1
    
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

            elif position == 1 and df.iloc[i]['Close'] >= tp:
                df.at[df.index[i], 'sell_price'] = tp
                df.at[df.index[i], 'position'] = 0
                position = 0   
                continue

            elif position == 1 and df.iloc[i]['Close'] <= sl:
                df.at[df.index[i], 'sell_price'] = sl
                df.at[df.index[i], 'position'] = 0
                position = 0   
                continue
                

            elif position == 1 and df.iloc[i]['exit_long'] == True:
                df.at[df.index[i], 'sell_price'] = df.iloc[i]['Close']
                df.at[df.index[i], 'position'] = 0
                position = 0
                entry_price = None
                continue

        
        print(df[df['enter_long']])

ex = Execution()
ex.buy_sell_price(ex.long_signal())