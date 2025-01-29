import os
import asyncio
from dotenv import load_dotenv
from text_adventure_engine.npc.npc_manager import NPCManager

async def test_memory_system():
    """Test the memory system with a sample conversation."""
    print("測試記憶系統啟動中...\n")
    
    # Load environment variables
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    
    if not openai_api_key:
        print("錯誤: 請確保 .env 文件中包含 OPENAI_API_KEY")
        return
    
    # Initialize NPC Manager
    npc_manager = NPCManager(openai_api_key)
    
    # Create test NPC (Yuki)
    npc_manager.create_npc(
        "yuki",
        "優希",
        "溫柔但有主見的藝術系學生",
        "在咖啡廳打工的大學生，夢想是成為插畫家"
    )
    
    # Test conversations
    conversations = [
        {
            "input": "你好，我是新來的客人",
            "desc": "初次見面對話",
            "context": "在咖啡廳初次見面"
        },
        
        {
            "input": "最近在畫什麼作品嗎？",
            "desc": "詢問藝術創作",
            "context": "注意到優希的素描本"
        },
        
        {
            "input": "還記得昨天說的那幅畫嗎？",
            "desc": "測試記憶連貫性",
            "context": "第二次造訪咖啡廳"
        },
        
        {
            "input": "對於未來的藝術事業有什麼計劃？",
            "desc": "深入對話",
            "context": "在咖啡廳安靜的角落"
        },
        
        {
            "input": "上次你提到想辦畫展的事情考慮得怎麼樣了？",
            "desc": "回顧先前對話",
            "context": "在美術館偶遇"
        }
    ]
    
    print("開始對話測試...\n")
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n=== 測試 {i}: {conv['desc']} ===")
        print(f"場景: {conv['context']}")
        print(f"玩家: {conv['input']}")
        
        try:
            response = await npc_manager.get_response("yuki", conv['input'])
            print(f"優希: {response}\n")
            
            # Add a small delay between conversations to simulate time passing
            if i < len(conversations):
                print("...時間流逝...\n")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"錯誤: {str(e)}\n")
            continue
    
    print("""
記憶系統測試完成！

觀察要點：
----------
1. 短期記憶：
   - 保存最近的對話內容
   - 影響即時對話的連貫性

2. 長期記憶：
   - 自動儲存重要的對話內容
   - 根據重要性評分決定是否保存
   - 影響後續對話的深度

3. 記憶整合：
   - 自動在對話中引用過去的重要記憶
   - 創造更自然的對話流程
   - 展現角色的個性發展

提示：
-----
1. 你可以修改 conversations 列表來測試不同的對話場景
2. 觀察 NPC 如何記住並引用之前的對話
3. 注意對話的連貫性和個性化程度

要深入了解記憶系統的工作原理，可以查看 npc_manager.py 中的實現細節。
""")

if __name__ == "__main__":
    asyncio.run(test_memory_system())