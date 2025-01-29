# Love Adventure Project

本项目包含两个主要部分：

1. `text_adventure_engine/` - 通用文字冒險遊戲引擎
2. `dating_game/` - 基於引擎開發的戀愛遊戲

## 目錄結構

```
love_adventure_project/
├── text_adventure_engine/    # 遊戲引擎
│   ├── core/                # 核心功能
│   ├── npc/                # NPC管理
│   ├── storage/            # 存儲系統
│   └── ui/                 # 用戶界面
│
└── dating_game/            # 戀愛遊戲
    ├── config/             # 遊戲配置
    ├── saves/             # 存檔目錄
    └── logs/              # 日誌目錄
```

## 安裝步驟

1. 安裝依賴：
```bash
pip install -r requirements.txt
```

2. 設置 OpenAI API：
在 `dating_game/.env` 中添加你的 API 金鑰：
```
OPENAI_API_KEY=your_api_key_here
```

3. 運行遊戲：
```bash
cd dating_game
python setup.py
python -m text_adventure_engine --game-dir .
```

更多詳細信息請參考各個目錄下的 README.md 文件。