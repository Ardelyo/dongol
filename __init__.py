"""
DONGOL - Distributed Orchestration for Navigating Goals and Operational Logic

A high-performance, agentic parallel thinking task management system.

Basic Usage:
    >>> import asyncio
    >>> from dongol import DongolEngine
    >>> 
    >>> async def main():
    ...     engine = await DongolEngine.create()
    ...     task = await engine.create_task("Hello", "World")
    ...     result = await engine.execute_task(task.id)
    ...     print(result.results)
    >>> 
    >>> asyncio.run(main())
"""

__version__ = "0.1.0"
__author__ = "DONGOL Team"

from core.engine import (
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
