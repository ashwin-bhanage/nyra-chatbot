"""
Seed script - Real Indian Restaurant/Hotel Menu
Run this to replace the menu with authentic items
"""

from app.database import SessionLocal
from app.models.menu import MenuItem, MenuCategory
from app.models.order import Order, OrderItem
from app.models.chat_log import ChatLog

def clear_all_data(db):
    """Clear existing data in correct order (respecting foreign keys)"""
    print("🗑️  Clearing existing data...")

    # 1. First delete order_items (child of orders and menu_items)
    db.query(OrderItem).delete()
    print("   ✅ Cleared order_items")

    # 2. Delete orders (child of users)
    db.query(Order).delete()
    print("   ✅ Cleared orders")

    # 3. Delete chat_logs
    db.query(ChatLog).delete()
    print("   ✅ Cleared chat_logs")

    # 4. Now we can safely delete menu_items
    db.query(MenuItem).delete()
    print("   ✅ Cleared menu_items")

    db.commit()
    print("✅ All data cleared successfully!")

def seed_real_menu():
    """Add real Indian restaurant menu items"""
    db = SessionLocal()

    # Clear existing data
    clear_all_data(db)

    print("Adding real restaurant menu items...")

    menu_items = [

        # ========== STARTERS / APPETIZERS ==========
        MenuItem(name="Paneer Tikka", description="Marinated cottage cheese cubes grilled in tandoor with spices", category=MenuCategory.APPETIZER, price=220, is_available=True),
        MenuItem(name="Chicken Tikka", description="Tender chicken pieces marinated in yogurt & spices, char-grilled", category=MenuCategory.APPETIZER, price=260, is_available=True),
        MenuItem(name="Veg Spring Rolls", description="Crispy rolls stuffed with mixed vegetables, served with chutney", category=MenuCategory.APPETIZER, price=140, is_available=True),
        MenuItem(name="Chicken 65", description="Spicy deep-fried chicken with curry leaves & red chilies", category=MenuCategory.APPETIZER, price=240, is_available=True),
        MenuItem(name="Fish Amritsari", description="Crispy fried fish fillets with Punjabi spices", category=MenuCategory.APPETIZER, price=280, is_available=True),
        MenuItem(name="Samosa (2 pcs)", description="Crispy pastry filled with spiced potatoes & peas", category=MenuCategory.APPETIZER, price=40, is_available=True),
        MenuItem(name="Onion Bhaji", description="Crispy onion fritters with gram flour & spices", category=MenuCategory.APPETIZER, price=70, is_available=True),
        MenuItem(name="Tandoori Prawns", description="Jumbo prawns marinated & grilled in tandoor", category=MenuCategory.APPETIZER, price=380, is_available=True),

        # ========== MAIN COURSE - VEG ==========
        MenuItem(name="Paneer Butter Masala", description="Cottage cheese in rich tomato & butter gravy", category=MenuCategory.MAIN, price=240, is_available=True),
        MenuItem(name="Dal Makhani", description="Black lentils slow-cooked with cream & butter", category=MenuCategory.MAIN, price=180, is_available=True),
        MenuItem(name="Palak Paneer", description="Cottage cheese cubes in creamy spinach gravy", category=MenuCategory.MAIN, price=220, is_available=True),
        MenuItem(name="Veg Biryani", description="Aromatic basmati rice with mixed vegetables & spices", category=MenuCategory.MAIN, price=180, is_available=True),
        MenuItem(name="Chole Bhature", description="Spiced chickpea curry with fluffy fried bread", category=MenuCategory.MAIN, price=150, is_available=True),
        MenuItem(name="Malai Kofta", description="Fried paneer dumplings in creamy tomato gravy", category=MenuCategory.MAIN, price=230, is_available=True),
        MenuItem(name="Aloo Gobi", description="Potatoes & cauliflower cooked with turmeric & spices", category=MenuCategory.MAIN, price=140, is_available=True),

        # ========== MAIN COURSE - NON-VEG ==========
        MenuItem(name="Butter Chicken", description="Tender chicken in rich tomato, butter & cream gravy", category=MenuCategory.MAIN, price=280, is_available=True),
        MenuItem(name="Chicken Biryani", description="Fragrant basmati rice layered with spiced chicken", category=MenuCategory.MAIN, price=260, is_available=True),
        MenuItem(name="Mutton Rogan Josh", description="Kashmiri style lamb curry with aromatic spices", category=MenuCategory.MAIN, price=380, is_available=True),
        MenuItem(name="Hyderabadi Biryani", description="Authentic dum-style biryani with tender mutton", category=MenuCategory.MAIN, price=350, is_available=True),
        MenuItem(name="Fish Curry", description="Fresh fish cooked in tangy coconut curry", category=MenuCategory.MAIN, price=240, is_available=True),
        MenuItem(name="Chicken Tikka Masala", description="Grilled chicken in spiced tomato & onion gravy", category=MenuCategory.MAIN, price=270, is_available=True),
        MenuItem(name="Prawn Masala", description="Succulent prawns in rich onion-tomato masala", category=MenuCategory.MAIN, price=340, is_available=True),
        MenuItem(name="Keema Matar", description="Minced lamb cooked with green peas & spices", category=MenuCategory.MAIN, price=290, is_available=True),

        # ========== BREADS ==========
        MenuItem(name="Butter Naan", description="Soft leavened bread brushed with butter", category=MenuCategory.APPETIZER, price=40, is_available=True),
        MenuItem(name="Garlic Naan", description="Naan topped with garlic & coriander", category=MenuCategory.APPETIZER, price=55, is_available=True),
        MenuItem(name="Tandoori Roti", description="Whole wheat bread baked in tandoor", category=MenuCategory.APPETIZER, price=20, is_available=True),
        MenuItem(name="Cheese Naan", description="Naan stuffed with melted cheese", category=MenuCategory.APPETIZER, price=70, is_available=True),
        MenuItem(name="Laccha Paratha", description="Layered whole wheat flaky bread", category=MenuCategory.APPETIZER, price=45, is_available=True),

        # ========== RICE ==========
        MenuItem(name="Jeera Rice", description="Basmati rice tempered with cumin seeds", category=MenuCategory.MAIN, price=120, is_available=True),
        MenuItem(name="Steamed Basmati Rice", description="Plain steamed long-grain basmati rice", category=MenuCategory.MAIN, price=90, is_available=True),

        # ========== DESSERTS ==========
        MenuItem(name="Gulab Jamun (2 pcs)", description="Deep-fried milk dumplings soaked in rose syrup", category=MenuCategory.DESSERT, price=60, is_available=True),
        MenuItem(name="Rasmalai", description="Soft paneer patties in sweetened saffron milk", category=MenuCategory.DESSERT, price=90, is_available=True),
        MenuItem(name="Kheer", description="Traditional rice pudding with cardamom & nuts", category=MenuCategory.DESSERT, price=70, is_available=True),
        MenuItem(name="Gajar Ka Halwa", description="Warm carrot pudding with ghee & dry fruits", category=MenuCategory.DESSERT, price=80, is_available=True),
        MenuItem(name="Kulfi", description="Traditional Indian ice cream with pistachios", category=MenuCategory.DESSERT, price=60, is_available=True),
        MenuItem(name="Jalebi", description="Crispy pretzel-shaped sweets soaked in sugar syrup", category=MenuCategory.DESSERT, price=50, is_available=True),
        MenuItem(name="Ras Malai Cake", description="Fusion dessert - sponge cake with rasmalai flavors", category=MenuCategory.DESSERT, price=150, is_available=True),

        # ========== BEVERAGES ==========
        MenuItem(name="Masala Chai", description="Traditional spiced Indian tea with milk", category=MenuCategory.BEVERAGE, price=20, is_available=True),
        MenuItem(name="Mango Lassi", description="Creamy yogurt drink blended with mango", category=MenuCategory.BEVERAGE, price=80, is_available=True),
        MenuItem(name="Sweet Lassi", description="Traditional sweetened yogurt drink", category=MenuCategory.BEVERAGE, price=60, is_available=True),
        MenuItem(name="Salted Lassi", description="Refreshing salted yogurt drink with cumin", category=MenuCategory.BEVERAGE, price=50, is_available=True),
        MenuItem(name="Fresh Lime Soda", description="Refreshing lime juice with soda (sweet/salt)", category=MenuCategory.BEVERAGE, price=70, is_available=True),
        MenuItem(name="Rose Falooda", description="Rose syrup milkshake with vermicelli & basil seeds", category=MenuCategory.BEVERAGE, price=120, is_available=True),
        MenuItem(name="Masala Buttermilk", description="Spiced buttermilk with mint & cumin", category=MenuCategory.BEVERAGE, price=30, is_available=True),
        MenuItem(name="Nimbu Pani", description="Fresh Indian-style lemonade", category=MenuCategory.BEVERAGE, price=30, is_available=True),
        MenuItem(name="Cold Coffee", description="Chilled coffee with ice cream", category=MenuCategory.BEVERAGE, price=120, is_available=True),
        MenuItem(name="Thandai", description="Chilled milk with nuts, saffron & rose petals", category=MenuCategory.BEVERAGE, price=110, is_available=True),
    ]

    try:
        db.add_all(menu_items)
        db.commit()

        # Count by category
        appetizers = sum(1 for i in menu_items if i.category == MenuCategory.APPETIZER)
        mains = sum(1 for i in menu_items if i.category == MenuCategory.MAIN)
        desserts = sum(1 for i in menu_items if i.category == MenuCategory.DESSERT)
        beverages = sum(1 for i in menu_items if i.category == MenuCategory.BEVERAGE)

        print(f"\n✅ Successfully added {len(menu_items)} menu items!")
        print("\n🍽️  Menu Summary:")
        print(f"  📍 Starters/Breads: {appetizers} items")
        print(f"  🍛 Main Course: {mains} items")
        print(f"  🍨 Desserts: {desserts} items")
        print(f"  🥤 Beverages: {beverages} items")
        print(f"\n  Total: {len(menu_items)} items")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🍛 REAL INDIAN RESTAURANT MENU SETUP")
    print("="*50)
    seed_real_menu()
    print("\n" + "="*50)
    print("✅ Menu setup complete!")
    print("="*50)
