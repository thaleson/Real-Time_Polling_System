# app/schemas.py

from pydantic import BaseModel, Field
from typing import List, Dict

class CreatePollRequest(BaseModel):
    """
    Schema for creating a new poll.

    Attributes:
        question (str): The question to be asked in the poll.
        options (List[str]): A list of options available for the poll.
    """
    question: str = Field(..., example="Qual é a sua linguagem de programação favorita?")
    options: List[str] = Field(..., example=["Python", "JavaScript", "Java", "C++"])

class VoteRequest(BaseModel):
    """
    Schema for voting in a poll.

    Attributes:
        option (str): The selected option to vote for in the poll.
    """
    option: str = Field(..., example="Python")

class PollResponse(BaseModel):
    """
    Schema for the response returned when querying a poll.

    Attributes:
        id (str): Unique identifier for the poll.
        question (str): The question being asked in the poll.
        options (Dict[str, int]): A dictionary of options and their respective vote counts.
    """
    id: str
    question: str
    options: Dict[str, int]
