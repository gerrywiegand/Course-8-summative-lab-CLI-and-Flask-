#!/usr/bin/env python3
import requests

API_URL = "http://127.0.0.1:5000"


def list_all_items():
    response = requests.get(f"{API_URL}/data")
    if response.status_code == 200:
        payload = response.json()
        items = payload.get("data", [])
        for item in items:
            print(
                f"ID: {item.get('id')} | "
                f"Name: {item.get('name')} | "
                f"Barcode: {item.get('barcode')} | "
                f"Price: {item.get('price')} | "
                f"Stock: {item.get('stock')} | "
            )
    else:
        print("Error:", response.status_code, response.text)


def get_item_by_id():
    item_id = input("Enter item ID: ").strip()
    if not item_id.isdigit():
        print("Item ID must be a number.")
        return

    response = requests.get(f"{API_URL}/data/{item_id}")
    if response.status_code == 200:
        item = response.json().get("data", {})
        print("Item details:")
        print(f"ID: {item.get('id')}")
        print(f"Name: {item.get('name')}")
        print(f"Barcode: {item.get('barcode')}")
        print(f"Brand: {item.get('brand')}")
        print(f"Price: {item.get('price')}")
        print(f"Stock: {item.get('stock')}")
        print(f"Categories: {item.get('categories')}")
    elif response.status_code == 404:
        print(f"No item found with ID {item_id}.")
    else:
        print("Error:", response.status_code, response.text)


def add_new_item():
    name = input("Enter item name: ").strip()
    barcode = input("Enter barcode: ").strip()
    price_str = input("Enter price: ").strip()
    stock_str = input("Enter stock quantity: ").strip()

    if not name or not barcode or not price_str or not stock_str:
        print("All fields are required.")
        return

    try:
        price = float(price_str)
        stock = int(stock_str)
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    payload = {
        "name": name,
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    try:
        response = requests.post(f"{API_URL}/data", json=payload)
        if response.status_code in (200, 201):
            body = response.json()
            item = body.get("data", {})
            warning = body.get("warning")

            print("\nItem created:")
            print(f"ID: {item.get('id')}")
            print(f"Name: {item.get('name')}")
            print(f"Barcode: {item.get('barcode')}")
            print(f"Brand: {item.get('brand')}")
            print(f"Price: {item.get('price')}")
            print(f"Stock: {item.get('stock')}")
            print(f"Categories: {item.get('categories')}")
            if warning:
                print(f"Warning from API: {warning}")
            print()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def update_item_cli():
    item_id = input("Enter item ID to update: ").strip()

    if not item_id.isdigit():
        print("Item ID must be a number.")
        return

    print("\nLeave fields blank to keep existing values.\n")

    name = input("New name: ").strip()
    barcode = input("New barcode: ").strip()
    price_str = input("New price: ").strip()
    stock_str = input("New stock quantity: ").strip()

    # Build the PATCH payload only with values that were provided
    payload = {}

    if name:
        payload["name"] = name

    if barcode:
        payload["barcode"] = barcode

    if price_str:
        try:
            payload["price"] = float(price_str)
        except ValueError:
            print("Price must be a number.")
            return

    if stock_str:
        try:
            payload["stock"] = int(stock_str)
        except ValueError:
            print("Stock must be an integer.")
            return

    if not payload:
        print("No updates provided.")
        return

    try:
        response = requests.patch(f"{API_URL}/data/{item_id}", json=payload)

        if response.status_code == 200:
            body = response.json()
            item = body.get("data", {})
            warning = body.get("warning")

            print("\nItem updated:")
            print(f"ID: {item.get('id')}")
            print(f"Name: {item.get('name')}")
            print(f"Barcode: {item.get('barcode')}")
            print(f"Brand: {item.get('brand')}")
            print(f"Price: {item.get('price')}")
            print(f"Stock: {item.get('stock')}")
            print(f"Categories: {item.get('categories')}")
            if warning:
                print(f"Warning from API: {warning}")
            print()

        elif response.status_code == 404:
            print(f"No item found with ID {item_id}.")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def delete_item_cli():
    item_id = input("Enter item ID to delete: ").strip()

    if not item_id.isdigit():
        print("Item ID must be a number.")
        return

    confirm = (
        input(f"Are you sure you want to delete item {item_id}? (y/n): ")
        .strip()
        .lower()
    )
    if confirm != "y":
        print("Delete cancelled.")
        return

    try:
        response = requests.delete(f"{API_URL}/data/{item_id}")

        if response.status_code in (200, 204):
            print(f"Item {item_id} deleted successfully.\n")

        elif response.status_code == 404:
            print(f"No item found with ID {item_id}.")

        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def add_item_from_barcode_cli():
    print("This will add an item and try to enrich it from OpenFoodFacts.\n")

    barcode = input("Enter barcode: ").strip()
    name = input("Enter item name: ").strip()
    price_str = input("Enter price: ").strip()
    stock_str = input("Enter stock quantity: ").strip()

    if not barcode or not name or not price_str or not stock_str:
        print("Barcode, name, price, and stock are all required.")
        return

    try:
        price = float(price_str)
        stock = int(stock_str)
    except ValueError:
        print("Price must be a number and stock must be an integer.")
        return

    payload = {
        "name": name,
        "barcode": barcode,
        "price": price,
        "stock": stock,
    }

    try:
        response = requests.post(f"{API_URL}/data", json=payload)

        if response.status_code in (200, 201):
            body = response.json()
            item = body.get("data", {})
            warning = body.get("warning")

            print("\nItem created (via OpenFoodFacts):")
            print(f"ID: {item.get('id')}")
            print(f"Name: {item.get('name')}")
            print(f"Barcode: {item.get('barcode')}")
            print(f"Brand: {item.get('brand')}")
            print(f"Price: {item.get('price')}")
            print(f"Stock: {item.get('stock')}")
            print(f"Categories: {item.get('categories')}")
            if warning:
                print(f"Warning from API: {warning}")
            print()
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def menu():
    print("Inventory Management CLI")
    print("1. List all items")
    print("2. Get item by ID")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("0. Exit")


def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            list_all_items()
            print("Listing all items...")

        elif choice == "2":
            get_item_by_id()

        elif choice == "3":
            print("Adding a new item...")
            add_new_item()

        elif choice == "4":
            print("Updating item...")
            update_item_cli()

        elif choice == "5":
            print("Deleting item...")
            delete_item_cli()
        elif choice == "6":
            print("Adding item from OpenFoodFacts (by barcode)...")
            add_item_from_barcode_cli()

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
