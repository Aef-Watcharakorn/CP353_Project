from models import Developer
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json
import os

main = Blueprint('main', __name__)

FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY','demo')
OPEN_FINNHUB_NEWS_URL = "https://finnhub.io/api/v1/news?category={0}&token={1}"
API_KEY = 'c0sit9n48v6tv6b8fm70'


@main.route("/")
def index():
    title = "Home"
    news = request.args.get('news')
    if not news:
        news = 'general'
    general = get_news(news, FINNHUB_API_KEY)
    return render_template("index.html", title=title, general=general)


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


