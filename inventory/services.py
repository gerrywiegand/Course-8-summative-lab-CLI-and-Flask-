from inventory.models import Item


class InventoryManager:
    def __init__(self):
        self.inventory = []

    def get_item(self, item_id):
        for item in self.inventory:
            if item.id == item_id:
                return item
        return None

    def add_item(
        self,
        name,
        barcode,
        price,
        stock,
        brand=None,
        ingredients=None,
        categories=None,
    ):
        item_id = max([item.id for item in self.inventory], default=0) + 1
        item = Item(
            id=item_id,
            name=name,
            barcode=barcode,
            brand=brand,
            ingredients=ingredients,
            price=price,
            stock=stock,
            categories=categories,
        )
        self.inventory.append(item)
        return item

    def update_item(self, item_id, updates_dict):
        item = self.get_item(item_id)
        if not item:
            raise ValueError("Item not found")
        if not updates_dict:
            raise ValueError("No updates provided")
        for key, value in updates_dict.items():
            if key in ("id", "barcode"):
                raise ValueError(f"Cannot update field: {key}")
            if not hasattr(item, key):
                raise ValueError(f"Invalid field: {key}")
            setattr(item, key, value)
        return item

    def remove_item(self, item_id):
        item = self.get_item(item_id)
        if not item:
            raise ValueError("Item not found")
        self.inventory.remove(item)
        return item

    def list_items(self):
        return self.inventory
