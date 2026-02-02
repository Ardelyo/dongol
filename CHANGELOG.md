# Changelog

All notable changes to DONGOL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2024-02-02

### 🎉 Initial Release

Made in Indonesia 🇮🇩 by Ardellio Satria Anindito (SMA Kartika XIX-1 Bandung)

### ✨ Features

#### Core Engine
- **Parallel Thinker Matrix** - Execute multiple thought streams simultaneously
- **Intelligent Chunking Engine** - Token-based, structure-based, and semantic chunking
- **Dependency Resolution** - Topological sort with automatic cycle detection
- **Context Memory System** - L1-L4 caching architecture
- **Zero-Latency Design** - Sub-millisecond task creation

#### Interfaces
- **CLI** - Rich terminal interface with progress bars and tables
- **REST API** - FastAPI-based with OpenAPI documentation
- **WebSocket** - Real-time updates for long-running tasks
- **Python SDK** - Type-hinted async API

#### Performance
- Task creation: 48,713 tasks/second
- Parallel speedup: 4.5x vs sequential
- Throughput: 1,644 MB/second
- Memory overhead: ~35 bytes per task

#### Real-World Testing
- Tested on 2,979 files (23.12 GB) from D:\ drive
- Successfully organized 1,455 files
- Validated on Windows, Linux, and macOS

### 📦 Installation Methods

```bash
# Via pip
pip install dongol

# With all features
pip install dongol[all]

# Using Docker
docker pull dongol/dongol:latest

# Using conda (coming soon)
conda install -c conda-forge dongol
```

### 🌏 Internationalization

- English (default)
- Bahasa Indonesia 🇮🇩
- 日本語 (Japanese) - Planned

### 📝 Documentation

- Comprehensive README in English and Indonesian
- API documentation with FastAPI
- Architecture diagrams
- Benchmark reports
- Real-world case studies

### 🤝 Community

- GitHub Discussions
- Discord server
- Twitter: @dongol_io
- Email: contact@dongol.io

### 🙏 Contributors

Special thanks to:
- Python Indonesia Community
- SMA Kartika XIX-1 Bandung
- Surabaya & Bandung Tech Communities

---

## [Unreleased]

### 🚧 Planned Features

- [ ] GUI Application (React/Electron)
- [ ] Distributed Mode (multi-node cluster)
- [ ] GPU Acceleration Support
- [ ] WebAssembly (WASM) Plugins
- [ ] Official MCP (Model Context Protocol) Integration
- [ ] Plugin Marketplace
- [ ] Cloud Storage Integration (S3, GCS, Azure)
- [ ] Kubernetes Operator
- [ ] Helm Charts

### 🔧 Improvements

- [ ] Persistent storage with SQLite/Sled
- [ ] Undo/Redo functionality
- [ ] Better error recovery
- [ ] More chunking strategies
- [ ] Performance optimizations

---

## Release Notes Format

Each release includes:
- 🎉 New Features
- 🚀 Performance Improvements
- 🐛 Bug Fixes
- 📚 Documentation Updates
- 🔧 Maintenance

---

*Made with ❤️ in Indonesia*
