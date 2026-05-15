from fastapi import FastAPI, Body
from pydantic import BaseModel

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
    id: int
    title: str
    author: str
    description: str
    rating: int





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


@app.post("/create_book")
async def create_book(book_request: BookRequest ):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(new_book)
    return book_request