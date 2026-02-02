"""
DONGOL Core Engine

High-performance task orchestration with parallel execution.
"""

from .engine import (
    DongolEngine,
    ChunkingEngine,
    ParallelExecutor,
    Task,
    Chunk,
    TaskStatus,
    Priority,
    get_engine,
)

__all__ = [
    "DongolEngine",
    "ChunkingEngine",
    "ParallelExecutor", 
    "Task",
    "Chunk",
    "TaskStatus",
    "Priority",
    "get_engine",
]
