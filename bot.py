import logging
from binance.client import Client
from binance.enums import *

logging.basicConfig(filename='bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class BasicBot:
    def __init__(self, api_key, api_secret, testnet=True):
        self.client = Client(api_key, api_secret)
        if testnet:
            self.client.FUTURES_URL = 'https://testnet.binancefuture.com/fapi'
        logging.info("Bot initialized with testnet: %s", testnet)

    def place_order(self, symbol, side, order_type, quantity, price=None, stop_price=None):
        try:
            params = {
                'symbol': symbol.upper(),
                'side': side.upper(),
                'type': order_type.upper(),
                'quantity': quantity
            }

            if order_type.upper() == 'LIMIT':
                params['price'] = price
                params['timeInForce'] = TIME_IN_FORCE_GTC
            elif order_type.upper() == 'STOP_MARKET':
                params['stopPrice'] = stop_price
            elif order_type.upper() == 'STOP_LIMIT':
                params['price'] = price
                params['stopPrice'] = stop_price
                params['timeInForce'] = TIME_IN_FORCE_GTC

            order = self.client.futures_create_order(**params)
            logging.info("Order placed: %s", order)
            return order
        except Exception as e:
            logging.error("Order failed: %s", str(e))
            return {"error": str(e)}
