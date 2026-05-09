from typing import List, Dict, Any
from fastapi import WebSocket
import json
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active:
            self.active.remove(ws)

    async def broadcast(self, message: Dict[str, Any]):
        payload = json.dumps({**message, "ts": datetime.utcnow().isoformat()})
        dead = []
        for ws in self.active:
            try:
                await ws.send_text(payload)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.disconnect(ws)

    async def broadcast_event(self, event_type: str, data: Dict[str, Any]):
        await self.broadcast({"event": event_type, "data": data})

    @property
    def connection_count(self) -> int:
        return len(self.active)

manager = ConnectionManager()
