# Text Adventure Engine 開發指南

本指南將介紹如何使用引擎開發複雜的文字冒險遊戲，並說明引擎的能力與限制。

## 引擎架構概述

### 1. 核心系統

```
GameWorld
├── Scene Management
│   ├── 場景轉換
│   ├── 場景狀態
│   └── 場景觸發器
├── Item System
│   ├── 物品屬性
│   ├── 物品互動
│   └── 物品組合
├── Event System
│   ├── 事件觸發
│   ├── 事件處理
│   └── 事件鏈
└── State Management
    ├── 遊戲狀態
    ├── 存檔系統
    └── 狀態追踪
```

### 2. NPC系統

```
NPCManager
├── Character State
│   ├── 基本屬性
│   ├── 動態狀態
│   └── 關係系統
├── Memory System
│   ├── 短期記憶
│   ├── 長期記憶
│   └── 記憶觸發
└── AI Integration
    ├── 對話生成
    ├── 行為決策
    └── 情境理解
```

## 高級功能實現

### 1. 複雜事件鏈
```python
class ComplexEvent:
    def __init__(self):
        self.prerequisites = []
        self.triggers = {}
        self.consequences = []
        self.state = {}

    async def check_prerequisites(self, game_world):
        return all(await prereq.check(game_world) for prereq in self.prerequisites)

    async def execute(self, game_world):
        if await self.check_prerequisites(game_world):
            for consequence in self.consequences:
                await consequence.apply(game_world)
            return True
        return False
```

### 2. 物品組合系統
```python
class CraftingSystem:
    def __init__(self):
        self.recipes = {}
        self.required_tools = {}
        
    def add_recipe(self, inputs: List[str], output: str, tools: Optional[List[str]] = None):
        self.recipes[tuple(sorted(inputs))] = output
        if tools:
            self.required_tools[output] = tools

    def can_craft(self, items: List[str], available_tools: List[str]) -> bool:
        recipe_key = tuple(sorted(items))
        if recipe_key not in self.recipes:
            return False
        
        output = self.recipes[recipe_key]
        required_tools = self.required_tools.get(output, [])
        return all(tool in available_tools for tool in required_tools)
```

### 3. 條件觸發器
```python
class ConditionalTrigger:
    def __init__(self):
        self.conditions = []
        self.actions = []
        self.state_changes = {}
        self.priority = 0

    async def evaluate(self, game_world):
        if all(await condition.check(game_world) for condition in self.conditions):
            for action in self.actions:
                await action.execute(game_world)
            game_world.update_state(self.state_changes)
            return True
        return False
```

## 最佳實踐

### 1. 場景設計
```yaml
scene:
  id: "puzzle_room"
  name: "神秘房間"
  description: "一個充滿謎題的房間，牆上有多個符號，中間放著一個機關箱。"
  items:
    mechanism_box:
      id: "box_01"
      name: "機關箱"
      description: "一個精密的機關箱，需要正確的組合才能打開。"
      state:
        locked: true
        combination: ["symbol_1", "symbol_3", "symbol_2"]
      interactions:
        - action: "examine"
          response: "箱子上有三個槽，似乎需要特定的符號卡片。"
        - action: "insert"
          requires_items: true
          validate: "check_combination"
```

### 2. NPC對話設計
```yaml
npc_dialogue:
  id: "sage"
  personality: "智者"
  knowledge_base:
    - topic: "符號"
      hints:
        - condition: "first_meeting"
          text: "符號的順序與月光的方向有關。"
        - condition: "examined_window"
          text: "你注意到窗戶的特殊設計了嗎？"
  memory_triggers:
    - type: "item_shown"
      item: "ancient_scroll"
      response: "這讓我想起一個古老的預言..."
```

### 3. 解謎機制
```python
class PuzzleMechanism:
    def __init__(self):
        self.states = {}
        self.dependencies = {}
        self.solutions = {}
        
    def add_dependency(self, puzzle_id: str, required_states: Dict):
        self.dependencies[puzzle_id] = required_states
        
    def is_solvable(self, puzzle_id: str) -> bool:
        if puzzle_id not in self.dependencies:
            return True
        return all(
            self.states.get(key) == value 
            for key, value in self.dependencies[puzzle_id].items()
        )
```

## 效能考量

1. **記憶系統優化**
   - 限制短期記憶大小（預設10條）
   - 長期記憶重要性閾值（>=0.7）
   - 定期清理非關鍵記憶

2. **事件處理優化**
   - 使用事件優先級
   - 條件預檢查
   - 事件批處理

3. **狀態管理優化**
   - 增量更新
   - 狀態緩存
   - 懶加載機制

## 引擎限制

1. **規模限制**
   - 單一場景最大物品數：100
   - 最大活躍NPC數：10
   - 最大並發事件數：50

2. **記憶系統限制**
   - 短期記憶上限：10條
   - 長期記憶無硬性限制，但建議控制在1000條以內
   - 記憶檢索深度：最近100條

3. **互動限制**
   - 物品組合最大數量：3個
   - 條件判斷最大深度：5層
   - 事件鏈最大長度：10

## 擴展建議

1. **自定義事件處理器**
```python
class CustomEventHandler:
    def __init__(self):
        self.handlers = {}
        
    def register(self, event_type: str, handler: callable):
        self.handlers[event_type] = handler
        
    async def handle(self, event: Event):
        if event.type in self.handlers:
            return await self.handlers[event.type](event)
```

2. **狀態追踪器**
```python
class StateTracker:
    def __init__(self):
        self.states = {}
        self.history = []
        self.watchers = []
        
    def add_watcher(self, state_key: str, callback: callable):
        self.watchers.append((state_key, callback))
        
    def update_state(self, key: str, value: any):
        old_value = self.states.get(key)
        self.states[key] = value
        self.history.append((key, old_value, value))
        self._notify_watchers(key, old_value, value)
```

3. **自定義指令**
```python
class CustomCommandManager:
    def __init__(self):
        self.commands = {}
        
    def register_command(self, name: str, handler: callable, help_text: str):
        self.commands[name] = {
            'handler': handler,
            'help': help_text
        }
        
    async def execute_command(self, command: str, args: List[str]):
        if command in self.commands:
            return await self.commands[command]['handler'](args)
```

## 除錯工具

1. **狀態檢視器**
```python
class StateInspector:
    @staticmethod
    def dump_game_state(game_world):
        return {
            'scene': game_world.current_scene.id,
            'inventory': [item.id for item in game_world.inventory],
            'npc_states': {npc.id: npc.state for npc in game_world.npcs},
            'events': game_world.event_queue
        }
```

2. **事件追踪器**
```python
class EventTracer:
    def __init__(self):
        self.trace_log = []
        
    def log_event(self, event: Event, result: bool):
        self.trace_log.append({
            'timestamp': datetime.now(),
            'event_type': event.type,
            'source': event.source_id,
            'target': event.target_id,
            'result': result
        })
```

## 性能監控

```python
class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
        
    @contextmanager
    def measure(self, operation: str):
        start = time.time()
        yield
        duration = time.time() - start
        self.metrics[operation].append(duration)
        
    def get_statistics(self):
        return {
            op: {
                'avg': sum(times)/len(times),
                'max': max(times),
                'min': min(times)
            }
            for op, times in self.metrics.items()
        }
```

使用這些工具和指南，開發者可以創建複雜的解謎遊戲，同時確保遊戲的性能和可維護性。接下來我們將通過一個具體的解謎遊戲示例來展示這些功能的實際應用。