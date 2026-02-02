<div align="center">

<!-- Red-White Indonesian Flag Colors Banner -->
<img src="https://img.shields.io/badge/MADE%20IN-INDONESIA-red?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAxMDAgNjAiPjxyZWN0IHdpZHRoPSIxMDAiIGhlaWdodD0iMzAiIGZpbGw9IiNmZmZmZmYiLz48cmVjdCB5PSIzMCIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIzMCIgZmlsbD0iI2ZmMDAwMCIvPjwvc3ZnPg==&logoColor=white&labelColor=white&color=red" alt="Made in Indonesia"/>

<!-- Animated DONGOL Logo -->
<h1>
  <span style="color: #ff0000;">D</span>
  <span style="color: #ffffff; background-color: #ff0000; padding: 0 5px;">O</span>
  <span style="color: #ff0000;">N</span>
  <span style="color: #ffffff; background-color: #ff0000; padding: 0 5px;">G</span>
  <span style="color: #ff0000;">O</span>
  <span style="color: #ffffff; background-color: #ff0000; padding: 0 5px;">L</span>
</h1>

**Distributed Orchestration for Navigating Goals and Operational Logic**

<p>
  <a href="docs/id/README.md">🇮🇩 Bahasa Indonesia</a> | 
  <a href="docs/en/README.md">🇬🇧 English</a> | 
  <a href="docs/jp/README.md">🇯🇵 日本語</a>
</p>

