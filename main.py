#!/usr/bin/env python3
from lib.data import data, URL
import flask from Flask


app = Flask(__name__)

class placeholder:
    def __init__(self):
        pass

@app.route('/')
def index():
    return "Welcome to the Open Food Facts App!"

@app.route('/data')
def get_data():
    return data

if __name__ == '__main__':
    app.run(debug=True)