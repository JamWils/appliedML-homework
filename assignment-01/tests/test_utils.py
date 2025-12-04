import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from library.utils import RandomUtils


class TestGenerateISBN(unittest.TestCase):
    """Test suite for the generate_isbn static method."""

    def test_isbn_length(self):
        """Test that generated ISBN has exactly 13 digits."""
        isbn = RandomUtils.generate_isbn()
        self.assertEqual(len(isbn), 13, f"ISBN should be 13 digits, got {len(isbn)}")

    def test_isbn_is_numeric(self):
        """Test that generated ISBN contains only numeric characters."""
        isbn = RandomUtils.generate_isbn()
        self.assertTrue(isbn.isdigit(), f"ISBN should contain only digits, got {isbn}")

    def test_isbn_prefix(self):
        """Test that generated ISBN starts with the '978' prefix."""
        isbn = RandomUtils.generate_isbn()
        self.assertTrue(isbn.startswith('978'), f"ISBN should start with '978', got {isbn[:3]}")

    def test_isbn_check_digit_valid(self):
        """Test that the check digit is correctly calculated."""
        isbn = RandomUtils.generate_isbn()

        total = 0
        for i, digit in enumerate(isbn[:-1]):  # All digits except check digit
            n = int(digit)
            if i % 2 == 0:
                total += n
            else:
                total += n * 3

        remainder = total % 10
        expected_check_digit = (10 - remainder) % 10
        actual_check_digit = int(isbn[-1])

        self.assertEqual(
            actual_check_digit,
            expected_check_digit,
            f"Check digit validation failed for ISBN {isbn}"
        )

    def test_isbn_uniqueness(self):
        """Test that multiple calls generate different ISBNs (probabilistic)."""
        isbns = [RandomUtils.generate_isbn() for _ in range(100)]
        unique_isbns = set(isbns)

        self.assertEqual(
            len(unique_isbns),
            100,
            f"Expected 100 unique ISBNs out of 100, got {len(unique_isbns)}"
        )

    def test_isbn_group_identifier_range(self):
        """Test that the group identifier is a single digit from 0-5."""
        isbn = RandomUtils.generate_isbn()
        group_identifier = isbn[3]  # Position after '978' prefix
        self.assertIn(
            group_identifier,
            '012345',
            f"Group identifier should be 0-5, got {group_identifier}"
        )

    def test_isbn_publisher_code_length(self):
        """Test that publisher code is 3 digits (positions 4-6)."""
        isbn = RandomUtils.generate_isbn()
        publisher_code = isbn[4:7]
        self.assertEqual(
            len(publisher_code),
            3,
            f"Publisher code should be 3 digits, got {len(publisher_code)}"
        )
        self.assertTrue(
            publisher_code.isdigit(),
            f"Publisher code should be numeric, got {publisher_code}"
        )

    def test_isbn_title_code_length(self):
        """Test that title code is 5 digits (positions 7-11)."""
        isbn = RandomUtils.generate_isbn()
        title_code = isbn[7:12]  # Before check digit (position 12)
        self.assertEqual(
            len(title_code),
            5,
            f"Title code should be 5 digits, got {len(title_code)}"
        )
        self.assertTrue(
            title_code.isdigit(),
            f"Title code should be numeric, got {title_code}"
        )

    def test_isbn_structure_breakdown(self):
        """Test the complete structure: prefix(3) + group(1) + publisher(3) + title(5) + check(1)."""
        isbn = RandomUtils.generate_isbn()

        prefix = isbn[0:3]
        group = isbn[3:4]
        publisher = isbn[4:7]
        title = isbn[7:12]
        check_digit = isbn[12:13]

        self.assertEqual(prefix, '978')
        self.assertEqual(len(group), 1)
        self.assertEqual(len(publisher), 3)
        self.assertEqual(len(title), 5)
        self.assertEqual(len(check_digit), 1)

        self.assertEqual(len(prefix + group + publisher + title + check_digit), 13)
        self.assertEqual(len(isbn), 13)

    def test_multiple_generations_all_valid(self):
        """Test that multiple generated ISBNs are all valid."""
        for _ in range(50):
            isbn = RandomUtils.generate_isbn()

            self.assertEqual(len(isbn), 13)
            self.assertTrue(isbn.isdigit())
            self.assertTrue(isbn.startswith('978'))

            total = 0
            for i, digit in enumerate(isbn[:-1]):
                n = int(digit)
                if i % 2 == 0:
                    total += n
                else:
                    total += n * 3
            remainder = total % 10
            expected_check_digit = (10 - remainder) % 10
            actual_check_digit = int(isbn[-1])
            self.assertEqual(actual_check_digit, expected_check_digit)


if __name__ == '__main__':
    unittest.main()
