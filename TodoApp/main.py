from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status

import models
from database import SessionLocal, engine
from models import Todos

app = FastAPI()

# Create all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)


# Database dependency function
# It creates a database session for each request and closes it after the request is completed
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable database dependency type
db_dependency = Annotated[Session, Depends(get_db)]


# Request model for creating a new to-do
# This validates incoming JSON body before saving it to the database
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)

    # Must match the SQLAlchemy model column name: completed
    completed: bool


# API endpoint to fetch all todos
@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()


# API endpoint to fetch a single to-do by ID
@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    if todo_model is not None:
        return todo_model

    raise HTTPException(status_code=404, detail="Todo not found.")


# API endpoint to create a new to-do
@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    # Convert Pydantic model into dictionary and unpack it into SQLAlchemy model
    todo_model = Todos(**todo_request.model_dump())

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return todo_model


# API endpoint to update an existing to-do using its ID
@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
        db: db_dependency,          # Database session dependency
        todo_request: TodoRequest,  # Request body containing updated to-do data
        todo_id: int = Path(gt=0)              # ID received from URL path parameter

):

    # Query the database table "todos"
    # Filter the rows where Todos.id matches the provided todo_id
    # first() returns the first matching row or None if not found
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # If no to-do exists with the given ID, raise 404 error
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")

    # Update the title field of the fetched database object
    todo_model.title = todo_request.title

    # Update the description field
    todo_model.description = todo_request.description

    # Update the priority field
    todo_model.priority = todo_request.priority

    # Update the completed status field
    todo_model.completed = todo_request.completed

    # Add the modified object back into the session
    # SQLAlchemy tracks this object and prepares UPDATE query
    db.add(todo_model)

    # Commit changes permanently into the database
    db.commit()



# Delete the app endpoint
@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

