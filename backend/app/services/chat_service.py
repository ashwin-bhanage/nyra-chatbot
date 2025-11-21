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
        phone_number: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process incoming chat message with order/reservation support
        """

        # Step 1: Get or create user
        if phone_number and not user_id:
            user = self._get_or_create_user(db, phone_number)
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
        """Handle order placement through chat - ADD TO CART instead of creating order"""

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

        if not extraction_result['success'] or (extraction_result.get('data') and extraction_result['data'].get('confidence') == 'low'):
            # AI couldn't understand the order - ask for clarification
            return {
                "response": "I'd love to help you order! Could you please specify which items you'd like? For example: 'I want 2 Chicken Biryani and 1 Butter Naan'",
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": menu_items_dict,
                "cart_items": [],
                "action": "clarification_needed"
            }

        # Extract order data
        order_data = extraction_result['data']

        try:
            # Prepare cart items to send to frontend
            cart_items = []
            total_amount = 0

            for item in order_data.get('items', []):
                # Find the menu item details
                menu_item = next(
                    (m for m in menu_items_dict if m['id'] == item['item_id']),
                    None
                )
                if menu_item:
                    price = float(item.get('price', menu_item.get('price', 0)))
                    quantity = int(item.get('quantity', 1))
                    cart_items.append({
                        'id': item['item_id'],
                        'name': item.get('item_name', menu_item.get('name')),
                        'price': price,
                        'quantity': quantity,
                        'description': menu_item.get('description', '')
                    })
                    total_amount += price * quantity

            # Build response message — use ₹ and integer display when possible
            items_text = "\n".join([
                f"• {item['quantity']}x {item['name']} (₹{int(item['price'])} each)"
                for item in cart_items
            ])

            response_text = (
                f"Great choice! I've added these items to your cart:\n\n"
                f"{items_text}\n\n"
                f"💰 Subtotal: ₹{int(total_amount)}\n\n"
                "You can review your cart and place the order when ready! 🛒"
            )

            return {
                "response": response_text,
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "cart_items": cart_items,
                "action": "items_added_to_cart"
            }

        except Exception as e:
            print(f"[ERROR] Cart preparation failed: {str(e)}")
            return {
                "response": f"I'm sorry, there was an issue adding items to your cart. Could you please try again?",
                "intent": "order_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": menu_items_dict,
                "cart_items": [],
                "action": "cart_failed"
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
        """Get menu items relevant to the query"""

        message_lower = message.lower().strip()
        print(f"[DEBUG] Searching for: '{message_lower}'")

        # 1) Quick exact name match (case-insensitive, partial)
        exact_items = db.query(MenuItem).filter(
            MenuItem.is_available == True,
            MenuItem.name.ilike(f"%{message_lower}%")
        ).all()
        if exact_items:
            print(f"[DEBUG] Exact/partial name match: {len(exact_items)} items")
            return [item.to_dict() for item in exact_items]

        # 2) Keyword-driven matches for Indian menu terms
        indian_terms = {
            "paneer": ["paneer"],
            "biryani": ["biryani"],
            "naan": ["naan"],
            "roti": ["roti", "chapati"],
            "paratha": ["paratha", "parantha"],
            "dal": ["dal", "dhal"],
            "chicken": ["chicken", "murgh"],
            "mutton": ["mutton", "goat", "rogan"],
            "fish": ["fish"],
            "prawn": ["prawn", "shrimp"],
            "soup": ["soup", "shorba"],
            "tikka": ["tikka"],
            "tandoori": ["tandoori"],
            "manchow": ["manchow"],
            "noodles": ["noodles", "noodle"],
            "rice": ["rice", "fried rice", "pulao"],
            "chili": ["chilli", "chili", "schezwan", "schezwan"]
        }

        for name, terms in indian_terms.items():
            if any(term in message_lower for term in terms):
                items = db.query(MenuItem).filter(
                    MenuItem.is_available == True,
                    or_(*[MenuItem.name.ilike(f"%{term}%") for term in terms])
                ).all()
                if items:
                    print(f"[DEBUG] Found {len(items)} Indian-term items for '{name}'")
                    return [item.to_dict() for item in items]

        # 3) Category search using keywords (appetizer/main/dessert/beverage)
        category_keywords = {
            'appetizer': ['starter', 'appetizer', 'snack', 'soup', 'tandoor'],
            'main': ['main', 'curry', 'meal', 'thali', 'biryani', 'rice'],
            'dessert': ['sweet', 'dessert', 'mithai', 'halwa', 'kulfi', 'gulab'],
            'beverage': ['drink', 'juice', 'chai', 'coffee', 'lassi', 'cold', 'soda']
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

        # 4) Fuzzy-ish fallback: match any single token in name or description
        tokens = [t for t in message_lower.split() if len(t) > 2]
        if tokens:
            candidates = []
            all_items = db.query(MenuItem).filter(MenuItem.is_available == True).all()
            for item in all_items:
                name = (item.name or "").lower()
                desc = (item.description or "").lower()
                match_score = sum(1 for t in tokens if t in name or t in desc)
                if match_score > 0:
                    candidates.append((match_score, item))
            candidates.sort(key=lambda x: x[0], reverse=True)
            if candidates:
                print(f"[DEBUG] Fuzzy token matches: returning {len(candidates)} items")
                return [c[1].to_dict() for c in candidates[:10]]

        # Default: return top available items (limit 10)
        print("[DEBUG] No match, returning top items")
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
