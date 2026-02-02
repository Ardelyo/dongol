"""
DONGOL Core Engine - High-Performance Task Orchestration
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import time
import uuid
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Coroutine, Dict, Generic, List, Optional, Set, TypeVar, Union
import heapq

T = TypeVar('T')


class TaskStatus(Enum):
    PENDING = auto()
    RUNNING = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELLED = auto()


class Priority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass
class Chunk:
    """Intelligent task chunk with metadata"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    content: Any = None
    parent_id: Optional[str] = None
    dependencies: Set[str] = field(default_factory=set)
    priority: Priority = Priority.NORMAL
    estimated_duration_ms: int = 1000
    tags: Set[str] = field(default_factory=set)
    context: Dict[str, Any] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'content': self.content,
            'parent_id': self.parent_id,
            'dependencies': list(self.dependencies),
            'priority': self.priority.name,
            'estimated_duration_ms': self.estimated_duration_ms,
            'tags': list(self.tags),
            'context': self.context,
            'created_at': self.created_at
        }


@dataclass
class Task:
    """Main task container with parallel execution support"""
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:12])
    name: str = "unnamed"
    description: str = ""
    chunks: List[Chunk] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    priority: Priority = Priority.NORMAL
    created_at: float = field(default_factory=time.time)
    started_at: Optional[float] = None
    completed_at: Optional[float] = None
    results: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parallel_mode: bool = True
    max_workers: int = 4
    
    @property
    def duration_ms(self) -> Optional[float]:
        if self.started_at and self.completed_at:
            return (self.completed_at - self.started_at) * 1000
        return None


