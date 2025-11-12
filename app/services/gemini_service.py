"""
Gemini AI Service - Handles all AI interactions
"""

import google.generativeai as genai
from app.config import settings
from typing import Optional, Dict, Any
import json

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

# Initialize the model
# Using gemini-pro for text generation
model = genai.GenerativeModel('gemini-2.5-flash')


class GeminiService:
    """Service class for Gemini AI interactions"""

    def __init__(self):
        self.model = model
        self.restaurant_context = self._build_restaurant_context()

    def _build_restaurant_context(self) -> str:
        """
        Build context about the restaurant
        This is prepended to every conversation
        """
        context = f"""
You are an AI assistant for {settings.RESTAURANT_NAME}, a friendly restaurant chatbot.

RESTAURANT INFORMATION:
- Name: {settings.RESTAURANT_NAME}
- Hours: {settings.RESTAURANT_HOURS}
- Delivery: {'Available' if settings.DELIVERY_AVAILABLE else 'Not available'}

YOUR ROLE:
- Help customers browse the menu
- Answer questions about food items
- Assist with placing orders
- Help with table reservations
- Provide information about the restaurant

PERSONALITY:
- Be friendly, warm, and helpful
- Use casual but professional language
- Be concise but informative
- Show enthusiasm about the food
- Handle complaints gracefully

CAPABILITIES:
1. Show menu items by category (appetizer, main, dessert, beverage)
2. Provide details about specific dishes
3. Help customers place orders
4. Make table reservations
5. Answer FAQs about hours, delivery, payments

IMPORTANT RULES:
- Always be polite and customer-focused
- If you don't know something, say so honestly
- Don't make up prices or menu items
- Suggest alternatives if something is unavailable
- Confirm order details before finalizing
"""
        return context

    async def generate_response(
        self,
        user_message: str,
        menu_items: Optional[list] = None,
        chat_history: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Generate AI response for user message

        Args:
            user_message: The user's message
            menu_items: List of menu items (if relevant to query)
            chat_history: Previous conversation messages

        Returns:
            Dict with response, intent, and additional data
        """
        try:
            # Build the complete prompt
            prompt = self._build_prompt(user_message, menu_items, chat_history)

            # Generate response from Gemini
            response = self.model.generate_content(prompt)

            # Extract intent from the message
            intent = self._detect_intent(user_message)

            return {
                "success": True,
                "response": response.text,
                "intent": intent,
                "error": None
            }

        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            return {
                "success": False,
                "response": "I'm having trouble processing your request right now. Please try again in a moment.",
                "intent": "error",
                "error": str(e)
            }

    def _build_prompt(
        self,
        user_message: str,
        menu_items: Optional[list] = None,
        chat_history: Optional[list] = None
    ) -> str:
        """Build the complete prompt for Gemini"""

        prompt_parts = [self.restaurant_context]

        # Add menu items if provided
        if menu_items:
            menu_text = "\n\nAVAILABLE MENU ITEMS:\n"
            for item in menu_items:
                menu_text += f"- {item['name']} (${item['price']}): {item.get('description', 'No description')}\n"
            prompt_parts.append(menu_text)

        # Add chat history for context
        if chat_history:
            history_text = "\n\nCONVERSATION HISTORY:\n"
            for msg in chat_history[-5:]:  # Last 5 messages for context
                history_text += f"Customer: {msg['user_message']}\n"
                history_text += f"You: {msg['bot_response']}\n"
            prompt_parts.append(history_text)

        # Add current user message
        prompt_parts.append(f"\n\nCUSTOMER'S CURRENT MESSAGE:\n{user_message}")

        # Add response instructions
        prompt_parts.append("""

RESPOND TO THE CUSTOMER:
- Be natural and conversational
- If they're asking about menu, show relevant items
- If they want to order, guide them through the process
- If they want to reserve, ask for date, time, and party size
- Keep responses concise (2-4 sentences usually)
""")

        return "\n".join(prompt_parts)

    def _detect_intent(self, message: str) -> str:
        """
        Detect user intent from message
        Simple keyword-based detection (can be improved with AI)
        """
        message_lower = message.lower()

        # Menu query keywords
        menu_keywords = ['menu', 'food', 'dish', 'eat', 'items', 'show', 'available',
                        'pizza', 'burger', 'pasta', 'salad', 'dessert', 'drink', 'beverage',
                        'appetizer', 'main', 'entree']

        # Order keywords
        order_keywords = ['order', 'buy', 'want', 'get', 'purchase', 'take', 'add to cart',
                         'i want', "i'll take", "i'd like"]

        # Reservation keywords
        reservation_keywords = ['book', 'reserve', 'table', 'reservation', 'booking',
                               'book a table', 'reserve a table']

        # Greeting keywords
        greeting_keywords = ['hi', 'hello', 'hey', 'good morning', 'good afternoon',
                           'good evening', 'greetings', 'sup', 'yo']

        # FAQ keywords
        faq_keywords = ['hours', 'open', 'close', 'delivery', 'payment', 'accept',
                       'location', 'address', 'what time', 'when do you', 'do you',
                       'timing', 'schedule']

        # Check intents (order matters - more specific first)
        if any(keyword in message_lower for keyword in greeting_keywords):
            return "greeting"
        elif any(keyword in message_lower for keyword in reservation_keywords):
            return "reservation_intent"
        elif any(keyword in message_lower for keyword in order_keywords):
            return "order_intent"
        elif any(keyword in message_lower for keyword in faq_keywords):
            return "faq"
        elif any(keyword in message_lower for keyword in menu_keywords):
            return "menu_query"
        else:
            return "general_query"

    async def extract_order_items(self, message: str, menu_items: list) -> Dict[str, Any]:
        """
        Extract order items and quantities from user message using AI

        Args:
            message: User's order message
            menu_items: Available menu items

        Returns:
            Dict with extracted items and quantities
        """
        try:
            # Build menu context
            menu_text = "Available items:\n"
            for item in menu_items:
                menu_text += f"- {item['name']} (ID: {item['id']}, Price: ${item['price']})\n"

            prompt = f"""
{menu_text}

User wants to order: "{message}"

Extract the items and quantities they want to order.
Respond ONLY with a JSON object in this exact format:
{{
    "items": [
        {{"item_id": 4, "item_name": "Margherita Pizza", "quantity": 2, "price": 12.99}}
    ],
    "total": 25.98,
    "confidence": "high"
}}

If you can't determine items clearly, set confidence to "low".
Only include items that exist in the available menu.
"""

            response = self.model.generate_content(prompt)

            # Parse JSON from response
            # Remove markdown code blocks if present
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            order_data = json.loads(response_text)
            return {
                "success": True,
                "data": order_data,
                "error": None
            }

        except Exception as e:
            print(f"Order extraction error: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }

    async def extract_reservation_details(self, message: str) -> Dict[str, Any]:
        """
        Extract reservation details from user message

        Args:
            message: User's reservation message

        Returns:
            Dict with date, time, party_size
        """
        try:
            prompt = f"""
User wants to make a reservation: "{message}"

Extract the reservation details.
Respond ONLY with a JSON object in this exact format:
{{
    "date": "2025-11-15",
    "time": "19:00",
    "party_size": 4,
    "special_requests": "window seat",
    "confidence": "high"
}}

If any detail is missing or unclear, set confidence to "low".
Use ISO format for date (YYYY-MM-DD) and time (HH:MM in 24-hour format).
"""

            response = self.model.generate_content(prompt)

            # Parse JSON
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            reservation_data = json.loads(response_text)
            return {
                "success": True,
                "data": reservation_data,
                "error": None
            }

        except Exception as e:
            print(f"Reservation extraction error: {str(e)}")
            return {
                "success": False,
                "data": None,
                "error": str(e)
            }


# Create singleton instance
gemini_service = GeminiService()
