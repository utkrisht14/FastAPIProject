# Imports create_engine function from SQLAlchemy.
# Used to establish connection between Python application and database.
from pathlib import Path

from sqlalchemy import create_engine


# Imports sessionmaker utility from SQLAlchemy ORM.
# Used to create database session objects for performing CRUD operations.
from sqlalchemy.orm import sessionmaker


# Imports declarative_base function from SQLAlchemy.
# Used to create a base class for ORM models (database tables).
from sqlalchemy.ext.declarative import declarative_base


# Database connection URL.
# Here SQLite database named todos.db will be created in current project folder.
DATABASE_PATH = Path(__file__).resolve().parent / "todos.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# Creates the main database engine/connection object.
# connect_args is needed for SQLite to allow usage with FastAPI async environment.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Creates a session factory for database interactions.
# autocommit=False means changes must be committed manually.
# autoflush=False prevents automatic flushing of changes before queries.
# bind=engine connects session to the created database engine.
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Creates a base class for all ORM database models.
# All table classes will inherit from this Base class.
Base = declarative_base()
