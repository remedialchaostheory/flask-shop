from unittest import TestCase
from models.item import ItemModel
from tests.unit.unit_base_test import UnitBaseTest


class ItemTest(UnitBaseTest):
    def setUp(self) -> None:
        pass

    def test_create_item(self):
        store_id = 1
        item_name = 'Test Item'
        item_price = 999.99
        item = ItemModel(item_name, item_price, store_id)

        self.assertEqual(
            item.name, item_name,
            'The name of the item does not equal it\'s creation value'
        )
        self.assertEqual(
            item.price, item_price,
            'The price of the item does not equal it\'s creation value'
        )
        self.assertEqual(
            item.store_id, store_id,
            f'Got store id: {item.store_id}. Should be {store_id}'
        )
        print("item ->", item.store)
        self.assertIsNone(item.store)

    def test_json(self):
        item_name = 'Test Item'
        item_price = 999.99
        item = ItemModel(item_name, item_price, 1)

        expected = {'name': item_name, 'price': item_price}
        self.assertDictEqual(
            item.json(), expected,
            f'JSON export does not match. Actual: {item.json()}, Expected: {expected}'
        )

    # def test_
