from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum

class EventType(Enum):
    DIALOG = "dialog"
    ITEM_INTERACTION = "item_interaction"
    SCENE_CHANGE = "scene_change"
    CUSTOM = "custom"

@dataclass
class Item:
    id: str
    name: str
    description: str
    is_takeable: bool = False
    is_useable: bool = False
    state: Dict = field(default_factory=dict)

@dataclass
class Scene:
    id: str
    name: str
    description: str
    items: Dict[str, Item] = field(default_factory=dict)
    connected_scenes: List[str] = field(default_factory=list)
    npcs: List[str] = field(default_factory=list)
    state: Dict = field(default_factory=dict)

@dataclass
class Event:
    type: EventType
    source_id: str
    target_id: Optional[str] = None
    data: Dict = field(default_factory=dict)

class GameWorld:
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Optional[Scene] = None
        self.inventory: Dict[str, Item] = {}
        self.game_state: Dict = {}
        self.event_handlers: Dict[EventType, List[callable]] = {
            event_type: [] for event_type in EventType
        }

    def add_scene(self, scene: Scene) -> None:
        """Add a new scene to the game world."""
        self.scenes[scene.id] = scene

    def change_scene(self, scene_id: str) -> bool:
        """Change the current scene if it's connected to the current one."""
        if not self.current_scene:
            self.current_scene = self.scenes[scene_id]
            return True

        if scene_id in self.current_scene.connected_scenes:
            self.current_scene = self.scenes[scene_id]
            return True
        return False

    def add_to_inventory(self, item: Item) -> bool:
        """Add an item to player's inventory."""
        if item.is_takeable:
            self.inventory[item.id] = item
            return True
        return False

    def remove_from_inventory(self, item_id: str) -> Optional[Item]:
        """Remove an item from player's inventory."""
        return self.inventory.pop(item_id, None)

    def register_event_handler(self, event_type: EventType, handler: callable) -> None:
        """Register a new event handler for the specified event type."""
        self.event_handlers[event_type].append(handler)

    def trigger_event(self, event: Event) -> List[Dict]:
        """Trigger an event and collect responses from all registered handlers."""
        responses = []
        for handler in self.event_handlers[event.type]:
            response = handler(event)
            if response:
                responses.append(response)
        return responses

    def get_scene_description(self) -> str:
        """Get the description of the current scene."""
        if not self.current_scene:
            return "No current scene"

        desc = f"\n{self.current_scene.name}\n"
        desc += f"{self.current_scene.description}\n\n"

        if self.current_scene.items:
            desc += "Items in the room:\n"
            for item in self.current_scene.items.values():
                desc += f"- {item.name}: {item.description}\n"

        if self.current_scene.npcs:
            desc += "\nCharacters present:\n"
            for npc in self.current_scene.npcs:
                desc += f"- {npc}\n"

        return desc

    def save_game_state(self) -> Dict:
        """Return a dictionary containing the current game state."""
        return {
            "current_scene": self.current_scene.id if self.current_scene else None,
            "inventory": {item_id: vars(item) for item_id, item in self.inventory.items()},
            "game_state": self.game_state
        }

    def load_game_state(self, state: Dict) -> None:
        """Load a previously saved game state."""
        if state["current_scene"]:
            self.current_scene = self.scenes[state["current_scene"]]
        self.inventory = {
            item_id: Item(**item_data)
            for item_id, item_data in state["inventory"].items()
        }
        self.game_state = state["game_state"]