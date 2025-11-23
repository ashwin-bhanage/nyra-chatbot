"""
Gemini AI Service - Handles all AI interactions
(Cleaned & safe-fix: keeps structure, names)
"""

import json
import re
from typing import Optional, Dict, Any

import google.generativeai as genai
from app.config import settings

# NOTE: switch model id to a supported one on your environment.
# If you still see "model not found", replace with a model from your ListModels.
genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


class GeminiService:
    def __init__(self):
        self.model = model
        self.restaurant_context = self._build_restaurant_context()

    def _build_restaurant_context(self) -> str:
        return f"""
You are an AI assistant for {settings.RESTAURANT_NAME}, a friendly restaurant chatbot.
RESTAURANT INFORMATION:
- Name: {settings.RESTAURANT_NAME}
- Hours: {settings.RESTAURANT_HOURS}
- Delivery: {"Available" if settings.DELIVERY_AVAILABLE else "Not available"}
YOUR ROLE: Help customers browse the menu, place orders, and make reservations.
PERSONALITY: Friendly, warm, concise, enthusiastic about food.
"""

    async def generate_response(
        self,
        user_message: str,
        menu_items: Optional[list] = None,
        chat_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Returns:
            {"success": bool, "response": str, "intent": str, "error": Optional[str]}
        """
        try:
            prompt = self._build_prompt(user_message, menu_items, chat_history)

            # Model call - keep usage consistent with existing code
            response = self.model.generate_content(prompt)

            # Support different return shapes
            text = getattr(response, "text", None) or (response.get("text") if isinstance(response, dict) else None)
            if not text or not text.strip():
                raise ValueError("Empty response from model")

            intent = self._detect_intent(user_message)

            return {"success": True, "response": text.strip(), "intent": intent, "error": None}

        except Exception as e:
            print("[ERROR] Gemini API Error:", str(e))
            import traceback
            traceback.print_exc()
            return {
                "success": False,
                "response": "I'm having trouble right now. Please try again.",
                "intent": "error",
                "error": str(e)
            }

    def _build_prompt(
        self,
        user_message: str,
        menu_items: Optional[list] = None,
        chat_history: Optional[list] = None
    ) -> str:
        parts = [self.restaurant_context]

        if menu_items:
            menu_text_lines = ["\n\nAVAILABLE MENU ITEMS:"]
            for item in menu_items:
                name = item.get("name", "Unknown")
                price = item.get("price", "")
                description = item.get("description", "")
                menu_text_lines.append(f"- {name} — ₹{price}: {description}")
            parts.append("\n".join(menu_text_lines))

        if chat_history:
            history_lines = ["\n\nCONVERSATION HISTORY:"]
            for msg in (chat_history[-5:] if len(chat_history) > 5 else chat_history):
                user_msg = msg.get("user_message", "")
                bot_msg = msg.get("bot_response", "")
                history_lines.append(f"Customer: {user_msg}\nYou: {bot_msg}")
            parts.append("\n".join(history_lines))

        parts.append(f"\n\nCUSTOMER MESSAGE:\n{user_message}")

        if menu_items and self._detect_intent(user_message) == "menu_query":
            parts.append(
                "\n\nIMPORTANT:\n"
                "- You MUST list the menu in bullet points.\n"
                "- NEVER say you are having trouble.\n"
                "- If menu_items exist, ALWAYS produce a list.\n"
            )
        else:
            parts.append(
                "\n\nIMPORTANT:\n"
                "- NEVER respond with 'I'm having trouble right now. Please try again.'\n"
                "- If you are unsure, ask the user a clarifying question.\n"
            )

        return "\n".join(parts)

    def _detect_intent(self, message: str) -> str:
        m = (message or "").lower()

        if any(m.startswith(g) for g in ['hi', 'hello', 'hey']):
            return "greeting"

        order_keywords = [
            'order', 'add', 'want', 'give me', 'get me',
            "i'll have", "i'd like", "i'll take",
            'buy', 'can i get', 'can i have', 'please add', 'i need'
        ]
        if any(k in m for k in order_keywords):
            return "order_intent"

        # numeric + food -> order
        if re.search(r'\d+', m):
            food_words = [
                'biryani', 'chicken', 'paneer', 'veg', 'naan', 'roti',
                'tikka', 'dal', 'curry', 'rice', 'kebab', 'samosa',
                'lassi', 'chai', 'soup', 'kulfi'
            ]
            if any(f in m for f in food_words):
                return "order_intent"

        if any(k in m for k in ['book', 'reserve', 'reservation', 'table for']):
            return "reservation_intent"

        if any(k in m for k in ['hours', 'open', 'close', 'delivery', 'payment', 'location']):
            return "faq"

        if any(k in m for k in ['menu', 'food', 'dish', 'items', 'show']):
            return "menu_query"

        if any(k in m for k in ['biryani', 'naan', 'roti', 'chicken', 'paneer', 'soup', 'kulfi']):
            return "order_intent"

        return "general_query"

    async def extract_order_items(self, message: str, menu_items: list) -> Dict[str, Any]:
        """
        Attempt to extract ordered items from user message using the model.
        Falls back to a deterministic extractor on failure.
        Returns the same shape as before.
        """
        try:
            menu_text = "AVAILABLE MENU ITEMS:\n"
            for item in menu_items:
                menu_text += f"- ID:{item['id']} | {item['name']} | ₹{item['price']}\n"

            prompt = f"""{menu_text}
USER MESSAGE: "{message}"
TASK: Extract food items to order. Match to the menu above.
RESPOND ONLY with valid JSON (no markdown). Example:
{{"items":[{{"item_id":1,"item_name":"Example","quantity":1,"price":10.0}}],"total":10.0,"confidence":"high"}}
RULES: Default quantity=1. Use exact item_id from menu. If uncertain, return an empty items list and confidence 'low'."""

            response = self.model.generate_content(prompt)
            raw = getattr(response, "text", None) or (response.get("text") if isinstance(response, dict) else None)
            if not raw:
                raise ValueError("Empty extraction response")

            raw = raw.strip().replace("```json", "").replace("```", "").strip()

            json_match = re.search(r"\{[\s\S]*\}", raw)
            if not json_match:
                # Let fallback handle it
                raise json.JSONDecodeError("No JSON found", raw, 0)

            data = json.loads(json_match.group())

            # Basic validation
            if data.get("items"):
                return {"success": True, "data": data, "error": None}

            # Model returned no items → fallback
            return self._fallback_extract_order(message, menu_items)

        except Exception as e:
            print(f"[ERROR] Order extraction error: {str(e)}")
            return self._fallback_extract_order(message, menu_items)

    def _fallback_extract_order(self, message: str, menu_items: list) -> Dict[str, Any]:
        """
        Deterministic fallback extractor with STRICT matching.
        Returns LOW confidence if query is too generic.
        """
        print("[DEBUG] Running STRICT fallback order extraction...")

        msg = (message or "").lower().strip()
        found_items = []
        total = 0.0

        # Check if query is too generic (just category name)
        generic_terms = [
            'biryani', 'naan', 'roti', 'dessert', 'beverage', 'drink',
            'soup', 'starter', 'curry', 'order', 'food', 'menu'
        ]

        # If message is ONLY a generic term (e.g., just "biryani"), return low confidence
        msg_words = msg.split()
        if len(msg_words) <= 2 and any(term == msg or term in msg_words for term in generic_terms):
            # Check if there's a specific modifier
            modifiers = ['chicken', 'veg', 'vegetable', 'paneer', 'mutton', 'egg', 'butter', 'garlic']
            has_modifier = any(mod in msg for mod in modifiers)

            if not has_modifier:
                print(f"[DEBUG] Query too generic: '{msg}' - returning low confidence")
                return {
                    "success": False,
                    "data": {"items": [], "total": 0.0, "confidence": "low"},
                    "error": "Query too generic"
                }

        # Synonyms to expand
        synonyms = {"veg": "vegetable", "veggie": "vegetable", "chix": "chicken"}
        for k, v in synonyms.items():
            if re.search(r'\b' + re.escape(k) + r'\b', msg):
                msg += " " + v

        # Split into candidate segments
        segments = re.split(r"\band\b|,|&|\n", msg)

        for segment in segments:
            seg = segment.strip()
            if not seg:
                continue

            for item in menu_items:
                name = item["name"]
                name_lower = name.lower()
                matched = False

                # STRICT matching rules:

                # 1) Exact full name match
                if name_lower == seg:
                    matched = True

                # 2) User said specific item + category (e.g., "chicken biryani", "butter naan")
                elif name_lower in seg and len(seg.split()) >= 2:
                    matched = True

                # 3) All words from item name present in segment
                elif len(name_lower.split()) >= 2:
                    item_words = set(re.findall(r'\w+', name_lower))
                    seg_words = set(re.findall(r'\w+', seg))
                    if item_words.issubset(seg_words):
                        matched = True

                if not matched:
                    continue

                # Quantity detection
                quantity = 1
                qty_patterns = [
                    rf"(\d+)\s*(?:x)?\s*{re.escape(name_lower)}",
                    rf"{re.escape(name_lower)}\s*(\d+)",
                    r"(\d+)\s+(?:x|pieces|pcs|orders|order)\b"
                ]

                for p in qty_patterns:
                    m_qty = re.search(p, seg)
                    if m_qty:
                        try:
                            quantity = int(m_qty.group(1))
                            if quantity > 20:  # sanity check
                                quantity = 1
                        except Exception:
                            quantity = 1
                        break

                # Avoid duplicates
                if any(f["item_id"] == item["id"] for f in found_items):
                    continue

                found_items.append({
                    "item_id": item["id"],
                    "item_name": item["name"],
                    "quantity": quantity,
                    "price": float(item["price"])
                })

                total += float(item["price"]) * quantity
                print(f"[DEBUG] Matched: {item['name']} x {quantity}")

        if not found_items:
            print("[DEBUG] No specific items matched")
            return {
                "success": False,
                "data": {"items": [], "total": 0.0, "confidence": "low"},
                "error": "No match"
            }

        print(f"[DEBUG] Found {len(found_items)} items")
        return {
            "success": True,
            "data": {"items": found_items, "total": total, "confidence": "high"},
            "error": None
        }

    async def extract_reservation_details(self, message: str) -> Dict[str, Any]:
        """
        Attempts to parse reservation details into a deterministic JSON.
        Keeps the same return shape as before.
        """
        try:
            prompt = (
                f'User wants reservation: "{message}"\n'
                'Respond ONLY with JSON in ISO date/time where possible. Example:\n'
                '{"date":"2025-11-15","time":"19:00","party_size":4,"special_requests":"", "confidence":"high"}\n'
                'If you cannot determine a value, return empty string for that field and confidence "low".'
            )

            response = self.model.generate_content(prompt)
            cleaned = getattr(response, "text", None) or (response.get("text") if isinstance(response, dict) else None)
            if not cleaned:
                raise ValueError("Empty reservation parsing response")

            cleaned = cleaned.strip().replace("```json", "").replace("```", "").strip()
            json_match = re.search(r"\{[\s\S]*\}", cleaned)
            if not json_match:
                raise json.JSONDecodeError("No JSON found", cleaned, 0)

            data = json.loads(json_match.group())
            return {"success": True, "data": data, "error": None}

        except Exception as e:
            print(f"[ERROR] Reservation parsing: {str(e)}")
            return {"success": False, "data": None, "error": str(e)}


# singleton
gemini_service = GeminiService()
