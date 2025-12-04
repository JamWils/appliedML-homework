import unittest
import sys
import os
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from library.cart import Cart
from library.item import Item


class TestCart(unittest.TestCase):
    """Test suite for the Cart class."""

    def setUp(self):
        """Create a temporary database file for each test."""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.write('{"Items": {}}')
        self.temp_file.close()
        self.cart = Cart(database_path=self.temp_file.name)

    def tearDown(self):
        """Clean up temporary file after each test."""
        os.unlink(self.temp_file.name)

    def test_cart_creation(self):
        """Test that a cart can be created with a database path."""
        self.assertEqual(self.cart.database_path, self.temp_file.name)
        self.assertEqual(self.cart.itemCount, 0)

    def test_cart_has_unique_id(self):
        """Test that each cart gets a unique UUID."""
        cart2 = Cart(database_path=self.temp_file.name)
        self.assertNotEqual(self.cart.id, cart2.id)

    def test_is_empty_true_when_no_items(self):
        """Test isEmpty returns True for empty cart."""
        self.assertTrue(self.cart.isEmpty)

    def test_is_empty_false_after_adding_item(self):
        """Test isEmpty returns False after adding an item."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            self.assertFalse(self.cart.isEmpty)


class TestAddItem(unittest.TestCase):
    """Test suite for the add_item method."""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.write('{"Items": {}}')
        self.temp_file.close()
        self.cart = Cart(database_path=self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_add_item_returns_true(self):
        """Test that add_item returns True on success."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            result = self.cart.add_item(item)
            self.assertTrue(result)

    def test_add_item_increments_count(self):
        """Test that add_item increments itemCount."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            self.assertEqual(self.cart.itemCount, 1)

    def test_add_item_persists_to_file(self):
        """Test that add_item saves the item to the JSON file."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)

            with open(self.temp_file.name, 'r') as f:
                data = json.load(f)

            self.assertIn('9781234567890', data['Items'])
            self.assertEqual(data['Items']['9781234567890']['title'], "Test Book")

    def test_add_multiple_items(self):
        """Test adding multiple items to cart."""
        with patch('library.utils.RandomUtils.generate_isbn', side_effect=['9781111111111', '9782222222222']):
            item1 = Item(title="Book One", author="Author One", type="book")
            item2 = Item(title="Book Two", author="Author Two", type="book")
            self.cart.add_item(item1)
            self.cart.add_item(item2)
            self.assertEqual(self.cart.itemCount, 2)


class TestRemoveByIndex(unittest.TestCase):
    """Test suite for the remove_by_index method."""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.write('{"Items": {}}')
        self.temp_file.close()
        self.cart = Cart(database_path=self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_remove_from_empty_cart_returns_false(self):
        """Test that removing from empty cart returns False."""
        result = self.cart.remove_by_index(0)
        self.assertFalse(result)

    def test_remove_invalid_index_returns_false(self):
        """Test that removing with invalid index returns False."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            result = self.cart.remove_by_index(5)
            self.assertFalse(result)

    def test_remove_negative_index_returns_false(self):
        """Test that removing with negative index returns False."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            result = self.cart.remove_by_index(-1)
            self.assertFalse(result)

    def test_remove_valid_index_returns_true(self):
        """Test that removing with valid index returns True."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            result = self.cart.remove_by_index(0)
            self.assertTrue(result)

    def test_remove_decrements_count(self):
        """Test that remove_by_index decrements itemCount."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            self.cart.remove_by_index(0)
            self.assertEqual(self.cart.itemCount, 0)

    def test_remove_persists_to_file(self):
        """Test that remove_by_index updates the JSON file."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="Test Book", author="Test Author", type="book")
            self.cart.add_item(item)
            self.cart.remove_by_index(0)

            with open(self.temp_file.name, 'r') as f:
                data = json.load(f)

            self.assertEqual(len(data['Items']), 0)


class TestEmptyCart(unittest.TestCase):
    """Test suite for the empty_cart method."""

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.write('{"Items": {}}')
        self.temp_file.close()
        self.cart = Cart(database_path=self.temp_file.name)

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_empty_cart_returns_true(self):
        """Test that empty_cart returns True."""
        result = self.cart.empty_cart()
        self.assertTrue(result)

    def test_empty_cart_on_empty_cart(self):
        """Test that empty_cart works on already empty cart."""
        result = self.cart.empty_cart()
        self.assertTrue(result)
        self.assertEqual(self.cart.itemCount, 0)

    def test_empty_cart_removes_all_items(self):
        """Test that empty_cart removes all items."""
        with patch('library.utils.RandomUtils.generate_isbn', side_effect=['9781111111111', '9782222222222', '9783333333333']):
            for i in range(3):
                item = Item(title=f"Book {i}", author=f"Author {i}", type="book")
                self.cart.add_item(item)

            self.cart.empty_cart()
            self.assertEqual(self.cart.itemCount, 0)

    def test_empty_cart_persists_to_file(self):
        """Test that empty_cart updates the JSON file."""
        with patch('library.utils.RandomUtils.generate_isbn', side_effect=['9781111111111', '9782222222222']):
            for i in range(2):
                item = Item(title=f"Book {i}", author=f"Author {i}", type="book")
                self.cart.add_item(item)

            self.cart.empty_cart()

            with open(self.temp_file.name, 'r') as f:
                data = json.load(f)

            self.assertEqual(len(data['Items']), 0)


if __name__ == '__main__':
    unittest.main()
