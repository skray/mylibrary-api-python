from flask import Flask, request
from flask import jsonify
import requests
import xmltodict
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"message": 'Hello, World!'})

@app.route('/books')
def search_books():
    search_string = request.args.get('q')
    if search_string is None:
        search_string = ''

    search_response = requests.get('https://www.goodreads.com/search/index.xml', {'key': os.environ.get('GOODREADS_API_KEY'), 'q': search_string})

    search_results = xmltodict.parse(search_response.text, xml_attribs=False)['GoodreadsResponse']['search']['results']
    if search_results is not None:
        response = jsonify(search_results['work'])
    else:
        response = jsonify([])

    response.headers["Content-Type"] = "application/json"
    return response
