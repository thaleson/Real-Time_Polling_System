# app/database.py

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from .config import settings
from .models import Base  # Importing Base from models.py

DATABASE_URL = settings.DATABASE_URL

# Create an asynchronous database engine
engine = create_async_engine(
    DATABASE_URL, echo=True, future=True
)

# Create a configured "Session" class
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    """
    Dependency that provides a database session.

    This asynchronous generator function yields a database session object 
    for use in API endpoints or other functions that require database 
    access. The session is automatically managed to ensure proper 
    cleanup after use.

    Yields:
        AsyncSession: An instance of AsyncSession for database operations.
    """
    async with async_session() as session:
        yield session
