import argparse
from bot import BasicBot
from config import API_KEY, API_SECRET

bot = BasicBot(API_KEY, API_SECRET)

parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")
parser.add_argument("--symbol", required=True, help="Trading pair (example BTCUSDT)")
parser.add_argument("--side", required=True, choices=["BUY", "SELL"])
parser.add_argument("--order_type", required=True, choices=["MARKET", "LIMIT", "STOP_MARKET", "STOP_LIMIT"])
parser.add_argument("--quantity", required=True, type=float)
parser.add_argument("--price", type=float, help="Required for LIMIT && STOP_LIMIT")
parser.add_argument("--stop_price", type=float, help="Required for STOP_MARKET && STOP_LIMIT")

args = parser.parse_args()

if args.order_type in ["LIMIT", "STOP_LIMIT"] and args.price is None:
    parser.error("Price is required for LIMIT and STOP_LIMIT orders.")
if args.order_type in ["STOP_MARKET", "STOP_LIMIT"] and args.stop_price is None:
    parser.error("Stop price is required for STOP_MARKET and STOP_LIMIT orders.")

result = bot.place_order(
    symbol=args.symbol.upper(),
    side=args.side,
    order_type=args.order_type,
    quantity=args.quantity,
    price=args.price,
    stop_price=args.stop_price
)

print("Order Result:")
print(result)