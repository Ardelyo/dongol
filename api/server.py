#!/usr/bin/env python3
"""
DONGOL API Server
REST API and WebSocket interface for remote access
"""
import asyncio
import json
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Task, Chunk, TaskStatus, Priority


# Pydantic models for API
class TaskCreateRequest(BaseModel):
    name: str
    content: str
    description: str = ""
    auto_chunk: bool = True
    chunk_size: int = 500
    priority: str = "NORMAL"
    parallel: bool = True
    max_workers: int = 4


class TaskResponse(BaseModel):
    id: str
    name: str
    description: str
    status: str
    priority: str
    created_at: float
    started_at: Optional[float]
    completed_at: Optional[float]
    duration_ms: Optional[float]
    chunk_count: int


class SystemStats(BaseModel):
    total_tasks: int
    total_chunks: int
    status_distribution: Dict[str, int]
    avg_chunks_per_task: float
    engine_running: bool


# Global engine instance
_engine: Optional[DongolEngine] = None


async def get_engine() -> DongolEngine:
    """Get or create global engine"""
    global _engine
    if _engine is None:
        _engine = DongolEngine()
        await _engine.start()
    return _engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan"""
    engine = await get_engine()
    
    def default_handler(chunk: Chunk) -> Dict:
        return {
            "chunk_id": chunk.id,
            "processed": True,
            "timestamp": asyncio.get_event_loop().time()
        }
    engine.register_handler("default", default_handler)
    
    yield
    
    if _engine:
        await _engine.stop()


app = FastAPI(
    title="DONGOL API",
    description="Distributed Orchestration for Navigating Goals and Operational Logic",
    version="0.1.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """API info"""
    return {
        "name": "DONGOL API",
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/stats", response_model=SystemStats)
async def get_stats():
    """Get system statistics"""
    engine = await get_engine()
    stats = engine.get_stats()
    return SystemStats(**stats)


@app.post("/tasks", response_model=TaskResponse)
async def create_task(request: TaskCreateRequest):
    """Create a new task"""
    engine = await get_engine()
    
    try:
        priority = Priority[request.priority.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid priority: {request.priority}")
    
    task = await engine.create_task(
        name=request.name,
        content=request.content,
        description=request.description,
        auto_chunk=request.auto_chunk,
        chunk_size=request.chunk_size,
        priority=priority,
        parallel=request.parallel,
        max_workers=request.max_workers
    )
    
    return TaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        status=task.status.name,
        priority=task.priority.name,
        created_at=task.created_at,
        started_at=task.started_at,
        completed_at=task.completed_at,
        duration_ms=task.duration_ms,
        chunk_count=len(task.chunks)
    )


@app.get("/tasks", response_model=List[TaskResponse])
async def list_tasks(status: Optional[str] = None, limit: int = 100, offset: int = 0):
    """List all tasks"""
    engine = await get_engine()
    tasks = list(engine.tasks.values())
    
    if status:
        tasks = [t for t in tasks if t.status.name.lower() == status.lower()]
    
    tasks = tasks[offset:offset + limit]
    
    return [
        TaskResponse(
            id=t.id, name=t.name, description=t.description,
            status=t.status.name, priority=t.priority.name,
            created_at=t.created_at, started_at=t.started_at,
            completed_at=t.completed_at, duration_ms=t.duration_ms,
            chunk_count=len(t.chunks)
        )
        for t in tasks
    ]


@app.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task details"""
    engine = await get_engine()
    
    if task_id not in engine.tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    task = engine.tasks[task_id]
    return TaskResponse(
        id=task.id, name=t.name, description=t.description,
        status=t.status.name, priority=t.priority.name,
        created_at=t.created_at, started_at=t.started_at,
        completed_at=t.completed_at, duration_ms=t.duration_ms,
        chunk_count=len(t.chunks)
    )


@app.post("/tasks/{task_id}/execute")
async def execute_task(task_id: str, handler: str = "default"):
    """Execute a task"""
    engine = await get_engine()
    
    if task_id not in engine.tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    task = await engine.execute_task(task_id, handler)
    
    return {
        "task_id": task.id,
        "status": task.status.name,
        "duration_ms": task.duration_ms,
        "results": task.results
    }


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    engine = await get_engine()
    
    if task_id not in engine.tasks:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    
    del engine.tasks[task_id]
    return {"message": f"Task {task_id} deleted"}


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time task updates"""
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            command = message.get("command")
            
            if command == "ping":
                await websocket.send_json({"type": "pong"})
            elif command == "get_stats":
                engine = await get_engine()
                stats = engine.get_stats()
                await websocket.send_json({"type": "stats", "data": stats})
            else:
                await websocket.send_json({"type": "error", "message": f"Unknown command: {command}"})
    except WebSocketDisconnect:
        manager.disconnect(websocket)


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
