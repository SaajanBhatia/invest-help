import pandas as pd  
import math
import numpy
from pandas.core.indexes import period
import yfinance as yf
from flask import Flask, session, jsonify

app = Flask(__name__)



class dataClass(object):
    def __init__(self,session):
        self.__session = session

    def validateTickerSearch(self, searchRequest):
        found = False
        stock = yf.Ticker(str(searchRequest))
        ## Error handling
        try:
            stock.info['shortName']
        except (KeyError, ValueError, NameError) as error:
            found = False
        else:
            found = True
        finally:
            return found 

    def getDataForTicker(self,ticker):
        stock = yf.Ticker(ticker.upper())
        data = stock.history(period="max")
        return data
        

@app.errorhandler(404)
def page_not_found(error):
    return ("Page not found. Please return home.")


@app.route("/")
def home():
    return '''
        <h1 style="color:red; padding: 12px">HOME</h1>
    '''

@app.route("/getData/<ticker>")
def getData(ticker):
    ## Tickers will be an array
    currentUser = dataClass(session)
    token = {
        "data" : {},
        "errors" : {}
    }

    print (ticker)
    if currentUser.validateTickerSearch(ticker):
        token["errors"][ticker] = "Ticker Search does not exist."
    else:
        token["data"][ticker] = currentUser.getDataForTicker(ticker)
    return jsonify(token)


if __name__ == "__main__":
    app.run(
        debug=True
    )