from models.item import ItemModel
from tests.base_test import BaseTest


class ItemTest(BaseTest):
    def test_crud(self):
        with self.app_context():
            item = ItemModel('Test', 99.99)

            self.assertIsNone(
                ItemModel.find_by_name('Test'),
                f'Found item: {item.name}. Expected None.'
            )
            item.save_to_db()
            self.assertIsNotNone(
                ItemModel.find_by_name('Test'),
                f'Did not find item: {item.name}'
            )
            item.delete_from_db()
            self.assertIsNone(
                ItemModel.find_by_name('Test'),
                f'Found item: {item.name}. Expected None.'
            )
