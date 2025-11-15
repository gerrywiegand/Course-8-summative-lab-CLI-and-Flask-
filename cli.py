#!/usr/bin/env python3
from inventory.data import URL  # noqa: F401


def menu():
    print("Inventory Management CLI")
    print("1. List all items")
    print("2. Get item by ID")
    print("3. Add new item")
    print("4. Update item")
    print("5. Delete item")
    print("6. Add item from OpenFoodFacts (by barcode)")
    print("0. Exit")


def main():
    while True:
        menu()
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Exiting...")
            break
        elif choice == "1":
            print("Listing all items...")
            # Logic to list all items
        elif choice == "2":
            item_id = input("Enter item ID: ")
            print(f"Getting item with ID {item_id}...")
            # Logic to get item by ID
        elif choice == "3":
            print("Adding new item...")
            # Logic to add new item
        elif choice == "4":
            item_id = input("Enter item ID to update: ")
            print(f"Updating item with ID {item_id}...")
            # Logic to update item
        elif choice == "5":
            item_id = input("Enter item ID to delete: ")
            print(f"Deleting item with ID {item_id}...")
            # Logic to delete item
        elif choice == "6":
            barcode = input("Enter barcode: ")
            print(f"Adding item from OpenFoodFacts with barcode {barcode}...")
            # Logic to add item from OpenFoodFacts
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
