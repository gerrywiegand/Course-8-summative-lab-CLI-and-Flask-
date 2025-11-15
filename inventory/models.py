class Item:
    def __init__(self, id, name, barcode, brand, ingredients, price, stock, categories):
        self.id = id
        self.name = name
        self.barcode = barcode
        self.brand = brand
        self.ingredients = ingredients
        self.price = price
        self.stock = stock
        self.categories = categories

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "barcode": self.barcode,
            "brand": self.brand,
            "ingredients": self.ingredients,
            "price": self.price,
            "stock": self.stock,
            "categories": self.categories,
        }
