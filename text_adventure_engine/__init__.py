"""
Text Adventure Engine
A modular text adventure game engine with AI-powered NPCs.
"""

from .core.game_world import GameWorld, Event, EventType, Scene, Item
from .npc.npc_manager import NPCManager
from .storage.game_storage import GameStorage
from .ui.game_cli import GameCLI

__version__ = '0.1.0'

__all__ = [
    'GameWorld',
    'Event',
    'EventType',
    'Scene',
    'Item',
    'NPCManager',
    'GameStorage',
    'GameCLI'
]