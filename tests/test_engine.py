#!/usr/bin/env python3
"""
DONGOL Core Engine Tests
"""
import asyncio
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import (
    DongolEngine, ChunkingEngine, ParallelExecutor,
    Task, Chunk, TaskStatus, Priority
)


class TestChunkingEngine:
    """Test the chunking engine"""
    
    def test_chunk_by_tokens_basic(self):
        chunker = ChunkingEngine()
        text = "Hello world " * 100
        chunks = chunker.chunk_by_tokens(text, token_limit=50)
        
        assert len(chunks) > 0
        assert all(isinstance(c, Chunk) for c in chunks)
        assert all("auto_chunked" in c.tags for c in chunks)
    
    def test_chunk_with_dependencies(self):
        chunker = ChunkingEngine()
        text = "First part. Second part. Third part. " * 10
        chunks = chunker.chunk_by_tokens(text, token_limit=30)
        
        # Check that dependencies are set
        for i, chunk in enumerate(chunks):
            if i > 0:
                assert len(chunk.dependencies) > 0
    
    def test_chunk_by_structure(self):
        chunker = ChunkingEngine()
        data = {
            "users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
            "settings": {"theme": "dark", "notifications": True}
        }
        chunks = chunker.chunk_by_structure(data)
        
        assert len(chunks) > 0
        assert all(c.context.get('path') for c in chunks)
    
    def test_analyze_dependencies_no_cycle(self):
        chunker = ChunkingEngine()
        chunks = [
            Chunk(id="a", dependencies=set()),
            Chunk(id="b", dependencies={"a"}),
            Chunk(id="c", dependencies={"b"}),
        ]
        graph = chunker.analyze_dependencies(chunks)
        
        assert "c" in graph
        assert graph["c"] == {"b"}


class TestParallelExecutor:
    """Test parallel execution"""
    
    @pytest.mark.asyncio
    async def test_executor_start_stop(self):
        executor = ParallelExecutor(max_workers=2)
        await executor.start()
        assert executor._executor is not None
        await executor.stop()
        assert executor._executor is None
    
    @pytest.mark.asyncio
    async def test_execute_single_chunk(self):
        executor = ParallelExecutor(max_workers=2)
        await executor.start()
        
        def handler(chunk: Chunk) -> str:
            return f"processed_{chunk.id}"
        
        chunk = Chunk(id="test", content="hello")
        result = await executor.execute_chunk(chunk, handler, {})
        
        assert result == "processed_test"
        await executor.stop()
    
    @pytest.mark.asyncio
    async def test_execute_parallel_with_deps(self):
        executor = ParallelExecutor(max_workers=4)
        await executor.start()
        
        execution_order = []
        
        async def handler(chunk: Chunk) -> str:
            execution_order.append(chunk.id)
            return f"result_{chunk.id}"
        
        chunks = [
            Chunk(id="a", dependencies=set()),
            Chunk(id="b", dependencies={"a"}),
            Chunk(id="c", dependencies={"a"}),
            Chunk(id="d", dependencies={"b", "c"}),
        ]
        
        results = await executor.execute_parallel(chunks, handler)
        
        assert len(results) == 4
        assert "a" in execution_order[:1]  # 'a' should be first
        assert results["d"] == "result_d"
        
        await executor.stop()


class TestDongolEngine:
    """Test the main engine"""
    
    @pytest.mark.asyncio
    async def test_engine_start_stop(self):
        engine = DongolEngine()
        await engine.start()
        assert engine._running
        await engine.stop()
        assert not engine._running
    
    @pytest.mark.asyncio
    async def test_create_task(self):
        engine = DongolEngine()
        await engine.start()
        
        task = await engine.create_task(
            name="Test Task",
            content="Hello world",
            auto_chunk=False
        )
        
        assert task.name == "Test Task"
        assert len(task.chunks) == 1
        assert task.id in engine.tasks
        
        await engine.stop()
    
    @pytest.mark.asyncio
    async def test_execute_task(self):
        engine = DongolEngine()
        await engine.start()
        
        def handler(chunk: Chunk) -> dict:
            return {"content": chunk.content, "processed": True}
        
        engine.register_handler("test", handler)
        
        task = await engine.create_task(
            name="Execution Test",
            content="test data",
            auto_chunk=False
        )
        
        result = await engine.execute_task(task.id, "test")
        
        assert result.status == TaskStatus.COMPLETED
        assert result.duration_ms is not None
        assert len(result.results) == 1
        
        await engine.stop()
    
    @pytest.mark.asyncio
    async def test_auto_chunking(self):
        engine = DongolEngine()
        await engine.start()
        
        long_content = "Word " * 1000
        
        task = await engine.create_task(
            name="Chunked Task",
            content=long_content,
            auto_chunk=True,
            chunk_size=100
        )
        
        assert len(task.chunks) > 1
        
        await engine.stop()
    
    @pytest.mark.asyncio
    async def test_get_stats(self):
        engine = DongolEngine()
        await engine.start()
        
        # Create some tasks
        for i in range(3):
            await engine.create_task(
                name=f"Task {i}",
                content="test",
                auto_chunk=False
            )
        
        stats = engine.get_stats()
        
        assert stats['total_tasks'] == 3
        assert stats['engine_running']
        
        await engine.stop()


class TestTaskAndChunk:
    """Test data classes"""
    
    def test_task_creation(self):
        task = Task(name="Test", description="A test task")
        assert task.name == "Test"
        assert task.status == TaskStatus.PENDING
        assert task.id is not None
    
    def test_task_duration(self):
        import time
        task = Task()
        task.started_at = time.time()
        task.completed_at = time.time() + 1.0
        
        assert task.duration_ms is not None
        assert task.duration_ms >= 1000
    
    def test_chunk_to_dict(self):
        chunk = Chunk(
            id="test-123",
            content="hello",
            tags={"test", "demo"}
        )
        data = chunk.to_dict()
        
        assert data['id'] == "test-123"
        assert data['content'] == "hello"
        assert isinstance(data['tags'], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
