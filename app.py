import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# 環境変数を読み込む
load_dotenv()

app = Flask(__name__)

# Alpha Vantage APIキーを環境変数から取得
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

@app.route("/")
def home():
    return "Hello, this is a stock prediction app!"

@app.route("/stock", methods=["GET"])
def get_stock_data():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Symbol is required"}), 400

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if "Time Series (5min)" not in data:
        return jsonify({"error": "Invalid response from API"}), 500

    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)