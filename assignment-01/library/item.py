from dataclasses import dataclass, field
from library.utils import RandomUtils


@dataclass(order=True, slots=True)
class Availability:
    isbn: str
    total_copies: int
    borrowed_copies: int = 0

@dataclass(frozen=True, order=True, slots=True)
class Item:
    title: str
    author: str
    type: str = "book"
    id: str = field(default="")

    def __post_init__(self):
        # Set type and id based on whether it's a book or not
        if self.type == 'book':
            object.__setattr__(self, 'id', RandomUtils.generate_isbn())
        else:
            object.__setattr__(self, 'type', 'other')
            object.__setattr__(self, 'id', RandomUtils.generate_uuidv4())


    @property
    def search_string(self) -> str:
        if self.type == 'book':
            return f"{self.title} {self.author} {self.id}"
        else:
            return f"{self.title} {self.id}"