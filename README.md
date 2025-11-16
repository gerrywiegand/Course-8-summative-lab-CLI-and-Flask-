# Inventory management CLI + Flask API

## A complete iventory management system built with

- Flask (REST API)
- Python CLI client
- In- memory service layer with item and inventory manager
- API requests from OpenFoodFacts
- Full Pytest suite

## Features

### Inventory system

able to create/edit/ and delte items in an inventory list with the follwoing values

- Name
- Id
- barcode
- price
- stock quantity
- brand
- ingredients
- categories

### CLI (command line interface)

user can execute the following commands

- List all inventory items
- View an item in more depth by ID
- Create and add new items to inventory through user input
- Update existing items (**note barcode and ID can not be changed**)
- delete an item
- create a new item via barcode from OpenFoodFacts

### Clean architecture

- models.py stores the item object and serializes them into a dictionary
- services.py houses the InventoryManager object
- utils.py contains function for fetch request
- app.py is the Flask application and routing
- cli.py is the frontend where users interact with the program

### Full pytest coverage

## Installation

### Clone Repo

git clone <your-repo-url>
cd Course-8-summative-lab-CLI-and-Flask

### Install dependencies

pipenv install
pipenv shell

## Running the API

### Start Flask server

python app.py

it will run at http://localhost:5000

## Running the CLI

python cli.py

You will see

Inventory Management CLI

1. List all items
2. Get item by ID
3. Add new item
4. Update item
5. Delete item
6. Add item from OpenFoodFacts (by barcode)
7. Exit

Each option communicates with the FLask API
Type your response and hit enter

## Running the Test Suite

pytest -q

## Author

Gerry Wiegand
