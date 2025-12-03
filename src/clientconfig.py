import keyring
import binance

class ClientConfig:

    def __init__(self):
        self.api_key = keyring.get_password("binance", "api_key")
        self.api_secret = keyring.get_password("binance", "api_secret")
        
    def get_client(self):
        self.client = binance.Client(self.api_key, self.api_secret)
        return self.client

    def set_client(self, new_api_key, new_api_secret):
        self.api_key = new_api_key
        self.api_secret = new_api_secret
        self.client = binance.Client(self.new_api_key, self.new_api_secret)
        return self.client

