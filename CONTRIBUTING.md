# Contributing to DONGOL 🇮🇩

Terima kasih (Thank you) for your interest in contributing to DONGOL! This document provides guidelines for contributing to this Made-in-Indonesia open source project.

## 🌟 Our Vision

DONGOL is built with Indonesian innovation for the world. We believe in:
- **Gotong Royong** (Collaboration) - Working together as a community
- **Bhinneka Tunggal Ika** (Unity in Diversity) - Welcoming contributors from all backgrounds
- **Keren** (Awesome) - Building something we can be proud of

## 🚀 Ways to Contribute

### 1. Report Bugs 🐛
If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Use the label `bug`

### 2. Suggest Features 💡
Have an idea? Create an issue with:
- Feature description
- Use cases
- Potential implementation approach
- Use the label `enhancement`

### 3. Write Code 💻

#### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/dongol-org/dongol.git
cd dongol

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

#### Development Workflow

1. **Fork and Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

2. **Make Changes**
   - Follow PEP 8 style guide
   - Add docstrings to functions/classes
   - Update tests if needed
   - Update documentation

3. **Test Your Changes**
   ```bash
   # Run tests
   pytest tests/ -v
   
   # Run with coverage
   pytest tests/ --cov=dongol --cov-report=html
   
   # Check code style
   ruff check dongol/
   black --check dongol/
   ```

4. **Commit**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   Commit message format:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation changes
   - `test:` Adding tests
   - `refactor:` Code refactoring
   - `perf:` Performance improvements
   - `chore:` Maintenance tasks

5. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a PR on GitHub.

### 4. Improve Documentation 📚

We welcome documentation improvements in both:
- **English** - `docs/en/`
- **Bahasa Indonesia** - `docs/id/`

### 5. Translate 🌐

Help us translate DONGOL to more languages:
- UI text in `dongol/i18n/`
- Documentation in `docs/`
- README files

### 6. Share and Promote 📢

- Star the repository ⭐
- Share on social media
- Write blog posts
- Give talks at local meetups

## 📝 Code Style Guidelines

### Python Code
- Follow **PEP 8**
- Use **type hints**
- Maximum line length: 100 characters
- Use **Black** for formatting
- Use **Ruff** for linting

```python
# Good example
from typing import List, Dict, Optional

async def process_chunks(
    chunks: List[Chunk],
    handler: Callable[[Chunk], T],
    max_workers: int = 4
) -> Dict[str, T]:
    """Process chunks in parallel.
    
    Args:
        chunks: List of chunks to process
        handler: Function to process each chunk
        max_workers: Maximum number of parallel workers
    
    Returns:
        Dictionary mapping chunk IDs to results
    """
    # Implementation here
    pass
```

### Documentation
- Use **Google-style** docstrings
- Update README if adding features
- Add examples for new functionality

### Tests
- Write tests for new features
- Maintain test coverage > 80%
- Use pytest fixtures
- Mock external services

## 🏷️ Issue Labels

| Label | Description | Bahasa Indonesia |
|-------|-------------|------------------|
| `bug` | Something isn't working | Ada yang rusak |
| `enhancement` | New feature request | Fitur baru |
| `documentation` | Docs improvements | Dokumentasi |
| `good first issue` | Good for beginners | Cocok untuk pemula |
| `help wanted` | Extra attention needed | Butuh bantuan |
| `performance` | Performance related | Performa |
| `indonesian` | Indonesia-specific | Terkait Indonesia |

## 🎨 Indonesian Cultural Elements

When contributing, feel free to include:
- **Indonesian language** support
- **Local examples** (Indonesian names, places)
- **Cultural references** that are globally understandable
- **Red-White** color scheme for UI elements

## 🙏 Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards others
- Embodying the spirit of *Gotong Royong*

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement
Violations may result in temporary or permanent ban from the project.

## 🌏 Local Communities

Join our Indonesian tech communities:
- **Python Indonesia** - @pythonid
- **Surabaya Tech** - Local meetup group
- **Bandung Tech** - Local meetup group

## 📞 Contact

- **Maintainer**: Ardellio Satria Anindito (SMA Kartika XIX-1 Bandung)
- **Email**: contact@dongol.io
- **Discord**: [Join our server](https://discord.gg/dongol)
- **Twitter**: [@dongol_io](https://twitter.com/dongol_io)

## 🎓 For Students

We especially welcome student contributors!
- High school projects are welcome
- University thesis integrations
- Coding competition implementations

Mention your school in your PR for a shoutout!

---

## FAQ

**Q: Do I need to speak Indonesian to contribute?**  
A: No! English is our primary language for code and documentation. But we appreciate Indonesian translations!

**Q: Can I use DONGOL for my school project?**  
A: Absolutely! We'd love to hear about it. Please share your project with us.

**Q: How do I get started?**  
A: Look for issues labeled `good first issue` or `help wanted`.

---

**Terima kasih banyak!** (Thank you very much!) 🙏

Let's build something amazing together!

*Made with ❤️ in Indonesia*
