import pandas as pd  
import math
import numpy
import secrets
from pandas.core.indexes import period
import yfinance as yf
from flask import Flask, session, jsonify, render_template

app = Flask(__name__)

@app.route("/validate-<searchRequest>", methods=['GET','POST'])
def validateTickerSearch(searchRequest):
    stock = yf.Ticker(str(searchRequest.upper()))
    ## Error handling
    try:
        stock.info['shortName']
    except (KeyError, ValueError, NameError):
        return jsonify(False)
    else:
        return jsonify(True)


def getDataForTicker(ticker):
    stock = yf.Ticker(ticker.upper())
    data = stock.history(period="5y")
    return {
        "close" : list(data["Close"]),
        "dates" : list(data.index)
    }

def getInfoForTicker(ticker):
    stock = yf.Ticker(ticker.upper())
    return stock.info
        

@app.errorhandler(404)
def page_not_found(error):
    return ("Page not found. Please return home.")


@app.route("/", methods=['GET','POST'])
def home():
    return render_template("index.html")

@app.route("/getData/<ticker>", methods=['GET','POST'])
def getData(ticker):
    ## Tickers will be an array
    session["closeData"] = {}

    session["closeData"] = getDataForTicker(ticker)

    return jsonify(session["closeData"])

@app.route("/getInfo/<ticker>", methods=['GET','POST'])
def getInfo(ticker):
    session["closeInfo"] = {}

    session["closeInfo"] = getInfoForTicker(ticker)

    return jsonify(session["closeInfo"])



if __name__ == "__main__":
    app.config['SECRET_KEY'] = secrets.token_urlsafe(16)
    app.run(
        debug=True,
    )