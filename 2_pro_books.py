from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

class Book:
    id:int
    title:str
    author: str
    description:str
    rating:int

    def __init__(self, id:int, title:str, author: str, description:str, rating:int):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default =None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "description": "A fellowship of men and dwarves",
                "rating": 4,
            }
        }
    }


BOOKS = [
    Book(1, "The Hobbit", "", "A fellowship of men and dwarves", 4),
    Book(2, "The Lord of the Rings", "", "A fellowship of men and dwarves", 5),
    Book(3, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling", "A young wizard begins his magical journey at Hogwarts", 5),
    Book(4, "1984", "George Orwell", "A dystopian world ruled by surveillance and control", 4),
    Book(5, "To Kill a Mockingbird", "Harper Lee", "A story of justice and racial inequality in a small town", 5),
    Book(6, "The Great Gatsby", "F. Scott Fitzgerald", "A young man's adventures in a world of magic and alchemy", 4),
]


@app.get("/books")
async def read_all_books():
    return BOOKS


# Function that fetches the book by the id
@app.get("/books/{book_id}")
async def read_book(book_id: int):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return {"message": "Book not found"}


# Function that fetches the book by rating
@app.get("/books/")
async def fetch_book_by_rating(rating: int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return




@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())  # book_request.model_dump() -> converts Pydantic object → dictionary.
    BOOKS.append(find_book_id(new_book))
    return book_request

def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# Update book with the book request
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
