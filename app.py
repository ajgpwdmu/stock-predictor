from flask import Flask, jsonify, request
import os
import yfinance as yf

app = Flask(__name__)

@app.route("/")
def home():
    return "Stock Predictor API is running!"

@app.route("/predict", methods=["GET"])
def predict():
    symbol = request.args.get("symbol", "AAPL")  # デフォルトでAppleの株価
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")

    if hist.empty:
        return jsonify({"error": "Invalid stock symbol or no data available"}), 400

    latest_price = hist["Close"].iloc[-1]  # 最新の終値
    return jsonify({"symbol": symbol, "latest_price": latest_price})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # 環境変数からポートを取得
    app.run(host="0.0.0.0", port=port, debug=True)