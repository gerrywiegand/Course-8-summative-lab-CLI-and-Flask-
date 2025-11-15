#!/usr/bin/env python3
from flask import Flask

from lib.data import data

app = Flask(__name__)


class Inventory:
    def __init__(self):
        pass


@app.route("/")
def index():
    return "Welcome to the Open Food Facts App!"


@app.route("/data", methods=["GET"])
def get_data():
    return data, 200


@app.route("/data/<int:item_id>", methods=["GET"])
def get_item(item_id):
    for item in data:
        if item.get("id") == item_id:
            return item, 200
    return {"error": "Item not found"}, 404


if __name__ == "__main__":
    app.run(debug=True)
