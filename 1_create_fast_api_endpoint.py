from fastapi import FastAPI

app = FastAPI()

BOOKS = [
{"title": "A Brief History of Time", "author": "Stephen Hawking", "category": "Science"},
    {"title": "Sapiens", "author": "Yuval Noah Harari", "category": "History"},
    {"title": "The Alchemist", "author": "Paulo Coelho", "category": "Fiction"},
    {"title": "Atomic Habits", "author": "James Clear", "category": "Self-Help"},
    {"title": "Clean Code", "author": "Robert C. Martin", "category": "Programming"}
]


@app.get("/api-endpoint")
async def first_api():
    return BOOKS