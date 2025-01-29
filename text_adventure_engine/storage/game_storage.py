import json
import yaml
import os
from typing import Dict, Optional
from datetime import datetime

class GameStorage:
    def __init__(self, game_dir: str):
        """Initialize storage with game directory path."""
        self.game_dir = game_dir
        self.config_dir = os.path.join(game_dir, "config")
        self.saves_dir = os.path.join(game_dir, "saves")
        self.ensure_directories()

    def ensure_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        os.makedirs(self.config_dir, exist_ok=True)
        os.makedirs(self.saves_dir, exist_ok=True)

    def load_game_config(self) -> Dict:
        """Load game configuration from YAML file."""
        config_path = os.path.join(self.config_dir, "game_config.yaml")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Game configuration not found at {config_path}")

    def load_npc_configs(self) -> Dict:
        """Load NPC configurations from YAML files."""
        npc_config_path = os.path.join(self.config_dir, "npcs")
        npcs = {}
        
        if not os.path.exists(npc_config_path):
            return npcs

        for filename in os.listdir(npc_config_path):
            if filename.endswith('.yaml'):
                with open(os.path.join(npc_config_path, filename), 'r', encoding='utf-8') as f:
                    npc_data = yaml.safe_load(f)
                    npcs[npc_data['id']] = npc_data
        
        return npcs

    def load_scene_configs(self) -> Dict:
        """Load scene configurations from YAML files."""
        scene_config_path = os.path.join(self.config_dir, "scenes")
        scenes = {}
        
        if not os.path.exists(scene_config_path):
            return scenes

        for filename in os.listdir(scene_config_path):
            if filename.endswith('.yaml'):
                with open(os.path.join(scene_config_path, filename), 'r', encoding='utf-8') as f:
                    scene_data = yaml.safe_load(f)
                    scenes[scene_data['id']] = scene_data
        
        return scenes

    def save_game_state(self, save_name: str, game_state: Dict, npc_states: Dict) -> str:
        """Save current game state and NPC states to a JSON file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"{save_name}_{timestamp}.json"
        save_path = os.path.join(self.saves_dir, save_filename)

        save_data = {
            "timestamp": timestamp,
            "game_state": game_state,
            "npc_states": npc_states
        }

        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        return save_filename

    def load_game_save(self, save_filename: str) -> Optional[Dict]:
        """Load a game save file."""
        save_path = os.path.join(self.saves_dir, save_filename)
        try:
            with open(save_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return None

    def list_save_files(self) -> list:
        """List all available save files."""
        saves = []
        for filename in os.listdir(self.saves_dir):
            if filename.endswith('.json'):
                save_path = os.path.join(self.saves_dir, filename)
                with open(save_path, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
                    saves.append({
                        "filename": filename,
                        "timestamp": save_data["timestamp"]
                    })
        return sorted(saves, key=lambda x: x["timestamp"], reverse=True)

    def create_default_config(self) -> None:
        """Create default configuration files if they don't exist."""
        default_game_config = {
            "game_name": "New Adventure",
            "initial_scene": "start_room",
            "game_version": "1.0.0"
        }

        default_scene = {
            "id": "start_room",
            "name": "Starting Room",
            "description": "A simple room where your adventure begins.",
            "items": {},
            "connected_scenes": [],
            "npcs": []
        }

        default_npc = {
            "id": "guide",
            "name": "Guide",
            "personality": "Helpful and friendly",
            "background": "A mysterious figure who helps new adventurers."
        }

        # Create game config
        os.makedirs(self.config_dir, exist_ok=True)
        game_config_path = os.path.join(self.config_dir, "game_config.yaml")
        if not os.path.exists(game_config_path):
            with open(game_config_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_game_config, f)

        # Create scenes directory and default scene
        scenes_dir = os.path.join(self.config_dir, "scenes")
        os.makedirs(scenes_dir, exist_ok=True)
        scene_path = os.path.join(scenes_dir, "start_room.yaml")
        if not os.path.exists(scene_path):
            with open(scene_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_scene, f)

        # Create NPCs directory and default NPC
        npcs_dir = os.path.join(self.config_dir, "npcs")
        os.makedirs(npcs_dir, exist_ok=True)
        npc_path = os.path.join(npcs_dir, "guide.yaml")
        if not os.path.exists(npc_path):
            with open(npc_path, 'w', encoding='utf-8') as f:
                yaml.dump(default_npc, f)