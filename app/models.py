# app/models.py

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, JSON
from typing import Dict

# Base class for declarative class definitions
Base = declarative_base()

class Poll(Base):
    """
    Poll model representing a polling question and its options.

    Attributes:
        id (str): Unique identifier for the poll.
        question (str): The question being asked in the poll.
        options (Dict[str, int]): A JSON object storing the options for the poll and 
                                   their respective vote counts.
                                   Example: {"Option A": 0, "Option B": 0, ...}
    """
    __tablename__ = "polls"

    id = Column(String, primary_key=True, index=True)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)  # {"Option A": 0, "Option B": 0, ...}
