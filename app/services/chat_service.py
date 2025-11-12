"""
Chat Service - FIXED VERSION
Replace your chat_service.py with this
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.chat_log import ChatLog
from app.models.user import User
from app.models.menu import MenuItem
from app.services.gemini_service import gemini_service
from typing import Dict, Any, Optional, List


class ChatService:
    """Service for managing chat conversations"""

    async def process_message(
        self,
        user_message: str,
        session_id: str,
        db: Session,
        user_id: Optional[int] = None,
        phone_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process incoming chat message
        """

        # Step 1: Get or create user
        if phone_number and not user_id:
            user = self._get_or_create_user(db, phone_number)
            user_id = user.id

        # Step 2: Get chat history for context
        chat_history = self._get_chat_history(db, session_id, limit=5)

        # Step 3: Determine intent and get menu items if needed
        intent = self._detect_intent(user_message)
        print(f"[DEBUG] Detected intent: {intent}")

        menu_items = []
        if intent in ['menu_query', 'order_intent']:
            menu_items = self._get_relevant_menu_items(db, user_message)
            print(f"[DEBUG] Found {len(menu_items)} menu items")

        # Step 4: Generate AI response
        ai_response = await gemini_service.generate_response(
            user_message=user_message,
            menu_items=menu_items if menu_items else None,
            chat_history=chat_history
        )

        # Step 5: Save to database
        self._save_chat_log(
            db=db,
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            bot_response=ai_response['response'],
            intent=intent
        )

        # Step 6: Prepare response
        response_data = {
            "response": ai_response['response'],
            "intent": intent,
            "session_id": session_id,
            "user_id": user_id,
            "menu_items": menu_items
        }

        return response_data

    def _detect_intent(self, message: str) -> str:
        """Enhanced intent detection"""
        message_lower = message.lower()

        # Greeting (check first - most specific)
        if any(word in message_lower for word in ['hi', 'hello', 'hey', 'greetings']) and len(message_lower.split()) <= 3:
            return 'greeting'

        # Reservation
        if any(word in message_lower for word in ['book', 'reserve', 'reservation', 'table for']):
            return 'reservation_intent'

        # Order intent
        if any(phrase in message_lower for phrase in ['i want to order', 'i want', "i'll take", "i'd like"]):
            return 'order_intent'

        # FAQ - specific patterns
        if any(word in message_lower for word in ['hours', 'open', 'close', 'delivery', 'deliver', 'payment', 'what time', 'when do']):
            return 'faq'

        # Menu query - anything about food/items
        if any(word in message_lower for word in ['menu', 'food', 'dish', 'pizza', 'burger', 'pasta', 'salad',
                                                   'dessert', 'drink', 'beverage', 'appetizer', 'show', 'have',
                                                   'wings', 'brownie', 'cake', 'coffee', 'juice', 'what']):
            return 'menu_query'

        return 'general_query'

    def _get_or_create_user(self, db: Session, phone_number: str) -> User:
        """Get existing user or create new one"""
        user = db.query(User).filter(User.phone_number == phone_number).first()

        if not user:
            user = User(phone_number=phone_number)
            db.add(user)
            db.commit()
            db.refresh(user)

        return user

    def _get_chat_history(
        self,
        db: Session,
        session_id: str,
        limit: int = 5
    ) -> List[Dict[str, str]]:
        """Get recent chat history for context"""
        logs = db.query(ChatLog).filter(
            ChatLog.session_id == session_id
        ).order_by(
            ChatLog.timestamp.desc()
        ).limit(limit).all()

        logs = list(reversed(logs))

        return [
            {
                "user_message": log.user_message,
                "bot_response": log.bot_response
            }
            for log in logs
        ]

    def _get_relevant_menu_items(
        self,
        db: Session,
        message: str
    ) -> List[Dict[str, Any]]:
        """Get menu items relevant to the query - FIXED VERSION"""

        message_lower = message.lower()
        print(f"[DEBUG] Searching for: '{message_lower}'")

        # Check for specific items first
        search_terms = {
            'pizza': ['pizza'],
            'burger': ['burger'],
            'pasta': ['pasta'],
            'salad': ['salad'],
            'wings': ['wings'],
            'bread': ['bread'],
            'brownie': ['brownie'],
            'cake': ['cake', 'cheesecake'],
            'coffee': ['coffee'],
            'juice': ['juice'],
            'cola': ['cola'],
            'tiramisu': ['tiramisu'],
            'mozzarella': ['mozzarella']
        }

        for key, terms in search_terms.items():
            if any(term in message_lower for term in terms):
                items = db.query(MenuItem).filter(
                    or_(*[MenuItem.name.ilike(f"%{term}%") for term in terms]),
                    MenuItem.is_available == True
                ).all()

                if items:
                    print(f"[DEBUG] Found {len(items)} items for '{key}'")
                    return [item.to_dict() for item in items]

        # Check for categories using string matching (not enum)
        category_keywords = {
            'appetizer': ['appetizer', 'starter', 'app'],
            'main': ['main', 'entree', 'meal', 'lunch', 'dinner'],
            'dessert': ['dessert', 'sweet', 'desserts'],
            'beverage': ['drink', 'drinks', 'beverage', 'beverages']
        }

        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                # Use string comparison for category
                items = db.query(MenuItem).filter(
                    MenuItem.is_available == True
                ).all()

                # Filter by category string value
                filtered_items = [
                    item for item in items
                    if item.category.value.lower() == category
                ]

                print(f"[DEBUG] Found {len(filtered_items)} items in category '{category}'")

                if filtered_items:
                    return [item.to_dict() for item in filtered_items]

        # Default: return all items
        print("[DEBUG] No match, returning all items")
        items = db.query(MenuItem).filter(
            MenuItem.is_available == True
        ).limit(10).all()

        return [item.to_dict() for item in items]

    def _save_chat_log(
        self,
        db: Session,
        user_id: Optional[int],
        session_id: str,
        user_message: str,
        bot_response: str,
        intent: str
    ):
        """Save chat interaction to database"""

        chat_log = ChatLog(
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            intent=intent
        )

        db.add(chat_log)
        db.commit()

    def get_session_history(
        self,
        db: Session,
        session_id: str
    ) -> List[ChatLog]:
        """Get full chat history for a session"""

        return db.query(ChatLog).filter(
            ChatLog.session_id == session_id
        ).order_by(
            ChatLog.timestamp.asc()
        ).all()


# Create singleton instance
chat_service = ChatService()
