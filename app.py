from flask import Flask, jsonify, request
import yfinance as yf
import numpy as np
import pandas as pd

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
        return jsonify({"error": str(e)}), 500

@app.route('/predict/<ticker>', methods=['GET'])
def predict_stock_price(ticker):
    try:
        # 株価データを取得（過去10日分）
        stock = yf.Ticker(ticker)
        data = stock.history(period="10d")

        if data.empty:
            return jsonify({"error": "No data found"}), 404

        # 終値データを取得
        close_prices = data["Close"].values

        # シンプルな移動平均予測（直近5日間の平均を次の日の予測値とする）
        if len(close_prices) < 5:
            return jsonify({"error": "Not enough data for prediction"}), 400

        predicted_price = np.mean(close_prices[-5:])  # 直近5日間の平均値を予測値とする

        return jsonify({"ticker": ticker, "predicted_price": predicted_price})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)