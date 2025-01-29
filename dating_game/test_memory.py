import os
import asyncio
from dotenv import load_dotenv
from text_adventure_engine.npc.npc_manager import NPCManager

async def test_memory_system():
    """Test the in-memory system with examples of short-term and long-term memories."""
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
    
    # Test conversations demonstrating memory system
    conversations = [
        # 1. 初次見面 - 基本對話
        {
            "input": "你好，我是新來的客人，可以幫我推薦咖啡嗎？",
            "desc": "初次見面對話",
            "note": "這會儲存在短期記憶中"
        },
        
        # 2. 觀察到她的興趣
        {
            "input": "我注意到你在忙的時候會畫畫，是在準備什麼作品嗎？",
            "desc": "關於藝術創作的對話",
            "note": "因為涉及她的重要興趣，可能會被存為長期記憶"
        },
        
        # 3. 引用之前的對話
        {
            "input": "上次你提到的那幅畫完成了嗎？我很期待看到成品。",
            "desc": "測試記憶連貫性",
            "note": "測試NPC是否記得之前的對話"
        },
        
        # 4. 分享個人經歷
        {
            "input": "我最近去了美術館的新展覽，讓我想到你說過的創作理念。",
            "desc": "建立更深的連接",
            "note": "可能觸發重要的長期記憶存儲"
        },
        
        # 5. 觸及感情話題
        {
            "input": "你知道嗎，每次看到你專注創作的樣子，都讓我感到很特別。",
            "desc": "表達更深的感情",
            "note": "重要的情感互動，應該會存入長期記憶"
        }
    ]
    
    print("開始對話測試...\n")
    
    for i, conv in enumerate(conversations, 1):
        print(f"\n=== 測試 {i}: {conv['desc']} ===")
        print(f"測試重點: {conv['note']}")
        print(f"玩家: {conv['input']}")
        
        try:
            response = await npc_manager.get_response("yuki", conv['input'])
            print(f"優希: {response}\n")
            
            # 顯示記憶狀態
            npc = npc_manager.npcs["yuki"]
            print(f"短期記憶數量: {len(npc.short_term_memory)}")
            print(f"長期記憶數量: {len(npc.long_term_memory)}")
            
            if npc.long_term_memory:
                print("\n最新的長期記憶:")
                latest_memory = npc.long_term_memory[-1]
                print(f"內容: {latest_memory.content}")
                print(f"重要性: {latest_memory.importance}")
                print(f"時間: {latest_memory.timestamp}")
            
            # Add a small delay between conversations
            if i < len(conversations):
                print("\n...時間流逝...\n")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"錯誤: {str(e)}\n")
            continue
    
    print("""
記憶系統測試完成！

測試結果說明：
-------------
1. 短期記憶特點：
   - 保存最近的對話內容（最多10條）
   - 自動更新，保持對話連貫性
   - 用於即時反應和上下文理解

2. 長期記憶特點：
   - 只保存重要性>=0.7的內容
   - 包含時間戳記和重要性評分
   - 用於建立持久的角色關係

3. 記憶整合效果：
   - NPC能自然引用之前的對話
   - 記憶影響對話的語氣和親密度
   - 創造連貫的角色發展

提示：實際遊戲中，記憶系統會根據：
1. 對話內容的重要性
2. 情感互動的深度
3. 事件的特殊性
自動決定哪些內容需要長期保存。

你可以通過不同的對話主題和互動方式來測試記憶系統的效果。
""")

if __name__ == "__main__":
    asyncio.run(test_memory_system())