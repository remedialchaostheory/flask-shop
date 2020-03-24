from unittest import TestCase
from models.item import ItemModel


class ItemTest(TestCase):
    def setUp(self) -> None:
        pass

    def test_create_item(self):
        item_name = 'Test Item'
        item_price = 999.99
        item = ItemModel(item_name, item_price)

        self.assertEqual(item.name, item_name,
                         'The name of the item does not equal it\'s creation value')
        self.assertEqual(item.price, item_price,
                         'The price of the item does not equal it\'s creation value')

    def test_json(self):
        item_name = 'Test Item'
        item_price = 999.99
        item = ItemModel(item_name, item_price)

        expected = {'name': item_name, 'price': item_price}
        self.assertDictEqual(item.json(), expected,
                             f'JSON export does not match. Actual: {item.json()}, Expected: {expected}')
