from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    return "Stock Predictor API is running!"

@app.route('/stock/<ticker>', methods=['GET'])
def get_stock_price(ticker):
    try:
        # Yahoo Financeから株価情報を取得
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        # 株価データが空でない場合、最新の終値を取得
        if not data.empty:
            price = data["Close"].iloc[-1]
            return jsonify({"ticker": ticker, "price": price})
        else:
            return jsonify({"error": "No stock data available"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)