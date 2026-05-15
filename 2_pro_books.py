from typing import Optional

from fastapi import FastAPI, Path, Query
from pydantic import BaseModel, Field

app = FastAPI()


# Normal Python class used to store book objects in memory
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id: int, title: str, author: str, description: str, rating: int, published_date: int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# Pydantic model used for request body validation
class BookRequest(BaseModel):
    # ID is optional because for creating a new book, we generate it automatically
    id: Optional[int] = Field(default=None, description="ID is not needed on create")

    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)

    # Published year should be required, so no default=None here
    published_date: int = Field(description="Year of publication", ge=1000, le=2100)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "description": "A fellowship of men and dwarves",
                "rating": 4,
                "published_date": 1937,
            }
        }
    }


BOOKS = [
    Book(1, "The Hobbit", "J.R.R. Tolkien", "A fellowship of men and dwarves", 4, 1937),
    Book(2, "The Lord of the Rings", "J.R.R. Tolkien", "A fellowship of men and dwarves", 5, 1954),
    Book(3, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "A young wizard begins his magical journey at Hogwarts", 5, 1997),
    Book(4, "1984", "George Orwell", "A dystopian world ruled by surveillance and control", 4, 1949),
    Book(5, "To Kill a Mockingbird", "Harper Lee", "A story of justice and racial inequality in a small town", 5, 1960),
    Book(6, "The Great Gatsby", "F. Scott Fitzgerald", "A young man's adventures in a world of magic and alchemy", 4, 1925),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# Fetch one book by ID
@app.get("/books/{book_id}")
async def read_book(book_id: int = Path(gt=0, description="Book ID must be greater than 0")):
    for book in BOOKS:
        if book.id == book_id:
            return book

    return {"message": "Book not found"}


# Fetch books by rating using query parameter
# Example: /books/rating/?rating=5
@app.get("/books/rating/")
async def fetch_book_by_rating(rating: int= Query(gt=0, lt=6, description="Rating must be between 1 and 5")):
    books_to_return = []

    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)

    return books_to_return


# Fetch books by published year using query parameter
# Example: /books/published/?published_date=1937
@app.get("/books/published/")
async def find_by_publish_date(published_date: int = Query(ge=1000, le=2100, description="Published date must be between 1000 and 2100")):
    books_to_return = []

    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)

    return books_to_return


# Create a new book
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    # Convert Pydantic model into dictionary, then unpack it into Book class
    new_book = Book(**book_request.model_dump())

    # Assign a new ID automatically
    new_book = assign_book_id(new_book)

    BOOKS.append(new_book)

    return new_book


# Helper function, not an API endpoint
def assign_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# Update existing book
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            return {"message": "Book updated successfully"}

    return {"message": "Book not found"}


# Delete book by ID
@app.delete("/books/{book_id}")
async def delete_book(book_id: int = Path(gt=0)):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}

    return {"message": "Book not found"}