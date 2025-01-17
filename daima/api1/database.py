import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Loading environment variables
load_dotenv()

# Getting the database configuration from environment variables
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')

# Print debugging information
print(f"DB_HOST: {DB_HOST}, DB_PORT: {DB_PORT}, DB_NAME: {DB_NAME}, DB_USER: {DB_USER}, DB_PASSWORD: {DB_PASSWORD}")

# Building Database URLs
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Creating a Database Engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Get the database session generator
def get_db():
    db = SessionLocal()
    try:
        yield db  # Use yield to make it a generator
    finally:
        db.close()  # Ensure that the session is closed after completion
