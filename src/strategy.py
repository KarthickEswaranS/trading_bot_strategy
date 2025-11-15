from src.dataloading import DataLoading
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import mplfinance as mplf
import ta
class Strategy(DataLoading):

    def __init__(self):
        super().__init__()
        self.interval_data = "1d"
        self.p_hist_data = self.data_processing(self.interval_data)
        #indcators
        # self.p_hist_data["rsi"] = ta.momentum.RSIIndicator(self.p_hist_data['Close'] , 14).rsi()

    def smma_logic(self, series, length):
        smma_values = []
        # go through every number one by one
        for i in range(len(series)):
            if i < length:
                smma_values.append(np.nan)
            elif i==length:
                smma_values.append(series.iloc[:length].mean())
            else:
                smma_values.append((smma_values[-1]* (length-1)+ series.iloc[i])/length)
        return pd.Series(smma_values, index=series.index)
    
    def stg_smma(self):
        df = self.p_hist_data
        
        df.set_index('Open Time', inplace=True)
        df['hl2'] = (df['High'] + df['Low'])/2

        # Calculate SMMA lines
        df["jaw"] = self.smma_logic(df["hl2"], 21)
        df["teeth"] = self.smma_logic(df["hl2"], 11)
        df["lips"] = self.smma_logic(df["hl2"], 7)

        return df
