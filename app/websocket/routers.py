from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager
import json

router = APIRouter()

@router.websocket("/live")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        await manager.broadcast_event("CONNECTED", {
            "message": "IA CENTINELL live feed active",
            "connections": manager.connection_count
        })
        while True:
            data = await websocket.receive_text()
            try:
                await manager.broadcast(json.loads(data))
            except json.JSONDecodeError:
                await manager.broadcast({"event":"MESSAGE","data":{"text":data}})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
