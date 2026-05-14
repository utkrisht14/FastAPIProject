from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "A Brief History of Time", "author": "Stephen Hawking", "category": "Science"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "History"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help"},
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Programming"}
]


@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/title/{book_title}")
async def read_book_by_title(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}


@app.get("/books/category/")
async def read_category_by_query(category: str):
    books_to_return = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/author/{book_author}")
async def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book["author"].casefold() == book_author.casefold()
            and book["category"].casefold() == category.casefold()
        ):
            books_to_return.append(book)

    return books_to_return