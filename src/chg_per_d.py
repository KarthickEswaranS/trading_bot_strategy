from src.dataloading import DataLoading


df = DataLoading()
hdf = df.get_historical_data("BTCUSDT", "1d", "21-9-2021", "21-9-2023")
pdf = df.data_processing(hdf).copy()

pdf["LH_AVG"] = (pdf["High"] + pdf["Low"])/2
pdf["LH_AVG_PCT_CHANGE"] = pdf["LH_AVG"].pct_change() * 100

# pdf["OC_AVG"] = (pdf["Open"] + pdf["Close"])/2
# pdf["OC_AVG_PCT_CHANGE"] = pdf["LH_AVG"].pct_change() * 100

print("LH_AVG_CHNG")
avg_change =  pdf["LH_AVG_PCT_CHANGE"].mean()
print(avg_change )

print("LH_AVG_CHNG")
max_change =  pdf["LH_AVG_PCT_CHANGE"].max()
print(max_change)

print("LH_AVG_CHNG")
min_change =  pdf["LH_AVG_PCT_CHANGE"].min()
print(min_change)

# ------- Result --------
# BTCUSDT
# -0.031	-0.03%	The LH average fell slightly (almost no change)
# 9.1778	+9.18%	The LH average increased by 9.18% compared to yesterday
# -12.2809	-12.28%	The LH average dropped by 12.28% compared to yesterday

# max Stoploss placement is
# 9.1 - 12.28 = -3.1 % based on the captial u  have