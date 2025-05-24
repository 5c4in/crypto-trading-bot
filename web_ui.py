from flask import Flask, request, render_template_string, flash, redirect
from bot import BasicBot
from config import API_KEY, API_SECRET

app = Flask(__name__)
bot = BasicBot(API_KEY, API_SECRET)

HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crypto Trading Bot</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background: #f9fbfd;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .card {
            border-radius: 1rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        }
        .form-control:focus {
            box-shadow: none;
            border-color: #6366f1;
        }
        .btn-primary {
            background-color: #6366f1;
            border: none;
        }
        .btn-primary:hover {
            background-color: #4f46e5;
        }
        .result-box {
            white-space: pre-wrap;
            background: #eef1f8;
            padding: 15px;
            border-radius: 0.5rem;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="card p-4">
                    <h3 class="text-center mb-4">Crypto Trading Bot</h3>
                    {% with messages = get_flashed_messages() %}
                        {% if messages %}
                        <div class="alert alert-warning">
                            {% for msg in messages %}{{ msg }}<br>{% endfor %}
                        </div>
                        {% endif %}
                    {% endwith %}
                    <form method="POST">
                        <div class="mb-3">
                            <label class="form-label">Symbol</label>
                            <input type="text" name="symbol" class="form-control" placeholder="BTCUSDT" required pattern="^[A-Z]{6,12}$">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Side</label>
                            <select name="side" class="form-select" required>
                                <option value="BUY">Buy</option>
                                <option value="SELL">Sell</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Order Type</label>
                            <select name="order_type" class="form-select" required>
                                <option value="MARKET">Market</option>
                                <option value="LIMIT">Limit</option>
                                <option value="STOP_MARKET">Stop Market</option>
                                <option value="STOP_LIMIT">Stop Limit</option>
                                <option value="TAKE_PROFIT_MARKET">Take Profit Market</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Quantity</label>
                            <input type="number" step="0.001" min="0.001" name="quantity" class="form-control" required>
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Price (Limit/Stop Limit only)</label>
                            <input type="number" step="0.01" name="price" class="form-control">
                        </div>
                        <div class="mb-3">
                            <label class="form-label">Stop Price (Stop/Take Profit types only)</label>
                            <input type="number" step="0.01" name="stop_price" class="form-control">
                        </div>
                        <button type="submit" class="btn btn-primary w-100">Place Order</button>
                    </form>
                    {% if result %}
                    <div class="result-box mt-4">
                        <strong>Result:</strong><br>
                        {{ result }}
                    </div>
                    {% endif %}
                </div>
            </div>
        </div>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            symbol = request.form['symbol'].strip().upper()
            side = request.form['side']
            order_type = request.form['order_type']
            quantity = float(request.form['quantity'])
            price = request.form.get('price')
            stop_price = request.form.get('stop_price')

            if not symbol.isalnum() or len(symbol) < 6:
                flash("Invalid symbol format.")
                return redirect('/')

            if quantity <= 0:
                flash("Quantity must be greater than 0.")
                return redirect('/')

            price = float(price) if price else None
            stop_price = float(stop_price) if stop_price else None

            if order_type in ['LIMIT', 'STOP_LIMIT'] and not price:
                flash("Price is required for LIMIT and STOP_LIMIT orders.")
                return redirect('/')

            if order_type in ['STOP_MARKET', 'STOP_LIMIT', 'TAKE_PROFIT_MARKET'] and not stop_price:
                flash("Stop price is required for STOP or TAKE_PROFIT_MARKET orders.")
                return redirect('/')

            result = bot.place_order(symbol, side, order_type, quantity, price, stop_price)
        except Exception as e:
            flash(f"Error: {e}")
            return redirect('/')

    return render_template_string(HTML, result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
