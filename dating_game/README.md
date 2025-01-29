# 戀愛冒險 - Dating Adventure

一個具有本地部署LLM和智能記憶系統的戀愛文字冒險遊戲。

## 本地服務架構

### 1. VLLM API 服務
- 支援多種大型語言模型（如 Llama 2、Mistral 等）
- 高效的批處理和推理
- 可自定義模型和參數

### 2. 本地 Mem0 記憶服務
- 本地化的語義記憶存儲
- 使用 all-MiniLM-L6-v2 進行文本嵌入
- 高效的記憶檢索系統

## 系統要求

1. **硬體需求**:
   - 支援 VLLM 的 GPU（建議 NVIDIA GPU with >=8GB VRAM）
   - 足夠的硬碟空間存儲模型和記憶數據

2. **軟體需求**:
   - Python 3.8+
   - CUDA Toolkit（用於 VLLM）
   - 所需 Python 包（見 requirements.txt）

## 安裝步驟

1. **安裝依賴**:
```bash
pip install -r requirements.txt
```

2. **設置本地服務**:

   A. VLLM 服務:
   ```bash
   # 下載模型（以 Llama 2 為例）
   huggingface-cli download meta-llama/Llama-2-7b-chat-hf

   # 啟動 VLLM 服務
   vllm --model /path/to/llama2/model --port 8000
   ```

   B. Mem0 服務:
   ```bash
   # 確保 config/services.yaml 配置正確
   mem0-server --config config/services.yaml --port 8001
   ```

3. **環境配置**:
   在 `.env` 文件中設置：
   ```
   # 選擇 LLM 提供者
   LLM_PROVIDER=vllm  # 或 openai

   # VLLM 配置
   VLLM_API_BASE=http://localhost:8000
   VLLM_MODEL=llama2

   # Mem0 配置
   MEM0_API_BASE=http://localhost:8001
   ```

4. **初始化遊戲**:
```bash
python setup.py
```

## 服務配置

### VLLM 配置（config/services.yaml）
```yaml
llm_services:
  vllm:
    host: localhost
    port: 8000
    models:
      - name: llama2
        path: /path/to/your/llama2/model
      - name: mistral
        path: /path/to/your/mistral/model
```

### Mem0 配置（config/services.yaml）
```yaml
mem0_service:
  host: localhost
  port: 8001
  storage_path: ./data/memories
  embedding_model: all-MiniLM-L6-v2
```

## 測試記憶系統

運行測試腳本來驗證服務是否正常運作：
```bash
python test_memory.py
```

測試腳本會：
1. 檢查所有本地服務是否正常運行
2. 執行一系列對話測試
3. 驗證記憶檢索功能
4. 顯示詳細的測試結果

## 遊戲特色

- 富有個性的女主角優希
- 多樣化的場景
- 智能記憶系統
- 動態對話生成
- 個性化反應

## 記憶系統說明

1. **短期記憶**
   - 存儲最近的對話上下文
   - 即時反應和連貫性

2. **長期記憶**
   - 使用本地 Mem0 服務存儲
   - 語義化搜索和檢索
   - 根據重要性自動存儲

3. **記憶檢索**
   - 基於當前對話上下文
   - 相關性排序
   - 自動整合到對話生成

## 遊戲指令

基本指令：
- `look` - 查看當前場景
- `inventory` - 查看物品欄
- `talk yuki [內容]` - 和優希對話
- `go [地點]` - 移動到其他場景
- `take [物品]` - 拿取物品
- `give [物品] to yuki` - 送禮物給優希
- `help` - 顯示幫助信息
- `save [名稱]` - 儲存遊戲
- `load [存檔]` - 讀取存檔

## 故障排除

1. **VLLM 服務問題**:
   - 檢查 GPU 驅動和 CUDA 版本
   - 確認模型路徑正確
   - 檢查 GPU 記憶體使用情況

2. **Mem0 服務問題**:
   - 確認存儲路徑權限
   - 檢查嵌入模型是否正確加載
   - 驗證記憶數據庫訪問

3. **常見錯誤**:
   ```bash
   # 檢查服務狀態
   curl http://localhost:8000/health
   curl http://localhost:8001/health

   # 查看服務日誌
   tail -f logs/vllm.log
   tail -f logs/mem0.log
   ```

## 性能優化

1. **VLLM 優化**:
   - 調整批處理大小
   - 優化模型量化
   - 使用張量並行

2. **記憶系統優化**:
   - 定期清理過期記憶
   - 優化嵌入計算
   - 調整檢索參數

## 開發說明

1. **添加新模型**:
   - 在 services.yaml 中添加模型配置
   - 確保模型格式兼容
   - 測試模型性能

2. **自定義記憶邏輯**:
   - 修改 NPCManager 中的記憶處理邏輯
   - 調整重要性閾值
   - 自定義記憶檢索策略

祝你在本地部署的遊戲中享受更流暢的體驗！