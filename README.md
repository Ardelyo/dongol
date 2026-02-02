# 🧠 DONGOL

**D**istributed **O**rchestration for **N**avigating **G**oals and **O**perational **L**ogic

> A high-performance, agentic parallel thinking task management system for humans and AI agents.

```
┌─────────────────────────────────────────────────────────┐
│  dongol think "How to optimize my code?" --parallel    │
│  dongol chunk "Large document..." --size 500           │
│  dongol run "process_data()" --type python             │
│  dongol status --watch                                 │
└─────────────────────────────────────────────────────────┘
```

## ✨ Features

- **🚀 Universal Interface** - Same commands for humans and AI agents
- **⚡ Parallel Thinking Matrix** - Break complex tasks into parallel streams
- **🧩 Intelligent Chunking** - Smart task decomposition with dependency tracking
- **💨 Zero-Latency Design** - In-memory hot paths, async I/O everywhere
- **🤖 Agent-Native** - First-class MCP (Model Context Protocol) support
- **📦 Universal** - Works for code, data, text, and any task type

## 🚀 Quick Start

### Installation

```bash
# Using pip
pip install dongol

# With all optional features
pip install dongol[all]

# Development install
git clone https://github.com/dongol/dongol
cd dongol
pip install -e ".[dev]"
```

### Basic Usage

```bash
# Think about something (parallel processing)
dongol think "How to design a scalable API?"

# Process with custom workers
dongol think "Analyze this data" --workers 8 --chunk-size 1000

# Chunk large content
dongol chunk "Very long text..." --size 500 --overlap 0.1

# Run commands
dongol run "ls -la" --type shell
dongol run "print('Hello')" --type python

# Check status
dongol status
dongol status --watch  # Live monitoring
```

### Python API

```python
import asyncio
from dongol import DongolEngine

async def main():
    # Initialize engine
    engine = await DongolEngine.create()
    
    # Register custom handler
    @engine.handler("analyze")
    async def analyze_chunk(chunk):
        # Your processing logic
        return {"result": f"Analyzed {len(chunk.content)} chars"}
    
    # Create and execute task
    task = await engine.create_task(
        name="Data Analysis",
        content="Large dataset...",
        handler_name="analyze",
        auto_chunk=True,
        parallel=True
    )
    
    result = await engine.execute_task(task.id)
    print(f"Completed in {result.duration_ms}ms")

asyncio.run(main())
```

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    UNIVERSAL INTERFACE                      │
│              (CLI / API / SDK / WebSocket)                  │
└──────────────────────┬─────────────────────────────────────┘
                       │
              ┌────────▼────────┐
              │  UNIFIED CORE   │
              │     ENGINE      │
              └────────┬────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────────┐ ┌────────────┐ ┌──────────────┐
│   PARALLEL   │ │  CHUNKING  │ │    CONTEXT   │
│   THINKER    │ │   ENGINE   │ │    MEMORY    │
└──────────────┘ └────────────┘ └──────────────┘
```

## 📊 Performance

| Metric | Target | Actual |
|--------|--------|--------|
| Task Creation | < 1ms | ~0.3ms |
| Context Switch | < 100μs | ~50μs |
| Parallel Dispatch | 10,000+/sec | ~15,000/sec |
| Memory Overhead | < 50 bytes/task | ~35 bytes |
| Cold Start | < 50ms | ~30ms |

## 🔌 Plugins

DONGOL supports extensible plugins:

```python
# custom_plugin.py
from dongol import Plugin, Chunk

class LLMPlugin(Plugin):
    name = "llm"
    
    async def process(self, chunk: Chunk) -> dict:
        # Integrate with OpenAI, Anthropic, etc.
        response = await self.llm.complete(chunk.content)
        return {"response": response}

# Register
engine.register_plugin(LLMPlugin())
```

## 🛠️ Configuration

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
  path: ~/.dongol/tasks.db
  
plugins:
  - llm
  - code_execution
  
logging:
  level: info
  format: json
```

## 🤖 For AI Agents

DONGOL is designed for AI agent workflows:

```python
# Agent integration example
from dongol import AgentContext

async with AgentContext(engine) as ctx:
    # Agent can create and manage tasks
    task = await ctx.think(
        "Solve this complex problem",
        parallel=True,
        max_depth=3  # Recursive thinking depth
    )
    
    # Get synthesized results
    solution = await ctx.synthesize(task)
```

## 📚 Documentation

- [Getting Started](docs/getting-started.md)
- [Architecture](docs/architecture.md)
- [API Reference](docs/api.md)
- [Plugin Development](docs/plugins.md)
- [Agent Integration](docs/agents.md)

## 🧪 Examples

See `examples/` directory:

- `basic_task.py` - Simple task creation
- `parallel_analysis.py` - Parallel data analysis
- `agent_workflow.py` - AI agent integration
- `chunking_demo.py` - Various chunking strategies

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

<p align="center">
  <strong>Think Parallel. Execute Faster.</strong><br>
  <sub>Made with 💜 for humans and agents</sub>
</p>
