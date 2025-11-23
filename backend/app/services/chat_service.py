"""
Chat Service - COMPLETE VERSION with Order & Reservation Support (CLEANED)
"""

from sqlalchemy.orm import Session
from app.models.chat_log import ChatLog
from app.models.user import User
from app.models.menu import MenuItem
from app.services.gemini_service import gemini_service
from app.services.reservation_service import reservation_service
from app.schemas.reservation import ReservationCreate
from typing import Dict, Any, Optional, List
from datetime import datetime
import re


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

        try:
            # Ensure user exists
            if phone_number and not user_id:
                user = self._get_or_create_user(db, phone_number)
                user_id = user.id

            chat_history = self._get_chat_history(db, session_id)
            intent = self._detect_intent(user_message)
            print(f"[DEBUG] Intent detected: {intent}")

            # Intent routing
            if intent == 'checkout_intent':
                # Don't extract items, just show a message
                result = {
                    "response": "Great! Your cart is ready for checkout. Please review your items and click 'Place Order' when ready!",
                    "intent": "checkout_intent",
                    "session_id": session_id,
                    "user_id": user_id,
                    "menu_items": [],
                    "cart_items": [],
                    "action": "show_cart"
                }

            elif intent == 'order_intent':
                result = await self._handle_order_intent(db, user_message, user_id, phone_number, chat_history)

            elif intent == 'reservation_intent':
                result = await self._handle_reservation_intent(db, user_message, user_id, phone_number, chat_history)

            else:
                menu_items = self._get_relevant_menu_items(db, user_message) if intent == 'menu_query' else []

                ai = await gemini_service.generate_response(
                    user_message=user_message,
                    menu_items=menu_items or None,
                    chat_history=chat_history
                )

                result = {
                    "response": ai['response'],
                    "intent": intent,
                    "session_id": session_id,
                    "user_id": user_id,
                    "menu_items": menu_items,
                    "cart_items": [],
                    "action": None
                }

            result["session_id"] = session_id
            self._save_chat_log(db, user_id, session_id, user_message, result["response"], intent)

            return result

        except Exception as e:
            print("[ERROR] process_message:", e)
            return {
                "response": "I'm having trouble processing your request.",
                "intent": "error",
                "session_id": session_id,
                "user_id": user_id,
                "menu_items": [],
                "cart_items": [],
                "action": "error"
            }

    def _detect_intent(self, message: str) -> str:
        """Detect user intent from message"""
        m = (message or "").lower()

        if not m:
            return 'general_query'

        # Greetings
        if any(m.startswith(g) for g in ['hi', 'hello', 'hey']):
            return 'greeting'

        # CHECKOUT/CART VIEW (check BEFORE order_intent!)
        checkout_keywords = [
            'checkout', 'check out', 'place order', 'complete order', 'finalize',
            'proceed', 'confirm', 'ready to order', 'done ordering', "that's all",
            'show cart', 'view cart', 'see cart', 'my cart', 'what did i order',
            'cart', 'bill', 'total', 'summary'
        ]
        if any(k in m for k in checkout_keywords):
            return 'checkout_intent'

        # Strong order keywords
        order_keywords = [
            'add', 'want', 'give me', 'get me', "i'll have", "i'd like",
            "i'll take", 'buy', 'can i get', 'can i have', 'please add', 'i need'
        ]
        if any(k in m for k in order_keywords):
            return 'order_intent'

        # Broad food vocabulary
        food_words = [
            'veg', 'vegetable', 'soup', 'hot & sour', 'hot and sour', 'tomato',
            'biryani', 'naan', 'roti', 'chicken', 'paneer', 'dal', 'curry',
            'rice', 'noodles', 'tikka', 'kebab', 'samosa', 'dessert',
            'sweet', 'ice cream', 'kulfi', 'lassi', 'chai'
        ]
        if any(f in m for f in food_words):
            return 'order_intent'

        # Number + food → order
        if re.search(r'\d+', m) and any(f in m for f in food_words):
            return 'order_intent'

        # Reservation
        if any(k in m for k in ['book', 'reserve', 'reservation', 'table for']):
            return 'reservation_intent'

        # FAQ
        if any(k in m for k in ['hours', 'open', 'close', 'delivery', 'payment', 'location']):
            return 'faq'

        # Menu browsing
        if any(k in m for k in ['menu', 'items', 'show', 'food']):
            return 'menu_query'

        return 'general_query'

    async def _handle_order_intent(
        self,
        db: Session,
        user_message: str,
        user_id: Optional[int],
        phone_number: Optional[str],
        chat_history: List[Dict]
    ) -> Dict[str, Any]:
        """Handle order placement through chat"""

        print("[DEBUG] _handle_order_intent called")

        try:
            # Fetch menu
            menu_rows = db.query(MenuItem).filter(MenuItem.is_available == True).all()
            menu_items = [item.to_dict() for item in menu_rows]

            # Extract items
            extraction_result = await gemini_service.extract_order_items(user_message, menu_items)
            print(f"[DEBUG] Extraction result: {extraction_result}")

            if not extraction_result['success']:
                return self._order_show_suggestions(db, user_message, user_id)

            order_data = extraction_result.get('data', {})
            confidence = order_data.get('confidence', 'low')
            items_list = order_data.get('items', [])

            if confidence == 'low' or not items_list:
                return self._order_show_suggestions(db, user_message, user_id)

            cart_items = []
            total_amount = 0.0

            # Match extracted items to menu
            for extracted in items_list:
                item_id = extracted.get('item_id')
                item_name = (extracted.get('item_name') or "").strip().lower()
                quantity = extracted.get('quantity', 1)

                # ID match first
                menu_item = next((m for m in menu_items if m['id'] == item_id), None)

                # Exact name match
                if not menu_item and item_name:
                    menu_item = next((m for m in menu_items if m['name'].strip().lower() == item_name), None)

                # Substring match
                if not menu_item and item_name:
                    menu_item = next((m for m in menu_items if item_name in m['name'].strip().lower()), None)

                if not menu_item:
                    print(f"[DEBUG] No match for '{item_name}' (id={item_id})")
                    continue

                try:
                    quantity = int(quantity) if str(quantity).isdigit() else 1
                except Exception:
                    quantity = 1

                price = float(menu_item['price'])
                cart_items.append({
                    "id": menu_item['id'],
                    "name": menu_item['name'],
                    "price": price,
                    "quantity": quantity,
                    "description": menu_item.get('description', '')
                })

                total_amount += price * quantity
                print(f"[DEBUG] Added to cart: {menu_item['name']} x {quantity}")

            if not cart_items:
                return self._order_show_suggestions(db, user_message, user_id)

            items_text = "\n".join(
                f"✓ {c['quantity']}x {c['name']} @ ₹{c['price']}" for c in cart_items
            )

            response_text = (
                f"Added to cart! 🛒\n\n{items_text}\n\n"
                f"💰 Subtotal: ₹{total_amount:.2f}\n\n"
                "Want to add more items or checkout?"
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
            print("[ERROR] _handle_order_intent failed:", e)
            import traceback
            traceback.print_exc()
            return self._order_show_suggestions(db, user_message, user_id)

    def _order_show_suggestions(self, db, msg, user_id):
        """Show menu items when order is ambiguous"""
        relevant = self._get_relevant_menu_items(db, msg)[:8]

        if relevant:
            items_text = "\n".join([
                f"• {item['name']} - ₹{item['price']}"
                for item in relevant
            ])

            # Extract category from message
            category = "available"
            if "biryani" in msg.lower():
                category = "biryani"
            elif "dessert" in msg.lower() or "sweet" in msg.lower():
                category = "dessert"
            elif "beverage" in msg.lower() or "drink" in msg.lower():
                category = "beverage"
            elif "naan" in msg.lower() or "roti" in msg.lower():
                category = "bread"

            response = (
                f"Here are our {category} options:\n\n"
                f"{items_text}\n\n"
                "Which one would you like? Just say like '2 Chicken Biryani' or 'Add 1 Butter Naan'"
            )
        else:
            response = (
                "I'd love to help you order! Try saying:\n"
                "• 'Add 2 Chicken Biryani'\n"
                "• '1 Paneer Tikka'\n"
                "• 'Show me desserts'"
            )

        return {
            "response": response,
            "intent": "order_intent",
            "session_id": "",
            "user_id": user_id,
            "menu_items": relevant,
            "cart_items": [],
            "action": "showing_menu"
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

        try:
            extraction = await gemini_service.extract_reservation_details(user_message)

            if not extraction['success'] or extraction['data'].get('confidence') == 'low':
                return {
                    "response": (
                        "I'd be happy to help you make a reservation! Please provide:\n"
                        "- Date\n- Time\n- Number of people\n\n"
                        "Example: 'Table for 4 on November 20 at 7 PM'"
                    ),
                    "intent": "reservation_intent",
                    "session_id": "",
                    "user_id": user_id,
                    "menu_items": [],
                    "cart_items": [],
                    "action": "clarification_needed"
                }

            d = extraction['data']
            reservation_create = ReservationCreate(
                user_id=user_id,
                phone_number=phone_number,
                reservation_date=datetime.fromisoformat(d['date']).date(),
                reservation_time=datetime.fromisoformat(f"2025-01-01T{d['time']}").time(),
                party_size=d['party_size'],
                special_requests=d.get('special_requests')
            )

            reservation = reservation_service.create_reservation(db, reservation_create)
            summary = reservation_service.generate_reservation_summary(reservation)

            return {
                "response": f"Perfect! Your reservation is confirmed! ✅\n\n{summary}",
                "intent": "reservation_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "cart_items": [],
                "action": "reservation_created",
                "reservation_id": reservation.id
            }

        except Exception as e:
            print("[ERROR] Reservation failed:", e)
            return {
                "response": "Sorry, there was an issue making your reservation. Please try again.",
                "intent": "reservation_intent",
                "session_id": "",
                "user_id": user_id,
                "menu_items": [],
                "cart_items": [],
                "action": "reservation_failed"
            }

    def _get_or_create_user(self, db: Session, phone_number: str) -> User:
        """Get or create user"""
        user = db.query(User).filter(User.phone_number == phone_number).first()
        if not user:
            user = User(phone_number=phone_number)
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    def _get_chat_history(self, db: Session, session_id: str, limit: int = 5):
        """Get recent chat history"""
        logs = (
            db.query(ChatLog)
            .filter(ChatLog.session_id == session_id)
            .order_by(ChatLog.timestamp.desc())
            .limit(limit)
            .all()
        )
        return [{"user_message": l.user_message, "bot_response": l.bot_response} for l in reversed(logs)]

    def _get_relevant_menu_items(self, db: Session, message: str):
        """Returns menu items based on keyword or category"""
        from sqlalchemy import cast, String, or_

        m = (message or "").lower().strip()

        # PRIORITY 1: Check SPECIFIC food items FIRST
        keyword_terms = {
            'biryani': 'biryani',
            'naan': 'naan',
            'roti': 'roti',
            'chicken': 'chicken',
            'paneer': 'paneer',
            'dal': 'dal',
            'tikka': 'tikka',
            'kulfi': 'kulfi',
            'lassi': 'lassi',
            'chai': 'chai',
            'soup': 'soup',
            'samosa': 'samosa',
            'kebab': 'kebab',
            'korma': 'korma',
            'butter': 'butter',
            'garlic': 'garlic'
        }

        # Search for specific items
        for key, search_term in keyword_terms.items():
            if key in m:
                rows = db.query(MenuItem).filter(
                    MenuItem.is_available == True,
                    or_(
                        MenuItem.name.ilike(f"%{search_term}%"),
                        MenuItem.description.ilike(f"%{search_term}%")
                    )
                ).all()

                if rows:
                    print(f"[DEBUG] Found {len(rows)} items matching '{search_term}'")
                    return [r.to_dict() for r in rows]

        # PRIORITY 2: Category search
        category_mapping = {
            "APPETIZER": ["starter", "starters", "appetizer", "appetizers", "snacks", "tandoori"],
            "MAIN": ["main", "mains", "curry", "curries", "gravy"],
            "DESSERT": ["dessert", "desserts", "sweet", "sweets", "ice cream", "halwa", "gulab", "ras", "jalebi"],
            "BEVERAGE": ["drink", "drinks", "beverage", "beverages", "coffee", "juice", "soda"],
        }

        for category_key, keywords in category_mapping.items():
            if any(k in m for k in keywords):
                rows = db.query(MenuItem).filter(
                    cast(MenuItem.category, String).ilike(category_key),
                    MenuItem.is_available == True
                ).all()
                if rows:
                    print(f"[DEBUG] Found {len(rows)} items in category '{category_key}'")
                    return [r.to_dict() for r in rows]

        # PRIORITY 3: Fallback
        print("[DEBUG] No match, returning first 8 items")
        rows = db.query(MenuItem).filter(MenuItem.is_available == True).limit(8).all()
        return [r.to_dict() for r in rows]

    def _save_chat_log(self, db: Session, user_id, session_id, user_message, bot_response, intent):
        """Save chat to database"""
        entry = ChatLog(
            user_id=user_id,
            session_id=session_id,
            user_message=user_message,
            bot_response=bot_response,
            intent=intent
        )
        db.add(entry)
        db.commit()


# singleton
chat_service = ChatService()
