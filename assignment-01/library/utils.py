import random
import string
import time

class RandomUtils:
    @staticmethod
    def generate_isbn():
        """Generate a random ISBN-13 number."""
        prefix = '978'  # Common prefix for books
        group = str(random.randint(0, 5)).zfill(1)
        publisher = str(random.randint(0, 999)).zfill(3)
        title = str(random.randint(0, 99999)).zfill(5)
        partial_isbn = prefix + group + publisher + title

        # Calculate check digit
        total = 0
        for i, digit in enumerate(partial_isbn):
            n = int(digit)
            if i % 2 == 0:
                total += n
            else:
                total += n * 3
        remainder = total % 10
        check_digit = (10 - remainder) % 10

        return partial_isbn + str(check_digit)

    @staticmethod
    def generate_uuidv4():
        """Generate a random UUID version 4."""
        hex_digits = string.hexdigits.lower()
        uuid_template = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'
        uuid_chars = []

        for char in uuid_template:
            if char == 'x':
                uuid_chars.append(random.choice(hex_digits[:16]))
            elif char == 'y':
                uuid_chars.append(random.choice('89ab'))
            else:
                uuid_chars.append(char)

        return ''.join(uuid_chars)

    @staticmethod
    def generate_random_number(start=0, end=100):
        """Generate a random number within a specified range."""
        return random.randint(start, end)