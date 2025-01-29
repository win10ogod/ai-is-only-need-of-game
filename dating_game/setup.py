import os
import shutil
from pathlib import Path

def setup_game():
    """Setup the dating game environment."""
    base_dir = Path(__file__).parent
    
    # Create necessary directories
    directories = [
        "saves",
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(base_dir / directory, exist_ok=True)
    
    # Create .env file template if it doesn't exist
    env_file = base_dir / ".env"
    if not env_file.exists():
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("# OpenAI API Configuration\n")
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n\n")
            f.write("# Optional custom OpenAI API base URL\n")
            f.write("#OPENAI_API_BASE=http://your-custom-openai-endpoint\n")
    
    print("""
戀愛冒險 - Dating Adventure
===========================

遊戲環境設置完成！

開始遊戲前請確保：

1. 安裝必要套件：
   pip install -r requirements.txt

2. 設置 OpenAI API：
   在 .env 檔案中填入你的 API 金鑰：
   OPENAI_API_KEY=your_api_key_here

3. 啟動遊戲：
   python -m text_adventure_engine --game-dir .

記憶系統說明：
-------------
- NPC 擁有短期和長期記憶系統
- 重要的對話會自動儲存為長期記憶
- 記憶會影響對話的連貫性和個性化
- 系統會自動管理記憶的重要性

更多資訊請參考 README.md
""")

if __name__ == "__main__":
    setup_game()