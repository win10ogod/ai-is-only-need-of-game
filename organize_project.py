import os
import shutil
from pathlib import Path

def create_directory_structure():
    """Create the project directory structure and move files to their proper locations."""
    project_root = Path(__file__).parent
    
    # Define directory structure
    directories = [
        "text_adventure_engine/core",
        "text_adventure_engine/npc",
        "text_adventure_engine/storage",
        "text_adventure_engine/ui",
        "dating_game/config/npcs",
        "dating_game/config/scenes",
        "dating_game/config/events",
        "dating_game/config/prompts",
        "dating_game/saves",
        "dating_game/logs"
    ]
    
    # Create directories
    for directory in directories:
        os.makedirs(project_root / directory, exist_ok=True)
    
    # Move engine files
    engine_files = {
        "core/game_world.py": "text_adventure_engine/core/",
        "npc/npc_manager.py": "text_adventure_engine/npc/",
        "storage/game_storage.py": "text_adventure_engine/storage/",
        "ui/game_cli.py": "text_adventure_engine/ui/",
        "main.py": "text_adventure_engine/",
        "__init__.py": "text_adventure_engine/"
    }
    
    base_engine_path = project_root.parent / "text_adventure_engine"
    if base_engine_path.exists():
        for src, dest in engine_files.items():
            src_path = base_engine_path / src
            if src_path.exists():
                shutil.copy2(src_path, project_root / dest)
    
    # Move game files
    game_files = {
        "config/game_config.yaml": "dating_game/config/",
        "config/npcs/yuki.yaml": "dating_game/config/npcs/",
        "config/scenes/cafe.yaml": "dating_game/config/scenes/",
        "config/scenes/park.yaml": "dating_game/config/scenes/",
        "config/scenes/art_gallery.yaml": "dating_game/config/scenes/",
        "config/events/yuki_events.yaml": "dating_game/config/events/",
        "config/prompts/yuki_prompt.yaml": "dating_game/config/prompts/",
        "setup.py": "dating_game/",
        "README.md": "dating_game/"
    }
    
    base_game_path = project_root.parent / "dating_game"
    if base_game_path.exists():
        for src, dest in game_files.items():
            src_path = base_game_path / src
            if src_path.exists():
                shutil.copy2(src_path, project_root / dest)

    # Create __init__.py files for Python packages
    init_locations = [
        "text_adventure_engine/core",
        "text_adventure_engine/npc",
        "text_adventure_engine/storage",
        "text_adventure_engine/ui"
    ]
    
    for location in init_locations:
        init_file = project_root / location / "__init__.py"
        if not init_file.exists():
            init_file.touch()

    print("""
專案重組完成！

目錄結構已建立：
love_adventure_project/
├── text_adventure_engine/    # 遊戲引擎
│   ├── core/
│   ├── npc/
│   ├── storage/
│   └── ui/
└── dating_game/            # 戀愛遊戲
    ├── config/
    ├── saves/
    └── logs/

請檢查所有文件是否已正確移動到新的位置。
    """)

if __name__ == "__main__":
    create_directory_structure()