from flask import Flask, jsonify, request
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Predictor API is running!"

@app.route('/stock/<ticker>')
def get_stock_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")
        price = data["Close"].iloc[-1] if not data.empty else None
        return jsonify({"ticker": ticker, "price": price})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)