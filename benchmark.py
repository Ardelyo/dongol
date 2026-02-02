#!/usr/bin/env python3
"""
DONGOL Performance Benchmark
"""
import asyncio
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from core.engine import DongolEngine, Chunk


async def benchmark_task_creation():
    """Benchmark task creation speed"""
    print("\n" + "="*60)
    print("Benchmark: Task Creation")
    print("="*60)
    
    engine = DongolEngine()
    await engine.start()
    
    # Warmup
    for _ in range(10):
        await engine.create_task("Warmup", "test", auto_chunk=False)
    
    # Benchmark
    num_tasks = 1000
    start = time.perf_counter()
    
    for i in range(num_tasks):
        await engine.create_task(
            name=f"Benchmark Task {i}",
            content="Test content for benchmarking",
            auto_chunk=False
        )
    
    elapsed = time.perf_counter() - start
    avg_ms = (elapsed / num_tasks) * 1000
    
    print(f"Created {num_tasks} tasks in {elapsed:.3f}s")
    print(f"Average: {avg_ms:.3f}ms per task")
    print(f"Throughput: {num_tasks/elapsed:.0f} tasks/sec")
    
    await engine.stop()


async def benchmark_parallel_execution():
    """Benchmark parallel task execution"""
    print("\n" + "="*60)
    print("Benchmark: Parallel Execution")
    print("="*60)
    
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    async def fast_handler(chunk: Chunk):
        # Simulate some work
        await asyncio.sleep(0.001)
        return {"processed": True, "chunk_id": chunk.id}
    
    engine.register_handler("fast", fast_handler)
    
    # Create task with many chunks
    content = "Word " * 5000
    task = await engine.create_task(
        name="Parallel Benchmark",
        content=content,
        auto_chunk=True,
        chunk_size=100
    )
    
    print(f"Task split into {len(task.chunks)} chunks")
    
    # Execute and measure
    start = time.perf_counter()
    result = await engine.execute_task(task.id, "fast")
    elapsed = time.perf_counter() - start
    
    print(f"Executed {len(task.chunks)} chunks in {elapsed*1000:.2f}ms")
    print(f"Average per chunk: {(elapsed/len(task.chunks))*1000:.3f}ms")
    print(f"Parallel speedup: ~{len(task.chunks) * 0.001 / elapsed:.1f}x")
    
    await engine.stop()


async def benchmark_chunking():
    """Benchmark chunking performance"""
    print("\n" + "="*60)
    print("Benchmark: Intelligent Chunking")
    print("="*60)
    
    from core.engine import ChunkingEngine
    
    chunker = ChunkingEngine()
    
    # Generate test content
    text = "This is a sample sentence. " * 1000
    
    # Benchmark token-based chunking
    sizes = [100, 500, 1000]
    
    for size in sizes:
        start = time.perf_counter()
        chunks = chunker.chunk_by_tokens(text, token_limit=size)
        elapsed = time.perf_counter() - start
        
        print(f"Token limit {size}: {len(chunks)} chunks in {elapsed*1000:.2f}ms "
              f"({len(text)/elapsed/1000:.1f}KB/s)")


async def benchmark_structured_data():
    """Benchmark structured data processing"""
    print("\n" + "="*60)
    print("Benchmark: Structured Data Processing")
    print("="*60)
    
    engine = DongolEngine({'max_workers': 4})
    await engine.start()
    
    def data_handler(chunk: Chunk):
        data = chunk.content
        return {
            "path": data.get('path'),
            "processed": True
        }
    
    engine.register_handler("data", data_handler)
    
    # Create large nested structure
    data = {
        f"section_{i}": {
            f"item_{j}": f"value_{i}_{j}" * 10
            for j in range(50)
        }
        for i in range(20)
    }
    
    task = await engine.create_task(
        name="Structured Data",
        content=data,
        auto_chunk=True
    )
    
    print(f"Data split into {len(task.chunks)} chunks")
    
    start = time.perf_counter()
    result = await engine.execute_task(task.id, "data")
    elapsed = time.perf_counter() - start
    
    print(f"Processed in {elapsed*1000:.2f}ms")
    print(f"Throughput: {len(task.chunks)/elapsed:.0f} chunks/sec")
    
    await engine.stop()


async def main():
    print("="*60)
    print("DONGOL Performance Benchmark")
    print("="*60)
    
    await benchmark_task_creation()
    await benchmark_chunking()
    await benchmark_parallel_execution()
    await benchmark_structured_data()
    
    print("\n" + "="*60)
    print("Benchmark Complete!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
