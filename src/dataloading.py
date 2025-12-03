from src.clientconfig import ClientConfig
import binance
import pandas as pd



class DataLoading(ClientConfig):

    def __init__(self):
        super().__init__()
        self.client = self.get_client()
        self.asset = "BTCUSDT"
        self.start_date = "1-1-2023"
        self.end_date = "31-12-2024"
        self.intervals = ["4hr","8hr","1d", "1w", "1m"]

    def get_historical_data(self):
        all_data = {} 
        interval_map = {
            "1min"  : self.client.KLINE_INTERVAL_1MINUTE,
            "3min"  : self.client.KLINE_INTERVAL_3MINUTE,
            "5min"  : self.client.KLINE_INTERVAL_5MINUTE,
            "15min"  : self.client.KLINE_INTERVAL_15MINUTE,
            "30min"  : self.client.KLINE_INTERVAL_30MINUTE,
            "1hr"  : self.client.KLINE_INTERVAL_1HOUR,
            "4hr"  : self.client.KLINE_INTERVAL_4HOUR,
            "8hr"  : self.client.KLINE_INTERVAL_8HOUR,
            "12hr"  : self.client.KLINE_INTERVAL_12HOUR,
            "1d"  : self.client.KLINE_INTERVAL_1DAY,
            "1w"  : self.client.KLINE_INTERVAL_1WEEK,
            "1m"  : self.client.KLINE_INTERVAL_1MONTH,
        }

        for interval in self.intervals:
            interval_value = interval_map.get(interval)
            hist_data = self.client.get_historical_klines(
                    symbol=self.asset,
                    interval=interval_value, 
                    start_str=self.start_date, 
                    end_str=self.end_date
            )
            
            all_data[interval] = hist_data

        return all_data
        
    def data_processing(self, interval):

        all_hist_data = self.get_historical_data()

        df_hist = pd.DataFrame(all_hist_data[interval])
        df_hist.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                          'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                          'Taker Buy Quote Asset Volume', 'Ignore']

        df_hist["Open Time"] = pd.to_datetime(df_hist["Open Time"],unit="ms")
        df_hist["Close Time"] = pd.to_datetime(df_hist["Close Time"],unit="ms")

        #converting string to numeric values
        numeric_data = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
        df_hist[numeric_data] = df_hist[numeric_data].apply(pd.to_numeric, axis=1)

        # print(df_hist)
        return df_hist
  
    def verify_credentials(self):
        try:
            self.client.ping()
            print("Credentials are valid. Account information retrieved successfully.")
            return True
        except binance.ClientError as e:
            print(f"Invalid credentials or error occurred: {e}")
            return False
        except binance.ServerError as e:
            print("⚠️ Binance Server Error.")
            print(f"Message: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error:{e}")

