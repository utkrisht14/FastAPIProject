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
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# Pydantic model for the book request used for validation
class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default =None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(ge=1, le=5)
    published_date: int = Field(description="Year of publication", default=None)


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
    Book(1, "The Hobbit", "J.R.R. Tolkien", "A fellowship of men and dwarves", 4, 1937),
    Book(2, "The Lord of the Rings", "J.R.R. Tolkien", "A fellowship of men and dwarves", 5, 1954),
    Book(3, "Harry Potter and the Sorcerer's Stone", "J.K. Rowling","A young wizard begins his magical journey at Hogwarts", 5, 1997),
    Book(4, "1984", "George Orwell", "A dystopian world ruled by surveillance and control", 4, 1949),
    Book(5, "To Kill a Mockingbird", "Harper Lee", "A story of justice and racial inequality in a small town", 5, 1960),
    Book(6, "The Great Gatsby", "F. Scott Fitzgerald", "A young man's adventures in a world of magic and alchemy", 4,1925),
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


# Function that get book by publish date
async def find_by_publish_date(published_date: int)
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return



# Function that creates a new book
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())  # book_request.model_dump() -> converts Pydantic object → dictionary.
    BOOKS.append(find_book_id(new_book))
    return book_request


# Function that assigns an id to the book
@app.get("/books/id")
def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


# Update book with the book request
@app.put("/books/update_book")
async def update_book(book: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book

# Delete the book by id
@app.delete("/books/{book_id")
async def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break
    return {"message": "Book deleted"}