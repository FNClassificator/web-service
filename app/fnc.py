from flask import Flask, render_template, request
from flask_cors import CORS

from app.controller.classify import classify_article


app = Flask(__name__, template_folder='templates/')
CORS(app)


@app.route('/')
def render_static():
    return render_template('tag.html')


@app.route('/classify')
def search():
    # Get params
    url = request.args.get('url')
    page = request.args.get('page')

    # Sort places
    response = classify_article(url, page)
    return render_template('result.html', params=response)