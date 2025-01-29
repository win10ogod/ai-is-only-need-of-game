from dataclasses import dataclass, field
from typing import Dict, List, Optional
import json
from datetime import datetime
from openai import OpenAI

@dataclass
class Memory:
    content: str
    timestamp: str
    importance: float = 1.0
    tags: List[str] = field(default_factory=list)

@dataclass
class NPCState:
    id: str
    name: str
    personality: str
    background: str
    short_term_memory: List[Dict] = field(default_factory=list)
    long_term_memory: List[Memory] = field(default_factory=list)
    state: Dict = field(default_factory=dict)

class NPCManager:
    def __init__(self, api_key: str):
        """Initialize NPCManager with OpenAI API key."""
        self.client = OpenAI(api_key=api_key)
        self.npcs: Dict[str, NPCState] = {}
        self.max_short_term_memory = 10
        self.memory_importance_threshold = 0.7

    def create_npc(self, npc_id: str, name: str, personality: str, background: str) -> None:
        """Create a new NPC with given attributes."""
        self.npcs[npc_id] = NPCState(
            id=npc_id,
            name=name,
            personality=personality,
            background=background
        )

    def _create_prompt(self, npc: NPCState, player_input: str) -> str:
        """Create a prompt for the AI model combining NPC personality and relevant memories."""
        system_prompt = f"""You are {npc.name}, with the following traits:
Personality: {npc.personality}
Background: {npc.background}

You must stay in character and respond as this persona would.
"""
        
        # Add relevant long-term memories
        relevant_memories = [
            f"- {memory.content} ({memory.timestamp})"
            for memory in npc.long_term_memory[-5:]  # Last 5 memories
        ]
        if relevant_memories:
            system_prompt += "\nLong-term memories:\n" + "\n".join(relevant_memories)

        # Add recent conversation context
        recent_context = [
            f"{'Player' if msg['role'] == 'user' else npc.name}: {msg['content']}"
            for msg in npc.short_term_memory[-3:]  # Last 3 exchanges
        ]
        if recent_context:
            system_prompt += "\nRecent conversation:\n" + "\n".join(recent_context)

        return system_prompt

    async def get_response(self, npc_id: str, player_input: str) -> str:
        """Get AI response for player input, considering NPC's memory and personality."""
        npc = self.npcs.get(npc_id)
        if not npc:
            raise ValueError(f"NPC {npc_id} not found")

        # Prepare conversation messages
        messages = [
            {"role": "system", "content": self._create_prompt(npc, player_input)},
            {"role": "user", "content": player_input}
        ]

        try:
            # Get response from OpenAI
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
            )
            
            ai_response = response.choices[0].message.content

            # Update short-term memory
            npc.short_term_memory.append({"role": "user", "content": player_input})
            npc.short_term_memory.append({"role": "assistant", "content": ai_response})
            
            # Trim short-term memory if too long
            if len(npc.short_term_memory) > self.max_short_term_memory:
                # Before trimming, analyze if any important information should be moved to long-term memory
                await self._analyze_and_store_long_term_memory(npc)
                # Keep only recent messages
                npc.short_term_memory = npc.short_term_memory[-self.max_short_term_memory:]

            return ai_response

        except Exception as e:
            return f"Error getting response: {str(e)}"

    async def _analyze_and_store_long_term_memory(self, npc: NPCState) -> None:
        """Analyze conversation and store important information in long-term memory."""
        # Combine recent messages for analysis
        recent_conversation = "\n".join([
            f"{'Player' if msg['role'] == 'user' else npc.name}: {msg['content']}"
            for msg in npc.short_term_memory[-2:]  # Analyze last exchange
        ])

        # Ask AI to analyze importance and extract key information
        messages = [
            {
                "role": "system",
                "content": """Analyze the conversation and extract important information that should be remembered long-term.
                Rate importance from 0.0 to 1.0. Return JSON format:
                {"importance": float, "content": "key information", "tags": ["relevant_tags"]}
                Return null if no significant information to remember."""
            },
            {"role": "user", "content": recent_conversation}
        ]

        try:
            response = await self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.3
            )
            
            analysis = json.loads(response.choices[0].message.content)
            if analysis and analysis["importance"] >= self.memory_importance_threshold:
                # Store as long-term memory
                npc.long_term_memory.append(Memory(
                    content=analysis["content"],
                    timestamp=datetime.now().isoformat(),
                    importance=analysis["importance"],
                    tags=analysis["tags"]
                ))

        except Exception as e:
            print(f"Error in memory analysis: {str(e)}")

    def save_npc_state(self, npc_id: str) -> Dict:
        """Save NPC state to dictionary."""
        npc = self.npcs.get(npc_id)
        if not npc:
            raise ValueError(f"NPC {npc_id} not found")
        
        return {
            "id": npc.id,
            "name": npc.name,
            "personality": npc.personality,
            "background": npc.background,
            "short_term_memory": npc.short_term_memory,
            "long_term_memory": [vars(m) for m in npc.long_term_memory],
            "state": npc.state
        }

    def load_npc_state(self, state: Dict) -> None:
        """Load NPC state from dictionary."""
        npc_id = state["id"]
        self.npcs[npc_id] = NPCState(
            id=state["id"],
            name=state["name"],
            personality=state["personality"],
            background=state["background"],
            short_term_memory=state["short_term_memory"],
            long_term_memory=[
                Memory(**m) for m in state["long_term_memory"]
            ],
            state=state["state"]
        )