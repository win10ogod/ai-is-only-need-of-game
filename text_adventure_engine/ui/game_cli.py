import os
import asyncio
from typing import Dict, List, Optional
from ..core.game_world import GameWorld, Event, EventType
from ..npc.npc_manager import NPCManager
from ..storage.game_storage import GameStorage

class GameCLI:
    def __init__(self, game_dir: str, openai_api_key: str):
        """Initialize the game CLI interface."""
        self.storage = GameStorage(game_dir)
        self.world = GameWorld()
        self.npc_manager = NPCManager(openai_api_key)
        self.running = False
        self.available_commands = {
            "look": self.cmd_look,
            "inventory": self.cmd_inventory,
            "take": self.cmd_take,
            "drop": self.cmd_drop,
            "go": self.cmd_go,
            "talk": self.cmd_talk,
            "save": self.cmd_save,
            "load": self.cmd_load,
            "help": self.cmd_help,
            "quit": self.cmd_quit
        }

    async def initialize_game(self) -> None:
        """Initialize the game world and NPCs from configuration."""
        try:
            # Load configurations
            game_config = self.storage.load_game_config()
            scene_configs = self.storage.load_scene_configs()
            npc_configs = self.storage.load_npc_configs()

            # Initialize scenes
            for scene_data in scene_configs.values():
                self.world.add_scene(scene_data)

            # Set initial scene
            initial_scene = game_config.get("initial_scene")
            if initial_scene:
                self.world.change_scene(initial_scene)

            # Initialize NPCs
            for npc_data in npc_configs.values():
                self.npc_manager.create_npc(
                    npc_data["id"],
                    npc_data["name"],
                    npc_data["personality"],
                    npc_data["background"]
                )

        except FileNotFoundError:
            print("Creating default game configuration...")
            self.storage.create_default_config()
            await self.initialize_game()

    def display(self, text: str) -> None:
        """Display text to the user with proper formatting."""
        print("\n" + "="*80)
        print(text.strip())
        print("="*80)

    async def cmd_look(self, args: List[str]) -> None:
        """Display current scene description."""
        self.display(self.world.get_scene_description())

    async def cmd_inventory(self, args: List[str]) -> None:
        """Display player's inventory."""
        if not self.world.inventory:
            self.display("Your inventory is empty.")
            return

        inventory_text = "Inventory:\n"
        for item in self.world.inventory.values():
            inventory_text += f"- {item.name}: {item.description}\n"
        self.display(inventory_text)

    async def cmd_take(self, args: List[str]) -> None:
        """Take an item from the current scene."""
        if not args:
            self.display("What do you want to take?")
            return

        item_name = " ".join(args)
        current_scene = self.world.current_scene
        for item_id, item in current_scene.items.items():
            if item.name.lower() == item_name.lower():
                if self.world.add_to_inventory(item):
                    del current_scene.items[item_id]
                    self.display(f"You took the {item.name}.")
                    return
                else:
                    self.display(f"You can't take the {item.name}.")
                    return

        self.display(f"There is no {item_name} here.")

    async def cmd_drop(self, args: List[str]) -> None:
        """Drop an item from inventory."""
        if not args:
            self.display("What do you want to drop?")
            return

        item_name = " ".join(args)
        for item_id, item in self.world.inventory.items():
            if item.name.lower() == item_name.lower():
                self.world.current_scene.items[item_id] = item
                self.world.remove_from_inventory(item_id)
                self.display(f"You dropped the {item.name}.")
                return

        self.display(f"You don't have a {item_name}.")

    async def cmd_go(self, args: List[str]) -> None:
        """Move to a connected scene."""
        if not args:
            self.display("Where do you want to go?")
            return

        destination = " ".join(args)
        for scene_id in self.world.current_scene.connected_scenes:
            scene = self.world.scenes[scene_id]
            if scene.name.lower() == destination.lower():
                if self.world.change_scene(scene_id):
                    await self.cmd_look([])
                    return

        self.display(f"You can't go to {destination}.")

    async def cmd_talk(self, args: List[str]) -> None:
        """Talk to an NPC."""
        if not args:
            self.display("Who do you want to talk to?")
            return

        npc_name = args[0]
        dialog = " ".join(args[1:]) if len(args) > 1 else "Hello"

        # Check if NPC is in current scene
        if npc_name.lower() not in [npc.lower() for npc in self.world.current_scene.npcs]:
            self.display(f"{npc_name} is not here.")
            return

        try:
            response = await self.npc_manager.get_response(npc_name, dialog)
            self.display(f"{npc_name}: {response}")
        except Exception as e:
            self.display(f"Error talking to {npc_name}: {str(e)}")

    async def cmd_save(self, args: List[str]) -> None:
        """Save the current game state."""
        save_name = "_".join(args) if args else "quicksave"
        game_state = self.world.save_game_state()
        npc_states = {
            npc_id: self.npc_manager.save_npc_state(npc_id)
            for npc_id in self.npc_manager.npcs
        }
        
        save_file = self.storage.save_game_state(save_name, game_state, npc_states)
        self.display(f"Game saved as: {save_file}")

    async def cmd_load(self, args: List[str]) -> None:
        """Load a saved game state."""
        if not args:
            saves = self.storage.list_save_files()
            if not saves:
                self.display("No save files found.")
                return
            
            save_list = "Available saves:\n"
            for save in saves:
                save_list += f"- {save['filename']} ({save['timestamp']})\n"
            self.display(save_list)
            return

        save_file = " ".join(args)
        save_data = self.storage.load_game_save(save_file)
        
        if not save_data:
            self.display(f"Save file '{save_file}' not found.")
            return

        self.world.load_game_state(save_data["game_state"])
        for npc_id, npc_state in save_data["npc_states"].items():
            self.npc_manager.load_npc_state(npc_state)

        self.display("Game loaded successfully.")
        await self.cmd_look([])

    async def cmd_help(self, args: List[str]) -> None:
        """Display available commands."""
        help_text = "Available commands:\n"
        help_text += "- look: Look around the current scene\n"
        help_text += "- inventory: Check your inventory\n"
        help_text += "- take [item]: Take an item\n"
        help_text += "- drop [item]: Drop an item\n"
        help_text += "- go [place]: Go to a connected scene\n"
        help_text += "- talk [npc] [message]: Talk to an NPC\n"
        help_text += "- save [name]: Save the game\n"
        help_text += "- load [file]: Load a saved game\n"
        help_text += "- help: Show this help message\n"
        help_text += "- quit: Exit the game"
        self.display(help_text)

    async def cmd_quit(self, args: List[str]) -> None:
        """Quit the game."""
        self.running = False
        self.display("Thanks for playing!")

    async def process_command(self, command: str) -> None:
        """Process a user command."""
        parts = command.lower().strip().split()
        if not parts:
            return

        cmd = parts[0]
        args = parts[1:]

        if cmd in self.available_commands:
            await self.available_commands[cmd](args)
        else:
            self.display(f"Unknown command: {cmd}\nType 'help' for available commands.")

    async def run(self) -> None:
        """Main game loop."""
        await self.initialize_game()
        
        self.display("Welcome to the Text Adventure Engine!")
        await self.cmd_look([])
        
        self.running = True
        while self.running:
            try:
                command = input("\n> ").strip()
                await self.process_command(command)
            except KeyboardInterrupt:
                await self.cmd_quit([])
            except Exception as e:
                self.display(f"Error: {str(e)}")