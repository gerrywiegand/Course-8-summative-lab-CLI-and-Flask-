import requests
from data import URL


def fetch_inventory_data(barcode: str):
    try:
        response = requests.get(f"{URL}/api/v0/product/{barcode}.json")
        response.raise_for_status()
        data = response.json()
        if data.get("status") == 0:
            return None
        product = data.get("product", {})

        return {
            "name": product.get("product_name", None),
            "brands": product.get("brands", None),
            "ingredients": product.get("ingredients_text", None),
            "categories": product.get("categories", None),
        }
    except requests.RequestException as e:
        raise ValueError(f"API request failed: {e}")
