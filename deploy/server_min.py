#!/usr/bin/python3

from flask import Flask, jsonify
from flask import Response
from flask import request

from parser import update_weights, get_articles, parse_article

app = Flask(__name__)

@app.route('/say_hello')
def say_hello():
    return 'Say hello'

@app.route('/parse_article/j/', methods = ['POST'])
def get_parsed_article():
    data = request.get_json(force=True)
    text = data['article_text']
    title = data['article_title']
    parsed_article = parse_article(text, title)

    return jsonify(parsed_article)

if __name__ == '__main__':
    app.run()