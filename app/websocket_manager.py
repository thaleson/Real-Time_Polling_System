# app/websocket_manager.py

from typing import List, Dict
from fastapi import WebSocket

class ConnectionManager:
    """
    Manages WebSocket connections for polls.

    Attributes:
        active_connections (Dict[str, List[WebSocket]]): A dictionary where the key is the poll_id
            and the value is a list of WebSocket connections associated with that poll.
    """
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, poll_id: str, websocket: WebSocket):
        """
        Accept a new WebSocket connection and add it to the active connections.

        Args:
            poll_id (str): The identifier for the poll.
            websocket (WebSocket): The WebSocket connection to be added.
        """
        await websocket.accept()
        if poll_id not in self.active_connections:
            self.active_connections[poll_id] = []
        self.active_connections[poll_id].append(websocket)

    def disconnect(self, poll_id: str, websocket: WebSocket):
        """
        Disconnect a WebSocket connection from the active connections.

        Args:
            poll_id (str): The identifier for the poll.
            websocket (WebSocket): The WebSocket connection to be removed.
        """
        self.active_connections[poll_id].remove(websocket)
        if not self.active_connections[poll_id]:
            del self.active_connections[poll_id]

    async def broadcast(self, poll_id: str, message: dict):
        """
        Broadcast a message to all WebSocket connections associated with a poll.

        Args:
            poll_id (str): The identifier for the poll.
            message (dict): The message to be sent to connected clients.
        """
        if poll_id in self.active_connections:
            for connection in self.active_connections[poll_id]:
                await connection.send_json(message)

manager = ConnectionManager()
