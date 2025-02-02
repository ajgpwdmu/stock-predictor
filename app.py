from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "株価予測アプリのテストページ"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
		
		import yfinance as yf
from flask import request, jsonify

@app.route("/stock", methods=["GET"])
def get_stock_price():
    symbol = request.args.get("symbol")  # 例: ?symbol=7203.T（トヨタ自動車）

    if not symbol:
        return jsonify({"error": "symbolパラメータを指定してください"}), 400

    try:
        stock = yf.Ticker(symbol)
        data = stock.history(period="1d")  # 最新1日のデータ
        if data.empty:
            return jsonify({"error": "データが取得できません"}), 400

        latest_price = data["Close"].iloc[-1]  # 終値を取得

        return jsonify({
            "symbol": symbol,
            "latest_price": latest_price
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500