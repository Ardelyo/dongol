# DONGOL Quick Start Guide

Get up and running with DONGOL in 5 minutes.

## Installation

### Option 1: Direct Install (Windows PowerShell)
```powershell
Invoke-RestMethod https://code.kimi.com/install.ps1 | Invoke-Expression
```

### Option 2: From Source
```bash
git clone https://github.com/dongol/dongol
cd dongol
pip install -e ".[all]"
```

### Option 3: pip (when published)
```bash
pip install dongol
```

## Verify Installation

```bash
dongol --help
dongol status
```

## Basic Usage

### 1. Parallel Thinking

```bash
# Think about a problem in parallel
dongol think "How to optimize a slow database query?"

# With custom settings
dongol think "Design a microservices architecture" \
    --workers 8 \
    --chunk-size 1000 \
    --parallel
```

### 2. Intelligent Chunking

```bash
# Chunk large text
dongol chunk "Very long text content..." --size 500 --overlap 0.1

# Chunk structured data
dongol chunk '{"users": [...]}' --by structure

# Save chunks to file
dongol chunk document.txt --size 200 --output chunks.json
```

### 3. Execute Tasks

```bash
# Run shell command
dongol run "ls -la" --type shell

# Run Python code
dongol run "print(sum(range(100)))" --type python

# With environment variables
dongol run "echo $GREETING" --type shell --env GREETING=Hello
```

### 4. Monitor System

```bash
# Check status
dongol status

# Watch mode (live updates)
dongol status --watch

# JSON output for scripting
dongol status --json-output
```

## Python API

### Basic Example

```python
import asyncio
from dongol import DongolEngine

async def main():
    # Initialize
    engine = DongolEngine()
    await engine.start()
    
    # Register custom handler
    def my_handler(chunk):
        return f"Processed: {chunk.content[:50]}"
    
    engine.register_handler("my_handler", my_handler)
    
    # Create task
    task = await engine.create_task(
        name="My Task",
        content="Content to process...",
        handler_name="my_handler",
        auto_chunk=True
    )
    
    # Execute
    result = await engine.execute_task(task.id)
    print(f"Completed in {result.duration_ms:.2f}ms")
    print(result.results)
    
    # Cleanup
    await engine.stop()

asyncio.run(main())
```

### Parallel Processing Example

```python
async def parallel_analysis():
    engine = DongolEngine({'max_workers': 8})
    await engine.start()
    
    # Process multiple items in parallel
    items = ["item1", "item2", "item3", "item4"]
    
    async def process_item(chunk):
        await asyncio.sleep(0.1)  # Simulate work
        return {"item": chunk.content, "processed": True}
    
    engine.register_handler("process", process_item)
    
    task = await engine.create_task(
        name="Batch Processing",
        content="\n".join(items),
        auto_chunk=True,
        parallel=True
    )
    
    result = await engine.execute_task(task.id, "process")
    
    for chunk_id, res in result.results.items():
        print(f"{chunk_id}: {res}")
    
    await engine.stop()
```

## Agent Integration

### Using with AI Agents

```python
from dongol import DongolEngine, Priority

class MyAgent:
    def __init__(self):
        self.engine = DongolEngine()
    
    async def think_parallel(self, problem: str) -> dict:
        """Multi-perspective analysis"""
        
        perspectives = ["technical", "business", "security", "user"]
        
        async def analyze(chunk):
            perspective = chunk.content
            # Your LLM call here
            return {
                "perspective": perspective,
                "analysis": f"Analysis from {perspective} view..."
            }
        
        self.engine.register_handler("analyze", analyze)
        
        task = await self.engine.create_task(
            name=f"Analyze: {problem[:30]}",
            content="\n".join(perspectives),
            auto_chunk=True,
            parallel=True
        )
        
        result = await self.engine.execute_task(task.id, "analyze")
        
        # Synthesize results
        return {
            "problem": problem,
            "perspectives": result.results,
            "synthesis": self.merge_analyses(result.results)
        }
```

## REST API Server

### Start the Server

```bash
# Start API server
cd dongol/api
python server.py

# Or with uvicorn
uvicorn api.server:app --reload --port 8000
```

### API Examples

```bash
# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "name": "API Test",
    "content": "Test content",
    "parallel": true,
    "max_workers": 4
  }'

# Execute task
curl -X POST http://localhost:8000/tasks/{task_id}/execute

# Get stats
curl http://localhost:8000/stats

# List tasks
curl "http://localhost:8000/tasks?limit=10"
```

## Configuration

Create `~/.dongol/config.yaml`:

```yaml
engine:
  max_workers: 8
  use_processes: false

chunking:
  max_chunk_size: 1000
  overlap_ratio: 0.1

storage:
  backend: sqlite
  path: ~/.dongol/data

logging:
  level: info
```

## Common Patterns

### Pattern 1: Batch Processing Pipeline

```python
async def batch_pipeline(items: list):
    engine = await DongolEngine.create()
    
    # Step 1: Chunk
    task = await engine.create_task(
        name="Batch",
        content="\n".join(str(i) for i in items),
        auto_chunk=True,
        chunk_size=100
    )
    
    # Step 2: Process in parallel
    result = await engine.execute_task(task.id)
    
    # Step 3: Aggregate
    return aggregate_results(result.results)
```

### Pattern 2: Recursive Task Decomposition

```python
async def recursive_solve(problem: str, depth: int = 2):
    if depth == 0:
        return await solve_leaf(problem)
    
    # Decompose
    sub_problems = await decompose(problem)
    
    # Solve sub-problems in parallel
    results = await asyncio.gather(*[
        recursive_solve(sub, depth - 1)
        for sub in sub_problems
    ])
    
    # Merge
    return merge_results(results)
```

### Pattern 3: Real-time Monitoring

```python
async def monitor_tasks():
    engine = await DongolEngine.create()
    
    while True:
        stats = engine.get_stats()
        print(f"Tasks: {stats['total_tasks']}, "
              f"Running: {stats['status_distribution'].get('RUNNING', 0)}")
        await asyncio.sleep(5)
```

## Troubleshooting

### Issue: Command not found
```bash
# Ensure dongol is in PATH
which dongol

# Or use python module
python -m dongol
```

### Issue: Import error
```bash
# Reinstall in development mode
pip install -e ".[all]"
```

### Issue: Performance issues
```yaml
# ~/.dongol/config.yaml
engine:
  max_workers: 16  # Increase workers
  use_processes: true  # For CPU-bound tasks

chunking:
  token_limit: 2000  # Larger chunks = less overhead
```

## Next Steps

- Read [CONCEPT.md](CONCEPT.md) for detailed architecture
- Check [examples/](examples/) for more code samples
- Review [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- Run tests: `make test`

---

**Happy Parallel Thinking!** 🧠
