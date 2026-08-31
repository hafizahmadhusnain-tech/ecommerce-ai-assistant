import re
import json
import httpx
import requests
from app.core.config import settings
from app.services.ai.prompts import SYSTEM_PROMPT
from app.services.ai.tools.store_tools import (
    search_products, 
    track_order, 
    semantic_product_recommendation,
    list_store_categories
)

class AIAssistant:
    def __init__(self):
        self.model = settings.model or "gemini-3.1-flash-lite-preview"
        self.api_key = settings.GEMINI_API_KEY

    def _get_live_store_context(self, user_input: str) -> str:
        """Rapidly queries PostgreSQL database for live products, order status, or categories"""
        q = user_input.lower().strip()
        
        # Check order tracking intent
        if any(k in q for k in ["order", "track", "#", "delivery", "status", "courier", "package"]):
            digits = re.findall(r'\d+', user_input)
            if digits:
                return f"\n[Live Database - Order Status]:\n{track_order.invoke({'order_id': digits[0]})}"
        
        # Check category/store overview intent
        if any(k in q for k in ["category", "categories", "what do you sell", "catalog", "overview", "what products"]):
            return f"\n[Live Database - Store Overview]:\n{list_store_categories.invoke({})}"
        
        # Check recommendations or benefit search
        if any(k in q for k in ["recommend", "suggest", "best for", "gift", "gym", "study"]):
            sem = semantic_product_recommendation.invoke({"user_query": user_input})
            if sem:
                return f"\n[Live Database - Recommended Products]:\n{sem}"

        # Standard product keyword search
        return f"\n[Live Database - In-Stock Products Matching Query]:\n{search_products.invoke({'query': user_input})}"

    def ask(self, user_input: str, history: list = None) -> str:
        """Synchronous response generator with direct live store context"""
        store_context = self._get_live_store_context(user_input)
        full_system = f"{SYSTEM_PROMPT}\n\n{store_context}"
        
        contents = []
        if history:
            for h in history[-4:]:
                role = "user" if getattr(h, "type", "") == "human" or (isinstance(h, dict) and h.get("role") == "user") else "model"
                text_val = getattr(h, "content", "") if not isinstance(h, dict) else h.get("content", "")
                if text_val:
                    contents.append({"role": role, "parts": [{"text": str(text_val)}]})
                    
        contents.append({"role": "user", "parts": [{"text": user_input}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        payload = {
            "system_instruction": {"parts": [{"text": full_system}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.3}
        }
        
        try:
            r = requests.post(url, json=payload, timeout=12)
            if r.status_code == 200:
                data = r.json()
                parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
                return "".join([p.get("text", "") for p in parts if "text" in p])
            else:
                return f"Maaf kijiye, waqti masla aya (HTTP {r.status_code})."
        except Exception as e:
            return f"Error: {str(e)}"

    async def astream_ask(self, user_input: str, history: list = None):
        """Asynchronously streams tokens directly via native Gemini SSE stream in real time (< 400ms TTFT)"""
        store_context = self._get_live_store_context(user_input)
        full_system = f"{SYSTEM_PROMPT}\n\n{store_context}"

        contents = []
        if history:
            for h in history[-4:]:
                role = "user" if getattr(h, "type", "") == "human" or (isinstance(h, dict) and h.get("role") == "user") else "model"
                text_val = getattr(h, "content", "") if not isinstance(h, dict) else h.get("content", "")
                if text_val:
                    contents.append({"role": role, "parts": [{"text": str(text_val)}]})
                    
        contents.append({"role": "user", "parts": [{"text": user_input}]})

        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:streamGenerateContent?alt=sse&key={self.api_key}"
        payload = {
            "system_instruction": {"parts": [{"text": full_system}]},
            "contents": contents,
            "generationConfig": {"temperature": 0.3}
        }

        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code == 200:
                        async for line in response.aiter_lines():
                            if line and line.startswith("data: "):
                                try:
                                    data = json.loads(line[6:])
                                    candidates = data.get("candidates", [])
                                    if candidates:
                                        parts = candidates[0].get("content", {}).get("parts", [])
                                        for part in parts:
                                            if "text" in part and part["text"]:
                                                yield part["text"]
                                except Exception:
                                    pass
                    else:
                        yield f"Humari store service me masla aya (Status: {response.status_code})."
            except Exception as e:
                # Fallback to sync ask words
                try:
                    resp_text = self.ask(user_input, history)
                    for w in resp_text.split(" "):
                        yield w + " "
                except Exception:
                    yield f"Waqti masla aya: {str(e)}"

# Global Instance for clean access across api routes
ai_assistant = AIAssistant()