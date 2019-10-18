from flask import Flask, render_template, request
import requests
import json
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import matplotlib.pyplot as plt


AV_key = '3CSH2Q79FWBCUE4M'
ts = TimeSeries(key=AV_key, output_format='pandas')
app = Flask(__name__)

@app.route('/')
def home():
    """Shows the Home Page"""
    return render_template("home.html")

@app.route('/stock')
def index():
    """Takes in input from the search bar and looks up Stock information
    using Alpha Vantage's API
    """
    search_term = request.args.get("search")
    try:
        data, meta_data = ts.get_intraday(symbol=search_term, interval='60min')
    except:
        return render_template("error_page.html")
    current_price = data['4. close'].iloc[0] #Current stock price
    stock_price = data['4. close'].values.tolist()
    stock_time = data.index.values
    return render_template("index.html", current_price=current_price, stock=search_term,
    stock_time=stock_time, stock_price=stock_price)

@app.route('/error_page')
def error():
    """Shows the Error Page"""
    return render_template("error_page.html")





# data['4. close'].plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
