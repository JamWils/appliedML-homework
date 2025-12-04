import unittest
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from library.item import Item, Availability


class TestAvailability(unittest.TestCase):
    """Test suite for the Availability dataclass."""

    def test_availability_creation(self):
        """Test basic Availability creation with all fields."""
        avail = Availability(isbn="9780123456789", total_copies=5, borrowed_copies=2)
        self.assertEqual(avail.isbn, "9780123456789")
        self.assertEqual(avail.total_copies, 5)
        self.assertEqual(avail.borrowed_copies, 2)

    def test_availability_default_borrowed_copies(self):
        """Test that borrowed_copies defaults to 0."""
        avail = Availability(isbn="9780123456789", total_copies=3)
        self.assertEqual(avail.borrowed_copies, 0)

    def test_availability_ordering(self):
        """Test that Availability instances can be compared."""
        avail1 = Availability(isbn="9780000000001", total_copies=5)
        avail2 = Availability(isbn="9780000000002", total_copies=5)
        self.assertLess(avail1, avail2)

    def test_availability_mutability(self):
        """Test that Availability fields can be modified (not frozen)."""
        avail = Availability(isbn="9780123456789", total_copies=5)
        avail.borrowed_copies = 3
        self.assertEqual(avail.borrowed_copies, 3)


class TestItem(unittest.TestCase):
    """Test suite for the Item dataclass."""

    def test_item_creation_book(self):
        """Test Item creation with type='book'."""
        item = Item(title="The Great Gatsby", author="F. Scott Fitzgerald", type="book")
        self.assertEqual(item.title, "The Great Gatsby")
        self.assertEqual(item.author, "F. Scott Fitzgerald")
        self.assertEqual(item.type, "book")

    def test_item_creation_other_type(self):
        """Test Item creation with non-book type."""
        item = Item(title="Nature Documentary", author="David Attenborough", type="dvd")
        self.assertEqual(item.title, "Nature Documentary")
        self.assertEqual(item.author, "David Attenborough")
        self.assertEqual(item.type, "other")

    def test_item_default_type_is_book(self):
        """Test that Item without explicit type defaults to 'book'."""
        item = Item(title="Unknown Item", author="Unknown Author")
        self.assertEqual(item.type, "book")

    def test_item_book_has_isbn_format(self):
        """Test that book items get an ISBN-format ID."""
        item = Item(title="Test Book", author="Test Author", type="book")
        self.assertEqual(len(item.id), 13)
        self.assertTrue(item.id.isdigit())
        self.assertTrue(item.id.startswith("978"))

    def test_item_other_has_uuid_format(self):
        """Test that non-book items get a UUID-format ID."""
        item = Item(title="Test DVD", author="Test Director", type="dvd")
        self.assertRegex(
            item.id,
            r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
        )

    def test_item_is_frozen(self):
        """Test that Item is immutable (frozen dataclass)."""
        item = Item(title="Frozen Book", author="Cold Author", type="book")
        with self.assertRaises(AttributeError):
            item.title = "New Title"

    def test_item_ordering(self):
        """Test that Item instances can be compared."""
        item1 = Item(title="A Book", author="Author A", type="book")
        item2 = Item(title="B Book", author="Author B", type="book")
        self.assertLess(item1, item2)

    def test_search_string_book(self):
        """Test search_string for book type includes title, author, and id."""
        with patch('library.utils.RandomUtils.generate_isbn', return_value='9781234567890'):
            item = Item(title="My Book", author="My Author", type="book")
            self.assertEqual(item.search_string, "My Book My Author 9781234567890")

    def test_search_string_other(self):
        """Test search_string for non-book type includes title and id only."""
        with patch('library.utils.RandomUtils.generate_uuidv4', return_value='12345678-1234-4123-8123-123456789abc'):
            item = Item(title="My DVD", author="Director Name", type="dvd")
            self.assertEqual(item.search_string, "My DVD 12345678-1234-4123-8123-123456789abc")

    def test_multiple_items_have_unique_ids(self):
        """Test that multiple items get unique IDs."""
        items = [Item(title=f"Book {i}", author="Author", type="book") for i in range(10)]
        ids = [item.id for item in items]
        self.assertEqual(len(ids), len(set(ids)), "All item IDs should be unique")


if __name__ == '__main__':
    unittest.main()
