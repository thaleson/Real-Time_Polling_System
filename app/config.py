# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    Configuration class for environment variables and system parameters.

    This class loads environment variables using the `python-dotenv` package to facilitate
    the management of configurations in development and production environments.

    Attributes:
        DATABASE_URL (str): Database connection URL. It is loaded from the 
        environment variable `DATABASE_URL`. If not defined, it defaults to a 
        local SQLite database with the file `polling.db`.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./polling.db")

settings = Settings()
