import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import flask
from models import Developer
from flask import Blueprint, render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import requests
from datetime import datetime
import time


main = Blueprint('main', __name__)

FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
OPEN_FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/news?category={0}&token={1}"
OPEN_FINNHUB_RATE_URL = "https://finnhub.io/api/v1/forex/rates?base={0}&token={1}"
OPEN_FINNHUB_PROFILE_URL = "https://finnhub.io/api/v1/stock/profile2?symbol={0}&token={1}"
OPEN_FINNHUB_SYMBOL_URL = "https://finnhub.io/api/v1/search?q={0}&token={1}"
#API_SHOW = 'c0sit9n48v6tv6b8fm70'

@main.route("/")
def index():
    title = "Home"
    base = request.args.get('base')
    if not base:
        base = 'THB'
    rate = get_rate(base, FINNHUB_API_KEY)
    return render_template("index.html", title=title, rate=rate)

@main.route("/news")
def news():
    title = "News"
    
    news = request.args.get('news')
    if not news:
        news = 'general'
    general = get_news(news, FINNHUB_API_KEY)
    return render_template("news.html", title=title, general=general, API=FINNHUB_API_KEY, news=news)

@main.route("/stock",methods=["GET","POST"])
def stock():
    title = "Stock"

    #API SYMBOL
    comp= request.form.get("company")
    if not comp:
        comp = 'AAPL'
    company = get_profile(comp, FINNHUB_API_KEY)
    
    df = pd.read_csv('https://finnhub.io/api/v1/stock/candle?symbol={0}&resolution=W&count=500&token={1}&format=csv'.format(comp,FINNHUB_API_KEY))
    w = list()
    for i in range(len(df)):
        x = int(df['t'][i])
        local_time = time.gmtime(x)
        w.append(time.strftime("%Y-%m-%d %H:%M:%S", local_time)) 
    fig = go.Figure(data=[go.Candlestick(x=w,
    open=df['o'],
    high=df['h'],
    low=df['l'],
    close=df['c'])])


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template("stock.html", title=title, plot=graphJSON, company=company)

@main.route("/profile")
def profile():
    title = "Profile Company"
    comp = request.args.get('company')
    if not comp:
        comp = 'AAPL'
    company = get_profile(comp, FINNHUB_API_KEY)
    symbol = get_symbol(comp, FINNHUB_API_KEY)
    return render_template("profile.html", title=title, comp=comp, company=company, symbol=symbol)


@main.route("/aboutus")
def about():
    title = "About us"
    #Query
    return render_template("aboutus.html", title=title, developer=Developer.query.all())


def serve_img(img_id):
    pass

def get_news(news, API_KEY):
    query = quote(news)
    url = OPEN_FINNHUB_NEWS_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    News = parsed
    return News

def get_rate(rate, API_KEY):
    query = quote(rate)
    url = OPEN_FINNHUB_RATE_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    alldata = parsed
    base = parsed['base']
    value = parsed['quote']
    ret = {'base': base,
            'value': value,
            'alldata':alldata
            }
    return ret

def profile():
    if request.method == 'GET':
        title = "Profile Company"
        comp = request.args.get('word')
        if not comp:
            comp = 'TSLA'
        symbol = get_symbol(comp, FINNHUB_API_KEY)
        company = get_profile(comp, FINNHUB_API_KEY)
        return render_template("profile.html", title=title, comp=comp, company=company, symbol=symbol)

def get_profile(company, API_KEY):
    query = quote(company)
    urlProfile = OPEN_FINNHUB_PROFILE_URL.format(query, API_KEY)

    dataProfile = urlopen(urlProfile).read()
    parsedProfile = json.loads(dataProfile)
    return parsedProfile

def get_symbol(symbol, API_KEY):
    query = quote(symbol)
    urlSymbol = OPEN_FINNHUB_SYMBOL_URL.format(query, API_KEY)
    dataSymbol = urlopen(urlSymbol).read()
    parsedSymbol = json.loads(dataSymbol)

    #SYMBOL DATA
    symbol = []
    count = parsedSymbol['count']
    for i in range(count):
        symbol = parsedSymbol['result'][i]

    ret = symbol

    return ret