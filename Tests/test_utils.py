import os
import sys

import pytest
import requests

# Ensure project root (parent of Tests/) is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from inventory.utils import fetch_inventory_data


def test_fetch_inventory_data_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass  # no error

        def json(self):
            return {
                "status": 1,
                "product": {
                    "product_name": "Test Noodles",
                    "brands": "BrandX",
                    "ingredients_text": "wheat, water, salt",
                    "categories": "Pasta, Noodles",
                },
            }

    def fake_get(url):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result = fetch_inventory_data("1234567890")

    assert result == {
        "name": "Test Noodles",
        "brands": "BrandX",
        "ingredients": "wheat, water, salt",
        "categories": "Pasta, Noodles",
    }


def test_fetch_inventory_data_not_found(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "status": 0,
                "product": {},
            }

    def fake_get(url):
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

    result = fetch_inventory_data("does-not-exist")

    assert result is None


def test_fetch_inventory_data_request_exception(monkeypatch):
    def fake_get(url):
        raise requests.RequestException("Network down")

    monkeypatch.setattr(requests, "get", fake_get)

    with pytest.raises(ValueError, match="API request failed"):
        fetch_inventory_data("1234567890")
