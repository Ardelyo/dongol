#!/usr/bin/env python3
"""
DONGOL Basic Usage Examples
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from core.engine import DongolEngine, Chunk, Priority


async def example_1_basic_task():
    """Example 1: Create and execute a basic task"""
    print("\n" + "="*50)
    print("Example 1: Basic Task Execution")
    print("="*50)
    
    engine = DongolEngine()
    await engine.start()
    
    # Define a simple handler
    def simple_handler(chunk: Chunk):
        return {
            "processed": str(chunk.content).upper(),
            "chunk_id": chunk.id
        }
    
    engine.register_handler("simple", simple_handler)
    
    # Create task
    task = await engine.create_task(
        name="Greeting Task",
        content="hello world from dongol",
        handler_name="simple",
        auto_chunk=True,
        chunk_size=20
    )
    
    print(f"Created task: {task.id}")
    print(f"Chunks: {len(task.chunks)}")
    
    # Execute
    result = await engine.execute_task(task.id, "simple")
    
    print(f"Status: {result.status.name}")
    print(f"Duration: {result.duration_ms:.2f}ms")
    print("Results:", result.results)
    
    await engine.stop()


async def example_2_parallel_processing():
    """Example 2: Parallel processing with dependencies"""
    print("\n" + "="*50)
    print("Example 2: Parallel Processing")
    print("="*50)
    
    engine = DongolEngine({'max_workers': 4})
    await engine.start()
    
    async def async_handler(chunk: Chunk):
        import random
        await asyncio.sleep(random.uniform(0.01, 0.05))  # Simulate work
        return {
            "chunk_id": chunk.id,
            "processed": f"Processed: {str(chunk.content)[:30]}...",
            "dependencies": list(chunk.dependencies)
        }
    
    engine.register_handler("async", async_handler)
    
    # Create a complex task that will be chunked
    large_content = " ".join([
        f"This is paragraph {i} with some content to process. " * 5
        for i in range(10)
    ])
    
    task = await engine.create_task(
        name="Parallel Analysis",
        content=large_content,
        handler_name="async",
        auto_chunk=True,
        chunk_size=200,
        parallel=True
    )
    
    print(f"Task split into {len(task.chunks)} chunks")
    
    # Show dependency graph
    for chunk in task.chunks:
        if chunk.dependencies:
            print(f"Chunk {chunk.id} depends on: {chunk.dependencies}")
    
    result = await engine.execute_task(task.id, "async")
    
    print(f"\nCompleted in {result.duration_ms:.2f}ms")
    print(f"Average per chunk: {result.duration_ms / len(task.chunks):.2f}ms")
    
    await engine.stop()


async def example_3_structured_data():
    """Example 3: Processing structured data"""
    print("\n" + "="*50)
    print("Example 3: Structured Data Chunking")
    print("="*50)
    
    engine = DongolEngine()
    await engine.start()
    
    def data_handler(chunk: Chunk):
        data = chunk.content
        return {
            "path": data.get('path', 'unknown'),
            "value_type": type(data.get('value')).__name__,
            "size": len(str(data.get('value')))
        }
    
    engine.register_handler("data", data_handler)
    
    # Complex nested data
    structured_data = {
        "users": [
            {"id": 1, "name": "Alice", "roles": ["admin", "user"]},
            {"id": 2, "name": "Bob", "roles": ["user"]},
        ],
        "settings": {
            "theme": "dark",
            "notifications": True,
            "features": {
                "beta": True,
                "experimental": ["feature_a", "feature_b"]
            }
        },
        "metadata": {
            "version": "1.0.0",
            "created": "2024-01-01"
        }
    }
    
    task = await engine.create_task(
        name="Data Processing",
        content=structured_data,
        handler_name="data",
        auto_chunk=True
    )
    
    print(f"Data split into {len(task.chunks)} chunks")
    
    for chunk in task.chunks:
        print(f"  - {chunk.context.get('path', 'root')}: {str(chunk.content)[:50]}...")
    
    result = await engine.execute_task(task.id, "data")
    
    print(f"\nProcessing results:")
    for chunk_id, res in result.results.items():
        print(f"  {chunk_id}: {res}")
    
    await engine.stop()


async def example_4_stats_and_monitoring():
    """Example 4: Engine statistics"""
    print("\n" + "="*50)
    print("Example 4: Statistics and Monitoring")
    print("="*50)
    
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    # Create multiple tasks
    for i in range(5):
        await engine.create_task(
            name=f"Batch Task {i}",
            content=f"Content for task {i} " * 50,
            auto_chunk=True,
            chunk_size=100
        )
    
    # Get stats
    stats = engine.get_stats()
    
    print("Engine Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    await engine.stop()


async def example_5_custom_chunking():
    """Example 5: Using the chunking engine directly"""
    print("\n" + "="*50)
    print("Example 5: Direct Chunking Engine Usage")
    print("="*50)
    
    from core.engine import ChunkingEngine
    
    chunker = ChunkingEngine({
        'max_chunk_size': 500,
        'overlap_ratio': 0.2
    })
    
    # Text chunking
    text = """
    DONGOL is designed for high-performance parallel task execution.
    It supports intelligent chunking, dependency tracking, and parallel processing.
    The system is optimized for both human and AI agent usage.
    """ * 10
    
    chunks = chunker.chunk_by_tokens(text, token_limit=100)
    
    print(f"Text split into {len(chunks)} chunks")
    for i, chunk in enumerate(chunks[:3], 1):  # Show first 3
        print(f"\nChunk {i} (ID: {chunk.id}):")
        print(f"  Content: {str(chunk.content)[:80]}...")
        print(f"  Dependencies: {chunk.dependencies}")
    
    if len(chunks) > 3:
        print(f"\n... and {len(chunks) - 3} more chunks")


async def main():
    """Run all examples"""
    print("🧠 DONGOL - Usage Examples")
    print("Running demonstration of core features...")
    
    await example_1_basic_task()
    await example_2_parallel_processing()
    await example_3_structured_data()
    await example_4_stats_and_monitoring()
    await example_5_custom_chunking()
    
    print("\n" + "="*50)
    print("All examples completed!")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())
