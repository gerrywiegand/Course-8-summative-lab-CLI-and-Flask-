import os
import sys

import pytest

# Ensure project root is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app import app
from inventory.services import InventoryManager


@pytest.fixture
def client():
    # Reset the in-memory inventory before each test
    InventoryManager.inventory = []
    InventoryManager.next_id = 1

    with app.test_client() as client:
        yield client


def test_get_all_items_empty(client):
    response = client.get("/data")
    assert response.status_code == 200

    body = response.get_json()
    assert "data" in body
    assert body["data"] == []


def test_post_new_item(client):
    payload = {
        "name": "Noodles",
        "barcode": "123",
        "price": 2.50,
        "stock": 3,
    }

    response = client.post("/data", json=payload)

    assert response.status_code == 201
    data = response.get_json()["data"]

    assert data["id"] == 1
    assert data["name"] == "Noodles"
    assert data["barcode"] == "123"
    assert data["price"] == 2.50
    assert data["stock"] == 3


def test_get_item_by_id(client):
    # First, create an item
    client.post(
        "/data",
        json={
            "name": "Noodles",
            "barcode": "123",
            "price": 2.50,
            "stock": 3,
        },
    )

    response = client.get("/data/1")

    assert response.status_code == 200
    body = response.get_json()
    item = body["data"]

    assert item["id"] == 1
    assert item["name"] == "Noodles"
    assert item["barcode"] == "123"


def test_patch_item(client):
    # Create an item
    client.post(
        "/data",
        json={
            "name": "Noodles",
            "barcode": "123",
            "price": 2.50,
            "stock": 3,
        },
    )

    # Now update it
    response = client.patch("/data/1", json={"price": 3.00})

    assert response.status_code == 200
    body = response.get_json()
    item = body["data"]

    assert item["price"] == 3.00
    assert item["name"] == "Noodles"
    assert item["barcode"] == "123"


def test_delete_item(client):
    # Create an item
    client.post(
        "/data",
        json={
            "name": "Noodles",
            "barcode": "123",
            "price": 2.50,
            "stock": 3,
        },
    )

    # Delete it
    response = client.delete("/data/1")
    assert response.status_code == 204

    # Ensure it’s gone
    response = client.get("/data/1")
    assert response.status_code == 404
