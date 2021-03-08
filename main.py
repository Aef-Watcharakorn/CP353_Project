import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import flask
from models import Developer
from flask import Blueprint, render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen


main = Blueprint('main', __name__)

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
OPEN_FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/news?category={0}&token={1}"
OPEN_FINNHUB_RATE_URL = "https://finnhub.io/api/v1/forex/rates?base={0}&token={1}"
API_KEY = 'c0sit9n48v6tv6b8fm70'


@main.route("/")
def index():
    title = "Home"
    base = request.args.get('base')
    if not base:
        base = 'EUR'
    rate = get_rate(base, API_KEY)
    return render_template("index.html", title=title, rate=rate)

@main.route("/news")
def news():
    title = "News"
    news = request.args.get('news')
    if not news:
        news = 'general'
    general = get_news(news, API_KEY)
    return render_template("news.html", title=title, general=general, API=API_KEY)

@main.route("/stock")
def stock():
    title = "Stock"
    ticker = 'AAPL'
    urlCandles = f'https://finnhub.io/api/v1/stock/candle?symbol={ticker}&resolution=1&from=1605543327&to=1605629727&token={API_KEY}'
    data = request.get(urlCandles).json()
    df = pd.json_normalize(data)

    fig = go.Figure([
        go.Scatter(

        )
    ])
    return render_template("stock.html", title=title)

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
