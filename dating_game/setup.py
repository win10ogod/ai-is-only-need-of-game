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
            f.write("# Add your OpenAI API key here\n")
            f.write("OPENAI_API_KEY=your_api_key_here\n")
    
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
遊戲使用兩層記憶系統：

1. 短期記憶：
   - 保存最近10次對話
   - 用於維持對話連貫性
   - 動態更新

2. 長期記憶：
   - 儲存重要事件和對話
   - 根據AI分析（重要性>=0.7）自動保存
   - 影響角色關係發展

記憶系統完全在本地運作，無需額外服務。
所有記憶都會保存在遊戲存檔中。

更多資訊請參考 README.md
""")

if __name__ == "__main__":
    setup_game()