class ChunkingEngine:
    """
    Intelligent task chunking with dependency analysis
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.max_chunk_size = self.config.get('max_chunk_size', 1000)
        self.min_chunk_size = self.config.get('min_chunk_size', 10)
        self.overlap_ratio = self.config.get('overlap_ratio', 0.1)
    
    def chunk_by_tokens(self, content: str, token_limit: int = 500) -> List[Chunk]:
        """Smart chunking that respects semantic boundaries"""
        words = content.split()
        chunks = []
        current_chunk = []
        current_tokens = 0
        
        for word in words:
            word_tokens = len(word) // 4 + 1  # Rough estimate
            
            if current_tokens + word_tokens > token_limit and current_chunk:
                chunks.append(Chunk(
                    content=' '.join(current_chunk),
                    tags={'auto_chunked', 'token_based'}
                ))
                # Keep overlap for context
                overlap_start = max(0, len(current_chunk) - int(len(current_chunk) * self.overlap_ratio))
                current_chunk = current_chunk[overlap_start:]
                current_tokens = sum(len(w) // 4 + 1 for w in current_chunk)
            
            current_chunk.append(word)
            current_tokens += word_tokens
        
        if current_chunk:
            chunks.append(Chunk(
                content=' '.join(current_chunk),
                tags={'auto_chunked', 'token_based'}
            ))
        
        # Link dependencies
        for i, chunk in enumerate(chunks):
            chunk.parent_id = f"batch_{hash(content) % 10000}"
            if i > 0:
                chunk.dependencies.add(chunks[i-1].id)
        
        return chunks
    
    def chunk_by_structure(self, data: Dict[str, Any]) -> List[Chunk]:
        """Chunk structured data intelligently"""
        chunks = []
        
        def extract_chunks(obj: Any, path: str = ""):
            if isinstance(obj, dict):
                for key, value in obj.items():
                    new_path = f"{path}.{key}" if path else key
                    if isinstance(value, (dict, list)) and len(str(value)) > self.max_chunk_size:
                        extract_chunks(value, new_path)
                    else:
                        chunks.append(Chunk(
                            content={'path': new_path, 'value': value},
                            tags={'structured', 'auto_chunked'},
                            context={'path': new_path}
                        ))
            elif isinstance(obj, list):
                for i, item in enumerate(obj):
                    new_path = f"{path}[{i}]"
                    if isinstance(item, (dict, list)) and len(str(item)) > self.max_chunk_size:
                        extract_chunks(item, new_path)
                    else:
                        chunks.append(Chunk(
                            content={'path': new_path, 'value': item},
                            tags={'structured', 'auto_chunked'},
                            context={'path': new_path, 'index': i}
                        ))
        
        extract_chunks(data)
        return chunks
    
    def analyze_dependencies(self, chunks: List[Chunk]) -> Dict[str, Set[str]]:
        """Analyze and optimize chunk dependencies"""
        dependency_graph = defaultdict(set)
        
        for chunk in chunks:
            dependency_graph[chunk.id] = chunk.dependencies
        
        # Detect cycles and resolve
        visited = set()
        temp_mark = set()
        
        def has_cycle(node: str) -> bool:
            if node in temp_mark:
                return True
            if node in visited:
                return False
            temp_mark.add(node)
            for dep in dependency_graph[node]:
                if has_cycle(dep):
                    return True
            temp_mark.remove(node)
            visited.add(node)
            return False
        
        # Remove cycles by breaking least important edges
        for chunk in chunks:
            if has_cycle(chunk.id):
                # Remove last dependency to break cycle
                if chunk.dependencies:
                    chunk.dependencies.pop()
        
        return dict(dependency_graph)


class ParallelExecutor:
    """
    High-performance parallel task executor
    """
    
    def __init__(self, max_workers: int = 4, use_processes: bool = False):
        self.max_workers = max_workers
        self.use_processes = use_processes
        self._executor: Optional[Union[ThreadPoolExecutor, ProcessPoolExecutor]] = None
        self._lock = asyncio.Lock()
        self._active_tasks: Dict[str, asyncio.Task] = {}
    
    async def start(self):
        if self.use_processes:
            self._executor = ProcessPoolExecutor(max_workers=self.max_workers)
        else:
            self._executor = ThreadPoolExecutor(max_workers=self.max_workers)
    
    async def stop(self):
        if self._executor:
            self._executor.shutdown(wait=True)
            self._executor = None
    
    async def execute_chunk(
        self, 
        chunk: Chunk, 
        handler: Callable[[Chunk], T],
        dependency_results: Dict[str, T]
    ) -> T:
        """Execute a single chunk with dependency injection"""
        # Inject dependency results into context
        chunk.context['dependencies'] = dependency_results
        
        loop = asyncio.get_event_loop()
        
        if self.use_processes:
            # Use process pool for CPU-bound tasks
            result = await loop.run_in_executor(self._executor, handler, chunk)
        else:
            # Use thread pool for I/O-bound tasks
            if asyncio.iscoroutinefunction(handler):
                result = await handler(chunk)
            else:
                result = await loop.run_in_executor(self._executor, handler, chunk)
        
        return result
    
    async def execute_parallel(
        self,
        chunks: List[Chunk],
        handler: Callable[[Chunk], T],
        dependency_graph: Optional[Dict[str, Set[str]]] = None
    ) -> Dict[str, T]:
        """Execute chunks in parallel respecting dependencies"""
        results: Dict[str, T] = {}
        completed: Set[str] = set()
        chunk_map = {c.id: c for c in chunks}
        
        async def can_execute(chunk: Chunk) -> bool:
            return chunk.dependencies.issubset(completed)
        
        async def execute_with_deps(chunk: Chunk):
            dep_results = {
                dep_id: results[dep_id] 
                for dep_id in chunk.dependencies 
                if dep_id in results
            }
            result = await self.execute_chunk(chunk, handler, dep_results)
            results[chunk.id] = result
            completed.add(chunk.id)
            return result
        
        # Topological sort with parallel execution
        remaining = set(c.id for c in chunks)
        
        while remaining:
            executable = [
                chunk_map[cid] for cid in remaining 
                if await can_execute(chunk_map[cid])
            ]
            
            if not executable:
                # Deadlock detected, break by executing first remaining
                executable = [chunk_map[list(remaining)[0]]]
            
            # Execute batch in parallel
            batch_tasks = [
                asyncio.create_task(execute_with_deps(chunk))
                for chunk in executable
            ]
            
            await asyncio.gather(*batch_tasks, return_exceptions=True)
            remaining -= set(c.id for c in executable)
        
        return results


class DongolEngine:
    """
    Main DONGOL Engine - Universal Task Orchestrator
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.chunking = ChunkingEngine(self.config.get('chunking', {}))
        self.executor = ParallelExecutor(
            max_workers=self.config.get('max_workers', 4),
            use_processes=self.config.get('use_processes', False)
        )
        self.tasks: Dict[str, Task] = {}
        self._handlers: Dict[str, Callable] = {}
        self._running = False
        self._event_queue: asyncio.Queue = asyncio.Queue()
    
    async def start(self):
        """Initialize the engine"""
        await self.executor.start()
        self._running = True
        asyncio.create_task(self._event_loop())
    
    async def stop(self):
        """Shutdown the engine"""
        self._running = False
        await self.executor.stop()
    
    async def _event_loop(self):
        """Background event processing"""
        while self._running:
            try:
                event = await asyncio.wait_for(self._event_queue.get(), timeout=0.1)
                await self._process_event(event)
            except asyncio.TimeoutError:
                continue
    
    async def _process_event(self, event: Dict[str, Any]):
        """Process system events"""
        event_type = event.get('type')
        if event_type == 'task_complete':
            task_id = event.get('task_id')
            if task_id in self.tasks:
                self.tasks[task_id].status = TaskStatus.COMPLETED
                self.tasks[task_id].completed_at = time.time()
    
    def register_handler(self, name: str, handler: Callable[[Chunk], Any]):
        """Register a chunk handler"""
        self._handlers[name] = handler
    
    async def create_task(
        self,
        name: str,
        content: Any,
        handler_name: str = "default",
        auto_chunk: bool = True,
        **options
    ) -> Task:
        """Create and optionally chunk a new task"""
        task = Task(
            name=name,
            description=options.get('description', ''),
            priority=Priority(options.get('priority', 2)),
            parallel_mode=options.get('parallel', True),
            max_workers=options.get('max_workers', 4)
        )
        
        if auto_chunk and isinstance(content, str):
            task.chunks = self.chunking.chunk_by_tokens(
                content, 
                token_limit=options.get('chunk_size', 500)
            )
        elif auto_chunk and isinstance(content, dict):
            task.chunks = self.chunking.chunk_by_structure(content)
        else:
            task.chunks = [Chunk(content=content, tags={'single'})]
        
        # Analyze dependencies
        self.chunking.analyze_dependencies(task.chunks)
        
        self.tasks[task.id] = task
        return task
    
    async def execute_task(self, task_id: str, handler_name: str = "default") -> Task:
        """Execute a task with parallel chunk processing"""
        if task_id not in self.tasks:
            raise ValueError(f"Task {task_id} not found")
        
        task = self.tasks[task_id]
        handler = self._handlers.get(handler_name, self._default_handler)
        
        task.status = TaskStatus.RUNNING
        task.started_at = time.time()
        
        if task.parallel_mode and len(task.chunks) > 1:
            # Execute chunks in parallel
            dependency_graph = {
                c.id: c.dependencies for c in task.chunks
            }
            results = await self.executor.execute_parallel(
                task.chunks, handler, dependency_graph
            )
        else:
            # Sequential execution
            results = {}
            for chunk in task.chunks:
                result = await self.executor.execute_chunk(chunk, handler, results)
                results[chunk.id] = result
        
        task.results = results
        task.status = TaskStatus.COMPLETED
        task.completed_at = time.time()
        
        # Notify completion
        await self._event_queue.put({
            'type': 'task_complete',
            'task_id': task_id,
            'timestamp': time.time()
        })
        
        return task
    
    def _default_handler(self, chunk: Chunk) -> Any:
        """Default chunk handler - override for custom logic"""
        return {
            'chunk_id': chunk.id,
            'processed': True,
            'content_preview': str(chunk.content)[:100] if chunk.content else None,
            'timestamp': time.time()
        }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get engine statistics"""
        total_tasks = len(self.tasks)
        status_counts = defaultdict(int)
        total_chunks = 0
        
        for task in self.tasks.values():
            status_counts[task.status.name] += 1
            total_chunks += len(task.chunks)
        
        return {
            'total_tasks': total_tasks,
            'total_chunks': total_chunks,
            'status_distribution': dict(status_counts),
            'avg_chunks_per_task': total_chunks / total_tasks if total_tasks > 0 else 0,
            'engine_running': self._running
        }


# Singleton instance
_engine: Optional[DongolEngine] = None


async def get_engine(config: Optional[Dict] = None) -> DongolEngine:
    """Get or create global engine instance"""
    global _engine
    if _engine is None:
        _engine = DongolEngine(config)
        await _engine.start()
    return _engine
