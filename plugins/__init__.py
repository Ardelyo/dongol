"""
DONGOL Plugin System

Extensible plugin architecture for custom functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict
from core.engine import Chunk


class Plugin(ABC):
    """Base class for DONGOL plugins"""
    
    name: str = "base"
    version: str = "0.1.0"
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin"""
        pass
    
    @abstractmethod
    async def process(self, chunk: Chunk) -> Dict[str, Any]:
        """Process a chunk"""
        pass
    
    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup plugin resources"""
        pass


class PluginManager:
    """Manage DONGOL plugins"""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
    
    def register(self, plugin: Plugin) -> None:
        """Register a plugin"""
        self._plugins[plugin.name] = plugin
    
    def get(self, name: str) -> Plugin:
        """Get a plugin by name"""
        return self._plugins[name]
    
    def list_plugins(self) -> list:
        """List all registered plugins"""
        return list(self._plugins.keys())
    
    async def initialize_all(self) -> None:
        """Initialize all plugins"""
        for plugin in self._plugins.values():
            await plugin.initialize()
    
    async def shutdown_all(self) -> None:
        """Shutdown all plugins"""
        for plugin in self._plugins.values():
            await plugin.shutdown()


__all__ = ["Plugin", "PluginManager"]
