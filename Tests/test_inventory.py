import os
import sys

import pytest

# Ensure project root (parent of Tests/) is on sys.path
CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from inventory.models import Item
from inventory.services import InventoryManager


@pytest.fixture
def manager():
    """Return a fresh InventoryManager for each test."""
    return InventoryManager()


def test_item_to_dict():
    item = Item(
        id=1,
        name="Test Item",
        barcode="1234567890",
        brand="Test Brand",
        ingredients="water, salt",
        price=3.99,
        stock=5,
        categories="Category A, Category B",
    )

    data = item.to_dict()

    assert data["id"] == 1
    assert data["name"] == "Test Item"
    assert data["barcode"] == "1234567890"
    assert data["brand"] == "Test Brand"
    assert data["ingredients"] == "water, salt"
    assert data["price"] == 3.99
    assert data["stock"] == 5
    assert data["categories"] == "Category A, Category B"


def test_add_item_creates_item_and_assigns_id(manager):
    item = manager.add_item(
        name="Noodles",
        barcode="1234567890",
        price=2.50,
        stock=3,
    )

    # correct type and fields
    assert isinstance(item, Item)
    assert item.id == 1  # first item should get id 1
    assert item.name == "Noodles"
    assert item.barcode == "1234567890"
    assert item.price == 2.50
    assert item.stock == 3

    # inventory should contain exactly this item
    items = manager.list_items()
    assert len(items) == 1
    assert items[0] is item


def test_add_item_increments_id(manager):
    item1 = manager.add_item("A", "111", 1.0, 1)
    item2 = manager.add_item("B", "222", 2.0, 2)

    assert item1.id == 1
    assert item2.id == 2


def test_get_item_returns_item_when_exists(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)

    found = manager.get_item(item.id)

    assert found is item


def test_get_item_returns_none_when_missing(manager):
    # no items yet
    assert manager.get_item(999) is None

    # or after adding some
    manager.add_item("A", "111", 1.0, 1)
    assert manager.get_item(999) is None


def test_update_item_updates_fields(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)

    updated = manager.update_item(item.id, {"name": "Spicy Noodles", "price": 3.0})

    assert updated is item
    assert item.name == "Spicy Noodles"
    assert item.price == 3.0
    # unchanged fields
    assert item.barcode == "123"
    assert item.stock == 3


def test_update_item_raises_for_missing_item(manager):
    with pytest.raises(ValueError, match="Item not found"):
        manager.update_item(999, {"name": "Nope"})


def test_update_item_raises_for_no_updates(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)
    with pytest.raises(ValueError, match="No updates provided"):
        manager.update_item(item.id, {})


def test_update_item_raises_for_invalid_field(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)
    with pytest.raises(ValueError, match="Invalid field"):
        manager.update_item(item.id, {"does_not_exist": "x"})


def test_update_item_cannot_change_id_or_barcode(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)

    with pytest.raises(ValueError, match="Cannot update field: id"):
        manager.update_item(item.id, {"id": 99})

    with pytest.raises(ValueError, match="Cannot update field: barcode"):
        manager.update_item(item.id, {"barcode": "999"})


def test_remove_item_removes_and_returns_item(manager):
    item = manager.add_item("Noodles", "123", 2.5, 3)

    removed = manager.remove_item(item.id)

    assert removed is item
    assert manager.list_items() == []


def test_remove_item_raises_for_missing_item(manager):
    with pytest.raises(ValueError, match="Item not found"):
        manager.remove_item(999)