<!-- Badges -->
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Tests](https://img.shields.io/github/workflow/status/dongol-org/dongol/Tests?style=flat-square&label=Tests&logo=github)](https://github.com/dongol-org/dongol/actions)
[![Coverage](https://img.shields.io/codecov/c/github/dongol-org/dongol?style=flat-square&label=Coverage)](https://codecov.io/gh/dongol-org/dongol)
[![PyPI](https://img.shields.io/pypi/v/dongol?style=flat-square&label=PyPI)](https://pypi.org/project/dongol)
[![Downloads](https://img.shields.io/pypi/dm/dongol?style=flat-square&label=Downloads)](https://pypi.org/project/dongol)
[![Discord](https://img.shields.io/discord/123456789?style=flat-square&label=Discord&logo=discord&color=7289DA)](https://discord.gg/dongol)

<!-- Tagline -->
<h3><i>"Think Parallel. Execute Faster. 🇮🇩"</i></h3>
<p>Created with ❤️ in Indonesia by <b>Ardellio Satria Anindito</b> (SMA Kartika XIX-1 Bandung)</p>

<!-- Banner Image -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/banner-dark.png">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/banner-light.png">
  <img alt="DONGOL Banner" src="docs/assets/banner-light.png" width="800">
</picture>

</div>

---

## 🚀 Quick Start

### Installation

```bash
# Via pip (Recommended)
pip install dongol

# With all features
pip install dongol[all]

# From source
git clone https://github.com/dongol-org/dongol.git
cd dongol
pip install -e ".[all]"

# Using Docker
docker pull dongol/dongol:latest
docker run -it dongol/dongol
```

### First Steps

```bash
# Analyze your code project
dongol analyze ./my-project

# Parallel processing of tasks
dongol think "Optimize this database query" --parallel

# Chunk large files
dongol chunk large-file.txt --size 1000

# Check system status
dongol status
```

### Python API

```python
import asyncio
from dongol import DongolEngine

async def main():
    # Initialize
    engine = await DongolEngine.create()
    
    # Create parallel task
    task = await engine.create_task(
        name="Process Data",
        content="Large dataset...",
        auto_chunk=True,
        parallel=True
    )
    
    # Execute
    result = await engine.execute_task(task.id)
    print(f"Completed in {result.duration_ms:.2f}ms")

asyncio.run(main())
```

---

## 📊 Performance

| Metric | Sequential | DONGOL | Speedup |
|--------|-----------|--------|---------|
| **Task Creation** | - | 48,713/s | **5x target** |
| **File Processing** | 43.7/s | 196.5/s | **4.5x** |
| **Throughput** | 365 MB/s | 1,644 MB/s | **4.5x** |
| **Latency** | - | <1ms | **✓** |

> Tested on 2,979 real files (23.12 GB) from D:\ drive

---

## ✨ Features

- 🚀 **Parallel Thinking Matrix** - Execute multiple thought streams simultaneously
- 🧩 **Intelligent Chunking** - Smart decomposition with dependency tracking
- 🤖 **Agent-Native** - Built for AI agent workflows (MCP compatible)
- ⚡ **Zero-Latency Design** - Sub-millisecond task creation
- 🌐 **Universal Interface** - CLI, REST API, WebSocket, Python SDK
- 🇮🇩 **Made in Indonesia** - Created by Indonesian student for the world

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  🖥️ UNIVERSAL INTERFACE                                      │
│  CLI • REST API • WebSocket • SDK • Web UI                  │
├─────────────────────────────────────────────────────────────┤
│  ⚙️ UNIFIED CORE ENGINE                                     │
│  Async Event Loop • Task Scheduler • State Machine          │
├─────────────────────────────────────────────────────────────┤
│  🔄 PARALLEL PROCESSING LAYER                               │
│  Thinker Matrix • Chunking Engine • Context Memory          │
├─────────────────────────────────────────────────────────────┤
│  💾 PERSISTENCE LAYER                                       │
│  SQLite • Sled • File System • Cloud                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation

| Language | Link |
|----------|------|
| 🇬🇧 English | [docs/en/](docs/en/) |
| 🇮🇩 Bahasa Indonesia | [docs/id/](docs/id/) |
| 🇯🇵 日本語 | [docs/jp/](docs/jp/) |

### Quick Links

- [Installation Guide](docs/en/installation.md)
- [Quick Start Tutorial](docs/en/quickstart.md)
- [API Reference](docs/en/api.md)
- [Architecture Guide](docs/en/architecture.md)
- [Contributing](CONTRIBUTING.md)

---

## 🌏 Community

Join our growing community:

- 💬 [Discord](https://discord.gg/dongol) - Chat with contributors
- 🐦 [Twitter](https://twitter.com/dongol_io) - Updates and announcements
- 📧 [Email](mailto:contact@dongol.io) - Contact the team
- 🌐 [Website](https://dongol.io) - Official website

### Indonesian Tech Communities

- 🇮🇩 [Python Indonesia](https://t.me/pythonid) - Telegram group
- 🇮🇩 [Surabaya Tech](https://www.meetup.com/surabaya-tech/) - Local meetups
- 🇮🇩 [Bandung Tech](https://www.meetup.com/bandung-tech/) - Local meetups

---

## 🤝 Contributing

We welcome contributions from everyone!

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/dongol.git
cd dongol

# Setup
pip install -e ".[dev]"
pre-commit install

# Make changes and test
pytest tests/ -v

# Submit PR
git push origin feature/your-feature
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

**Special thanks to all contributors!**

<a href="https://github.com/dongol-org/dongol/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=dongol-org/dongol" />
</a>

---

## 📖 Citation

If you use DONGOL in your research, please cite:

```bibtex
@software{dongol2024,
  author = {Anindito, Ardellio Satria},
  title = {DONGOL: Distributed Orchestration for Navigating Goals},
  year = {2024},
  school = {SMA Kartika XIX-1 Bandung},
  address = {Indonesia},
  url = {https://github.com/dongol-org/dongol}
}
```

---

## 📜 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file.

```
MIT License
Copyright (c) 2024-2025 Ardellio Satria Anindito & DONGOL Contributors
Made in Indonesia 🇮🇩
```

---

## 🙏 Acknowledgments

- **Python Indonesia Community** - For inspiration and support
- **SMA Kartika XIX-1 Bandung** - For educational foundation
- **Surabaya & Bandung Tech Communities** - For local support
- **All Contributors** - For making this project better

---

<div align="center">

**[⬆ Back to Top](#-quick-start)**

*Made with ❤️ and ☕ in Indonesia*

🇮🇩 🇮🇩 🇮🇩

</div>
