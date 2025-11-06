from src.clientconfig import ClientConfig
import binance
import pandas as pd
import mplfinance as mplf


class DataLoading(ClientConfig):

    def __init__(self):
        super().__init__()
        self.client = binance.Client(self.api_key, self.api_secret)

    def get_historical_data(self, symbol, user_interval, start_date, end_date):

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

        interval = interval_map.get(user_interval, self.client.KLINE_INTERVAL_1DAY)
        hist_data = self.client.get_historical_klines(
            symbol=symbol,
            interval=interval, 
            start_str=start_date, 
            end_str=end_date
            )
        self.data_processing(hist_data=hist_data)
        return hist_data
        
    def data_processing(self, hist_data):
        #Raw data to a organized data
        df_hist = pd.DataFrame(hist_data)
        df_hist.columns = ['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time',
                          'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume',
                          'Taker Buy Quote Asset Volume', 'Ignore']

        df_hist["Open Time"] = pd.to_datetime(df_hist["Open Time"],unit="ms")
        df_hist["Close Time"] = pd.to_datetime(df_hist["Close Time"],unit="ms")

        #converting string to numeric values
        numeric_data = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']
        df_hist[numeric_data] = df_hist[numeric_data].apply(pd.to_numeric, axis=1)

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

