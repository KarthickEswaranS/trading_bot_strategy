import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from src.dataloading import DataLoading

# ---- Load data ----
df = DataLoading()
hdf = df.get_historical_data("BTCUSDT", "1w", "21-9-2021", "21-9-2023")
pdf = df.data_processing(hdf)

# ---- Ensure datetime format ----
pdf['Open Time'] = pd.to_datetime(pdf['Open Time'])
pdf['Close Time'] = pd.to_datetime(pdf['Close Time'])

# ---- Create DataFrames ----
df_open = pdf.copy().set_index('Open Time')
df_close = pdf.copy().set_index('Close Time')

# ---- Create 2 side-by-side charts ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot candles using existing axes (no new figure)
mpf.plot(
    df_open,
    type='candle',
    style='yahoo',
    ax=axes[0],
    axtitle="Candles (Indexed by Open Time)",
    returnfig=False
)

mpf.plot(
    df_close,
    type='candle',
    style='yahoo',
    ax=axes[1],
    axtitle="Candles (Indexed by Close Time)",
    returnfig=False
)

plt.tight_layout()
plt.show()
