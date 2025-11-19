"""
Chat Service - COMPLETE VERSION with Order & Reservation Support
"""

from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.chat_log import ChatLog
from app.models.user import User
from app.models.menu import MenuItem
from app.services.gemini_service import gemini_service
from app.services.order_service import order_service
from app.services.reservation_service import reservation_service
from app.schemas.order import OrderCreate, OrderItemCreate
from app.schemas.reservation import ReservationCreate
from typing import Dict, Any, Optional, List
from datetime import datetime


class ChatService:
    """Service for managing chat conversations"""

    async def process_message(
        self,
        user_message: str,
        session_id: str,
        db: Session,
        user_id: Optional[int] = None,
        phone_number: Optional[str] = None,
        email: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process incoming chat message with order/reservation support
        """

        # Step 1: Get or create user
        user = None

        if phone_number:
            user = db.query(User).filter(User.phone_number == phone_number).first()

            if not user:
                # ⭐ CHANGED — always create if not found
                user = self._get_or_create_user(db, phone_number, email) #ADDED EMAIL

            user_id = user.id

        # Step 2: Get chat history for context
        chat_history = self._get_chat_history(db, session_id, limit=5)

        # Step 3: Determine intent
        intent = self._detect_intent(user_message)
        print(f"[DEBUG] Detected intent: {intent}")

        # Step 4: Handle different intents
        response_data = None

        if intent == 'order_intent':
            # Handle order placement
            response_data = await self._handle_order_intent(
                db, user_message, user_id, phone_number, chat_history
            )

        elif intent == 'reservation_intent':
            # Handle reservation
            response_data = await self._handle_reservation_intent(
                db, user_message, user_id, phone_number, chat_history
            )

        else:
            # Regular chat (menu query, FAQ, etc.)
            menu_items = []
            if intent == 'menu_query':
                menu_items = self._get_relevant_menu_items(db, user_message)

            ai_response = await gemini_service.generate_response(
                user_message=user_message,
                menu_items=menu_items if menu_items else None,
                chat_history=chat_history
            )

            response_data = {
                "response": ai_response['response'],
                "intent": intent,
                "session_id": session_id,
                "user_id": user_id,
                "menu_items": menu_items,
                "action": None
            }

        # Step 5: Save to database
        self._save_chat_log(
            db=db,
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            bot_response=response_data['response'],
            intent=intent
        )

        return response_data

    async def _handle_order_intent(
        self,
        db: Session,
        user_message: str,
        user_id: Optional[int],
        phone_number: Optional[str],
        chat_history: List[Dict]
    ) -> Dict[str, Any]:
        """Handle order placement through chat"""

        # Get available menu items
        menu_items = db.query(MenuItem).filter(
            MenuItem.is_available == True
        ).all()

        menu_items_dict = [item.to_dict() for item in menu_items]

        # Use Gemini to extract order items
        extraction_result = await gemini_service.extract_order_items(
            user_message,
            menu_items_dict
        )

        if not extraction_result['success'] or extraction_result['data']['confidence'] == 'low':
            # AI couldn't understand the order - ask for clarification
            return {
                "response": "I'd love to help you order! Could you please specify which items you'd like? For example: 'I want 2 Margherita pizzas and 1 Coke'",
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": menu_items_dict,
                "action": "clarification_needed"
            }

        # Extract order data
        order_data = extraction_result['data']

        try:
            # Create order items
            order_items = [
                OrderItemCreate(
                    menu_item_id=item['item_id'],
                    quantity=item['quantity']
                )
                for item in order_data['items']
            ]

            # Create order
            order_create = OrderCreate(
                user_id=user_id,
                phone_number=phone_number,
                items=order_items,
                delivery_address=None,  # Can ask for this next
                special_instructions=None
            )

            order = order_service.create_order(db, order_create)

            # Generate success response
            summary = order_service.generate_order_summary(order, db)

            response_text = f"Great! Your order has been placed successfully! 🎉\n\n{summary}\n\nWould you like this delivered? If yes, please provide your delivery address."

            return {
                "response": response_text,
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "action": "order_created",
                "order_id": order.id,
                "order_total": float(order.total_amount)
            }

        except Exception as e:
            print(f"[ERROR] Order creation failed: {str(e)}")
            return {
                "response": f"I'm sorry, there was an issue processing your order: {str(e)}. Could you please try again?",
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": menu_items_dict,
                "action": "order_failed"
            }

    async def _handle_reservation_intent(
        self,
        db: Session,
        user_message: str,
        user_id: Optional[int],
        phone_number: Optional[str],
        chat_history: List[Dict]
    ) -> Dict[str, Any]:
        """Handle reservation through chat"""

        # Use Gemini to extract reservation details
        extraction_result = await gemini_service.extract_reservation_details(user_message)

        if not extraction_result['success'] or extraction_result['data']['confidence'] == 'low':
            # AI couldn't understand - ask for clarification
            return {
                "response": "I'd be happy to help you make a reservation! Please provide:\n- Date (e.g., November 20)\n- Time (e.g., 7 PM)\n- Number of people\n\nFor example: 'Table for 4 on November 20 at 7 PM'",
                "intent": "reservation_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "action": "clarification_needed"
            }

        # Extract reservation data
        res_data = extraction_result['data']

        try:
            # Create reservation
            reservation_create = ReservationCreate(
                user_id=user_id,
                phone_number=phone_number,
                reservation_date=datetime.fromisoformat(res_data['date']).date(),
                reservation_time=datetime.fromisoformat(f"2025-01-01T{res_data['time']}").time(),
                party_size=res_data['party_size'],
                special_requests=res_data.get('special_requests')
            )

            reservation = reservation_service.create_reservation(db, reservation_create)

            # Generate success response
            summary = reservation_service.generate_reservation_summary(reservation)

            response_text = f"Perfect! Your reservation has been confirmed! ✅\n\n{summary}\n\nWe look forward to seeing you! Is there anything else I can help you with?"

            return {
                "response": response_text,
                "intent": "reservation_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "action": "reservation_created",
                "reservation_id": reservation.id
            }

        except Exception as e:
            print(f"[ERROR] Reservation creation failed: {str(e)}")
            return {
                "response": f"I'm sorry, there was an issue making your reservation: {str(e)}. Could you please try again?",
                "intent": "reservation_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "action": "reservation_failed"
            }

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
        if any(phrase in message_lower for phrase in ['i want to order', 'i want', "i'll take", "i'd like", 'order']):
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

    def _get_or_create_user(self, db: Session, phone_number: str, email: Optional[str] = None) -> User:
        """Get existing user or create new one automatically"""

        user = db.query(User).filter(User.phone_number == phone_number).first()

        if user:
            # ⭐ ADDED — Update email if provided and missing
            if email and not user.email:
                user.email = email
                db.commit()
                db.refresh(user)
            return user

        # ⭐ CHANGED — Create with email
        user = User(
            phone_number=phone_number,
            name="Guest User",
            email=email
        )
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
        """Get menu items relevant to the query"""

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

        # Check for categories
        category_keywords = {
            'appetizer': ['appetizer', 'starter', 'app'],
            'main': ['main', 'entree', 'meal', 'lunch', 'dinner'],
            'dessert': ['dessert', 'sweet', 'desserts'],
            'beverage': ['drink', 'drinks', 'beverage', 'beverages']
        }

        for category, keywords in category_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                items = db.query(MenuItem).filter(
                    MenuItem.is_available == True
                ).all()

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
