#!/usr/bin/python3

from flask import Flask, request, render_template
from model import Model
import settings


app = Flask(__name__)
model = Model.from_pickles(settings.MODEL_FILE, settings.VECTORIZER_FILE)


@app.route('/', methods=['POST', 'GET'])
def index(text='', prediction_message=''):
    if request.method == "POST":
        text = request.form["text"]
        prediction_message = model.get_santa_answer(text)

    return render_template('index.html', text=text, prediction_message=prediction_message)


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=80)
