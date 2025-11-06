from src.clientconfig import ClientConfig
import asyncio
from binance import AsyncClient, BinanceSocketManager

async def order_book(client, symbol):
    order_book = await client.get_order_book(symbol=symbol)
    # print(order_book)

async def kline_listener(client):
    bm = BinanceSocketManager(client)
    symbol = 'BTCUSDT'
    res_count = 0

    loop = asyncio.get_running_loop()
    async with bm.kline_socket(symbol=symbol, interval=AsyncClient.KLINE_INTERVAL_1SECOND) as stream:
        while True:
            res = await stream.recv()
            res_count += 1
            print(res)
            if res_count == 5:
                res_count = 0
                loop.call_soon(asyncio.create_task, order_book(client, symbol))

async def main():
    api_client = ClientConfig()
    client = await AsyncClient.create(api_client.api_key, api_client.api_secret)
    try:
        await kline_listener(client)
    finally:
        await client.close_connection()

if __name__ == "__main__":
    asyncio.run(main())
 