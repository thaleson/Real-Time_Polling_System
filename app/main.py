# app/main.py

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.future import select
from uuid import uuid4

from .database import engine, Base, get_db
from .models import Poll
from .schemas import CreatePollRequest, VoteRequest, PollResponse
from .websocket_manager import manager

import json

app = FastAPI(title="Real-Time Polling System")

# Mount the 'static' folder to serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_event():
    """
    Startup event that runs once when the application starts.

    This event handler is responsible for creating the necessary tables in 
    the database if they do not already exist. It uses the SQLAlchemy engine 
    to synchronize the database schema with the defined models.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.post("/polls/", response_model=PollResponse)
async def create_poll(poll: CreatePollRequest, db=Depends(get_db)):
    """
    Create a new poll.

    This endpoint allows users to create a new poll by providing a question 
    and a list of options. The created poll is stored in the database, and 
    a broadcast message is sent to connected clients to update them about the 
    new poll.

    Args:
        poll (CreatePollRequest): The poll data including the question and options.
        db (AsyncSession): The database session.

    Returns:
        PollResponse: The created poll response including its ID, question, and options.
    """
    poll_id = str(uuid4())
    options_dict = {option: 0 for option in poll.options}
    new_poll = Poll(id=poll_id, question=poll.question, options=options_dict)
    db.add(new_poll)
    await db.commit()
    await db.refresh(new_poll)
    
    # Send update to connected clients
    await manager.broadcast(poll_id, {
        "id": new_poll.id,
        "question": new_poll.question,
        "options": new_poll.options
    })

    return PollResponse(
        id=new_poll.id,
        question=new_poll.question,
        options=new_poll.options
    )

@app.get("/polls/{poll_id}", response_model=PollResponse)
async def get_poll(poll_id: str, db=Depends(get_db)):
    """
    Retrieve a poll by its ID.

    This endpoint allows users to fetch details of a specific poll using 
    its unique identifier.

    Args:
        poll_id (str): The ID of the poll to retrieve.
        db (AsyncSession): The database session.

    Returns:
        PollResponse: The retrieved poll response including its ID, question, and options.

    Raises:
        HTTPException: If the poll is not found, a 404 error is raised.
    """
    result = await db.execute(select(Poll).where(Poll.id == poll_id))
    poll = result.scalar_one_or_none()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    return PollResponse(
        id=poll.id,
        question=poll.question,
        options=poll.options
    )

@app.post("/polls/{poll_id}/vote/")
async def vote(poll_id: str, vote: VoteRequest, db=Depends(get_db)):
    """
    Vote for a specific option in a poll.

    This endpoint allows users to submit their vote for a particular 
    option in an existing poll. The vote is recorded, and a broadcast 
    message is sent to connected clients to update the vote counts.

    Args:
        poll_id (str): The ID of the poll to vote in.
        vote (VoteRequest): The vote data containing the chosen option.
        db (AsyncSession): The database session.

    Returns:
        JSONResponse: A message indicating the successful registration of the vote.

    Raises:
        HTTPException: If the poll is not found or the option is invalid, appropriate errors are raised.
    """
    result = await db.execute(select(Poll).where(Poll.id == poll_id))
    poll = result.scalar_one_or_none()
    if not poll:
        raise HTTPException(status_code=404, detail="Poll not found.")
    if vote.option not in poll.options:
        raise HTTPException(status_code=400, detail="Invalid option.")
    
    poll.options[vote.option] += 1
    db.add(poll)
    await db.commit()
    await db.refresh(poll)
    
    # Send update to connected clients
    await manager.broadcast(poll_id, {
        "id": poll.id,
        "question": poll.question,
        "options": poll.options
    })

    return JSONResponse(content={"message": "Vote recorded successfully."})

@app.websocket("/ws/polls/{poll_id}")
async def websocket_endpoint(websocket: WebSocket, poll_id: str):
    """
    WebSocket endpoint for real-time updates of a poll.

    This WebSocket connection allows clients to receive real-time updates 
    about the votes of a specific poll. Clients can connect and listen 
    for updates regarding the poll.

    Args:
        websocket (WebSocket): The WebSocket connection object.
        poll_id (str): The ID of the poll to connect to.
    """
    await manager.connect(poll_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
    
    except WebSocketDisconnect:
        manager.disconnect(poll_id, websocket)

@app.get("/", response_class=HTMLResponse)
async def get():
    """
    Render the main HTML page for the polling application.

    This endpoint serves the main page of the application, which contains 
    the user interface for creating and participating in polls.

    Returns:
        HTMLResponse: The HTML content of the main page.
    """
    with open("app/static/index.html") as f:
        return HTMLResponse(content=f.read())
