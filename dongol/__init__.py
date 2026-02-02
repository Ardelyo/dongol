"""
DONGOL - Distributed Orchestration for Navigating Goals and Operational Logic

A high-performance, agentic parallel thinking task management system.
Made in Indonesia 🇮🇩 by Ardellio Satria Anindito
SMA Kartika XIX-1 Bandung

Version: 0.1.0
"""

__version__ = "0.1.0"
__author__ = "Ardellio Satria Anindito"
__email__ = "contact@dongol.io"
__license__ = "MIT"
__copyright__ = "Copyright 2024-2025 Ardellio Satria Anindito & DONGOL Contributors"

# Country of origin
__country__ = "Indonesia"
__country_flag__ = "🇮🇩"

# School attribution
__school__ = "SMA Kartika XIX-1 Bandung"
__city__ = "Bandung"

__all__ = [
    "__version__",
    "__author__",
    "__country__",
    "__school__",
]

# Core exports
try:
    from .core.engine import (
        DongolEngine,
        ChunkingEngine,
        ParallelExecutor,
        Task,
        Chunk,
        TaskStatus,
        Priority,
        get_engine,
    )
    
    __all__.extend([
        "DongolEngine",
        "ChunkingEngine",
        "ParallelExecutor",
        "Task",
        "Chunk",
        "TaskStatus",
        "Priority",
        "get_engine",
    ])
except ImportError:
    pass


def get_info():
    """Get DONGOL package information."""
    return {
        "name": "DONGOL",
        "version": __version__,
        "author": __author__,
        "country": __country__,
        "flag": __country_flag__,
        "school": __school__,
        "license": __license__,
        "motto": "Think Parallel. Execute Faster.",
        "indonesian_motto": "Berpikir Paralel. Eksekusi Lebih Cepat.",
    }


def show_banner():
    """Show DONGOL banner."""
    banner = f"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   ██████   ██████  ███    ██  ██████   ██████               ║
║   ██   ██ ██    ██ ████   ██ ██       ██    ██              ║
║   ██   ██ ██    ██ ██ ██  ██ ██   ███ ██    ██              ║
║   ██   ██ ██    ██ ██  ██ ██ ██    ██ ██    ██              ║
║   ██████   ██████  ██   ████  ██████   ██████               ║
║                                                               ║
║              {__country_flag__} Made in {__country__}                              ║
║       Created by {__author__}                   ║
║       {__school__}                      ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
Version: {__version__} | License: {__license__}
    """
    print(banner)


# Version compatibility check
import sys

if sys.version_info < (3, 9):
    raise ImportError(
        f"DONGOL {__version__} requires Python 3.9+. "
        f"Current version: {sys.version_info.major}.{sys.version_info.minor}"
    )
