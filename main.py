from models import Developer
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

main = Blueprint('main', __name__)

OPEN_COVID19_URL = "http://newsapi.org/v2/everything?q={0}&language=en&sortBy=publishedAt&pageSize=5&apiKey={1}"
OPEN_COVID19_KEY = '0f123f4c5b4f45a6b33d7ca370bbaf05'

OPEN_NEWS_URL = "http://newsapi.org/v2/everything?q={0}&language=en&sortBy=publishedAt&pageSize=5&apiKey={1}"

@main.route("/")
def index():
    title = "Home"
    news = request.args.get('news')
    if not news:
        news = 'covid-19'

    covid19 = get_covid19(news, OPEN_COVID19_KEY)
    

    return render_template("index.html", title=title, covid19=covid19, news=news)


@main.route("/aboutus")
def about():
    title = "About us"
    #Query
    return render_template("aboutus.html", title=title, developer=Developer.query.all())


def serve_img(img_id):
    pass

def get_covid19(news,API_KEY):
    queryNews = quote(news)
    url = OPEN_COVID19_URL.format(queryNews, OPEN_COVID19_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)

    covid19 = parsed.get('articles')
    
    return covid19

def get_searchNews(news, API_KEY):
    queryNews = quote(news)
    url = OPEN_NEWS_URL.format(queryNews, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = parsed.get('articles')
    return news

