#!/usr/bin/env python3
from flask import Flask  # noqa: I001
from flask import request
from inventory.services import InventoryManager  # noqa: F401
from inventory.models import Item  # noqa: F401


app = Flask(__name__)


Inventory = InventoryManager()


@app.route("/")
def index():
    return "Welcome to the Open Food Facts App!"


@app.route("/data", methods=["GET"])
def get_data():
    items = Inventory.list_items()
    items_dict = [item.to_dict() for item in items]
    return {"data": items_dict}, 200


@app.route("/data/<int:item_id>", methods=["GET"])
def get_by_id(item_id):
    item = Inventory.get_item(item_id)
    if not item:
        return {"error": "Item not found"}, 404
    return {"data": item.__dict__}, 200


@app.route("/data", methods=["POST"])
def add_item():
    data = request.get_json()
    name = data.get("name")
    barcode = data.get("barcode")
    price = data.get("price")
    stock = data.get("stock")
    if None in ([name, barcode, price, stock]):
        return {"error": "Missing required fields"}, 400
    item = Inventory.add_item(name, barcode, price, stock)
    return {"data": item.to_dict()}, 201


@app.route("/data/<int:item_id>", methods=["PATCH"])
def update_item(item_id):
    data = request.get_json()
    if data is None:
        return {"error": "No updates provided"}, 400
    try:
        item = Inventory.update_item(item_id, data)
        return {"data": item.to_dict()}, 200
    except ValueError as e:
        msg = str(e)
        if msg == "Item not found":
            return {"error": msg}, 404
        else:
            return {"error": str(e)}, 400


@app.route("/data/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    try:
        item = Inventory.remove_item(item_id)
        return {"data": item.to_dict()}, 204
    except ValueError as e:
        msg = str(e)
        if msg == "Item not found":
            return {"error": msg}, 404
        else:
            return {"error": str(e)}, 400


if __name__ == "__main__":
    app.run(debug=True)
