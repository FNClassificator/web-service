from flask import Flask, render_template, request
from flask_cors import CORS

from app.controller.classify import classify_article
from app.classificator.run import create_classifier
import json

app = Flask(__name__, template_folder='templates/')
CORS(app)



# Implement LDA MODEL
models = create_classifier()


@app.route('/')
def render_static():
    return render_template('tag.html')


@app.route('/predict')
def search():
    # Get params
    url = request.headers.get('url')
    page = request.headers.get('page')
    print('Request about:', page, url)

    # Sort places
    prediction = classify_article(url, page, models)
    if prediction == 0:
        res = 'Real news'
    else:
        res = 'Fake news'
    response = app.response_class(
        response=json.dumps({'result': res}),
        status=200,
        mimetype='application/json'
    )
    return response