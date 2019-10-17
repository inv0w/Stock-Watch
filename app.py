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
        data, meta_data = ts.get_intraday(symbol=search_term, interval='5min')
    except:
        return render_template("home.html")
    current_price = data['4. close'].iloc[0] #Current stock price
    print(data)
    print(meta_data)
    return render_template("index.html", current_price=current_price, stock=search_term)


# data['4. close'].plot()
# plt.title('Intraday Times Series for the MSFT stock (1 min)')
# plt.show()
