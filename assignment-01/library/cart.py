import json
from dataclasses import dataclass, field
from library.item import Item, Availability
from library.utils import RandomUtils
from library.file_io import FStream

@dataclass
class Cart:
    database_path: str
    inventory_path: str = "assignment-01/library_inventory.json"
    itemCount: int = 0
    id: str = field(default_factory=RandomUtils.generate_uuidv4)

    @property
    def isEmpty(self) -> bool:
        """Check if the cart is empty."""
        return self.itemCount == 0
    
    def get_all_items(self, verbose=False) -> list[Item]:
        """Retrieve all items in the cart."""
        data_file = FStream.load_json_files(self.database_path)
        self.itemCount = len(data_file.items())
        

        if verbose:
            FStream.print_json(self.items)

        return self.items
    
    def search_books(self, query: str) -> list[Item]:
        data = FStream.load_json_files(self.database_path)
        matching_items = []
        for item_id, item_data in data["Items"].items():
            item = Item(title=item_data["title"], author=item_data["author"], id=item_data["id"], type=item_data["type"])
            if query.lower() in item.search_string().lower():
                matching_items.append(item)

        if len(matching_items) == 0:
            print("No items found")

        else:
            for item in matching_items:
                print(f"Found: {item.type}-{item.title}")

        return matching_items

    def add_item(self, item: Item) -> bool:
        """Add an item to the cart."""
        data = FStream.load_json_files(self.database_path)
        if "Items" not in data:
            data["Items"] = {}

        data["Items"][item.id] = {
            "id": item.id,
            "title": item.title,
            "author": item.author,
            "type": item.type
        }

        FStream.save_json_files(self.database_path, data)
        self.itemCount += 1
        return True

    def remove_by_index(self, index: int) -> bool:
        """Remove an item from the cart by its index."""
        data = FStream.load_json_files(self.database_path)

        if "Items" not in data or len(data["Items"]) == 0:
            print("Cart is empty")
            return False

        item_ids = list(data["Items"].keys())

        if index < 0 or index >= len(item_ids):
            print(f"Index {index} out of range. Cart has {len(item_ids)} items.")
            return False

        item_id = item_ids[index]
        del data["Items"][item_id]
        FStream.save_json_files(self.database_path, data)
        self.itemCount -= 1
        return True

    def empty_cart(self) -> bool:
        """Remove all items from the cart."""
        data = FStream.load_json_files(self.database_path)
        data["Items"] = {}
        FStream.save_json_files(self.database_path, data)
        self.itemCount = 0
        return True

    def is_available(self, item_id: str) -> bool:
        """Check if an item is available to borrow."""
        inventory = FStream.load_json_files(self.inventory_path)

        if "Books" not in inventory or item_id not in inventory["Books"]:
            print(f"Item {item_id} not found in inventory")
            return False

        book = inventory["Books"][item_id]
        available = book["total_copies"] - book["borrowed_copies"]
        return available > 0

    def get_availability(self, item_id: str) -> Availability | None:
        """Get availability info for an item."""
        inventory = FStream.load_json_files(self.inventory_path)

        if "Books" not in inventory or item_id not in inventory["Books"]:
            return None

        book = inventory["Books"][item_id]
        return Availability(
            isbn=item_id,
            total_copies=book["total_copies"],
            borrowed_copies=book["borrowed_copies"]
        )

    def borrow_item(self, item_id: str) -> bool:
        """Borrow an item from the library."""
        if not self.is_available(item_id):
            print(f"Item {item_id} is not available for borrowing")
            return False

        inventory = FStream.load_json_files(self.inventory_path)
        inventory["Books"][item_id]["borrowed_copies"] += 1
        FStream.save_json_files(self.inventory_path, inventory)
        print(f"Successfully borrowed item {item_id}")
        return True

    def return_item(self, item_id: str) -> bool:
        """Return a borrowed item to the library."""
        inventory = FStream.load_json_files(self.inventory_path)

        if "Books" not in inventory or item_id not in inventory["Books"]:
            print(f"Item {item_id} not found in inventory")
            return False

        book = inventory["Books"][item_id]
        if book["borrowed_copies"] <= 0:
            print(f"Item {item_id} has no borrowed copies to return")
            return False

        inventory["Books"][item_id]["borrowed_copies"] -= 1
        FStream.save_json_files(self.inventory_path, inventory)
        print(f"Successfully returned item {item_id}")
        return True

    def list_available_books(self) -> list[dict]:
        """List all books that have available copies."""
        inventory = FStream.load_json_files(self.inventory_path)
        available_books = []

        if "Books" not in inventory:
            return available_books

        for item_id, book in inventory["Books"].items():
            available = book["total_copies"] - book["borrowed_copies"]
            if available > 0:
                available_books.append({
                    "id": item_id,
                    "title": book["title"],
                    "author": book["author"],
                    "available_copies": available
                })

        return available_books