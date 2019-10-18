from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import json
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os


host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/stock-watch')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
portfolio = db.portfolio

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
def show_error():
    """Shows the Error Page"""
    return render_template("error_page.html")

@app.route('/portfolio')
def display_portfolio():
    """Shows the Portfolio Page"""
    return render_template("portfolio.html", portfolio=portfolio.find())

@app.route('/portfolio/new')
def stock_new():
    """Create a new Stock."""
    return render_template('stocks_new.html', stock={}, title='New Stock')

@app.route('/portfolio', methods=['POST'])
def portfolio_add_stock():
    """Adds stock to portfolio."""
    stock = {
        'name': request.form.get('name'),
        'amount': request.form.get('amount')
    }
    stock_id = portfolio.insert_one(stock).inserted_id
    return render_template('portfolio.html', portfolio=portfolio.find())

@app.route('/portfolio/<stock_id>/edit')
def stock_edit(stock_id):
    """Show the edit form for a stock."""
    stock = portfolio.find_one({'_id': ObjectId(stock_id)})
    return render_template('stocks_edit.html', stock=stock, title='Edit Stock')

@app.route('/portfolio/<stock_id>', methods=['POST'])
def stock_update(stock_id):
    """Submit an edited stock."""
    updated_stock = {
        'name': request.form.get('name'),
        'amount': request.form.get('amount')
    }
    portfolio.update_one(
        {'_id': ObjectId(stock_id)},
        {'$set': updated_stock})
    return redirect(url_for('display_portfolio', stock_id=stock_id))

@app.route('/portfolio/<stock_id>/delete', methods=['POST'])
def stock_delete(stock_id):
    """Deletes stock from portfolio."""
    portfolio.delete_one({'_id': ObjectId(stock_id)})
    return render_template('portfolio.html', portfolio=portfolio.find())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
