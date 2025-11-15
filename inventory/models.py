class Item:
    def __init__(
        self, id, name, barcode, brand, quantity, ingredients, price, stock, categories
    ):
        self.id = id
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.quantity = quantity
        self.ingredients = ingredients
        self.price = price
        self.stock = stock
        self.categories = categories
