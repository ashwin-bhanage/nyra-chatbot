"""
Seed script - Add sample menu items to database
Run this once to populate the menu
"""

from app.database import SessionLocal
from app.models.menu import MenuItem, MenuCategory

def seed_menu():
    """Add sample menu items"""
    db = SessionLocal()

    # Check if menu already has items
    existing_count = db.query(MenuItem).count()
    if existing_count > 0:
        print(f"⚠️  Menu already has {existing_count} items!")
        print("Do you want to add more? (Press Ctrl+C to cancel)")
        input("Press Enter to continue...")

    print("Adding sample menu items...")

    # Sample menu items
    menu_items = [
    # ---------------- NEW INDIAN HOTEL ITEMS ----------------

    # Appetizers
    MenuItem(name="Paneer Tikka", description="Char-grilled paneer marinated in spices", category=MenuCategory.APPETIZER, price=180, is_available=True),
    MenuItem(name="Chicken Tandoori (Half)", description="Roasted chicken marinated in tandoori spices", category=MenuCategory.APPETIZER, price=260, is_available=True),
    MenuItem(name="Veg Manchurian Dry", description="Crispy veg balls tossed in spicy sauce", category=MenuCategory.APPETIZER, price=150, is_available=True),
    MenuItem(name="Chicken Lollipop", description="Crispy fried drumettes tossed in sauce", category=MenuCategory.APPETIZER, price=220, is_available=True),
    MenuItem(name="Hara Bhara Kebab", description="Spinach & pea patties", category=MenuCategory.APPETIZER, price=140, is_available=True),
    MenuItem(name="Fish Fry", description="Shallow-fried spiced fish", category=MenuCategory.APPETIZER, price=240, is_available=True),
    MenuItem(name="Chicken 65", description="South Indian spiced fried chicken", category=MenuCategory.APPETIZER, price=210, is_available=True),
    MenuItem(name="Veg Crispy", description="Fried crispy vegetables in sauce", category=MenuCategory.APPETIZER, price=160, is_available=True),

    # Main Course - Veg
    MenuItem(name="Paneer Butter Masala", description="Paneer in creamy tomato gravy", category=MenuCategory.MAIN, price=220, is_available=True),
    MenuItem(name="Dal Tadka", description="Yellow dal tempered with ghee", category=MenuCategory.MAIN, price=150, is_available=True),
    MenuItem(name="Dal Makhani", description="Slow-cooked dal with butter", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Veg Kolhapuri", description="Spicy mixed veg curry", category=MenuCategory.MAIN, price=170, is_available=True),
    MenuItem(name="Kaju Curry", description="Creamy cashew curry", category=MenuCategory.MAIN, price=250, is_available=True),
    MenuItem(name="Aloo Gobi", description="Potato & cauliflower", category=MenuCategory.MAIN, price=140, is_available=True),
    MenuItem(name="Chole Masala", description="Chickpeas in Punjabi gravy", category=MenuCategory.MAIN, price=160, is_available=True),
    MenuItem(name="Mushroom Masala", description="Mushrooms in spiced gravy", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Palak Paneer", description="Spinach-based paneer curry", category=MenuCategory.MAIN, price=210, is_available=True),
    MenuItem(name="Kadhai Paneer", description="Paneer with capsicum in kadai masala", category=MenuCategory.MAIN, price=220, is_available=True),

    # Main Course - Non-Veg
    MenuItem(name="Butter Chicken", description="Creamy tomato-based chicken curry", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Chicken Curry", description="Home-style chicken curry", category=MenuCategory.MAIN, price=220, is_available=True),
    MenuItem(name="Chicken Masala", description="Spicy chicken curry", category=MenuCategory.MAIN, price=230, is_available=True),
    MenuItem(name="Chicken Handi", description="Slow-cooked chicken handi", category=MenuCategory.MAIN, price=280, is_available=True),
    MenuItem(name="Mutton Rogan Josh", description="Kashmiri-style rich mutton curry", category=MenuCategory.MAIN, price=380, is_available=True),
    MenuItem(name="Mutton Curry", description="Traditional mutton gravy", category=MenuCategory.MAIN, price=350, is_available=True),
    MenuItem(name="Egg Curry", description="Boiled eggs in spiced gravy", category=MenuCategory.MAIN, price=140, is_available=True),

    # Rice & Biryani
    MenuItem(name="Chicken Biryani", description="Hyderabadi chicken biryani", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Mutton Biryani", description="Premium mutton biryani", category=MenuCategory.MAIN, price=380, is_available=True),
    MenuItem(name="Veg Biryani", description="Veg layered biryani", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Egg Biryani", description="Egg biryani with spices", category=MenuCategory.MAIN, price=160, is_available=True),
    MenuItem(name="Veg Pulao", description="Rice cooked with vegetables", category=MenuCategory.MAIN, price=130, is_available=True),
    MenuItem(name="Jeera Rice", description="Cumin flavored basmati", category=MenuCategory.MAIN, price=110, is_available=True),
    MenuItem(name="Steam Rice", description="Plain basmati rice", category=MenuCategory.MAIN, price=90, is_available=True),
    MenuItem(name="Curd Rice", description="South Indian curd rice", category=MenuCategory.MAIN, price=120, is_available=True),

    # Breads
    MenuItem(name="Butter Naan", description="Soft naan with butter", category=MenuCategory.MAIN, price=40, is_available=True),
    MenuItem(name="Garlic Naan", description="Naan topped with garlic", category=MenuCategory.MAIN, price=55, is_available=True),
    MenuItem(name="Tandoori Roti", description="Whole wheat tandoori roti", category=MenuCategory.MAIN, price=25, is_available=True),
    MenuItem(name="Butter Roti", description="Roti brushed with butter", category=MenuCategory.MAIN, price=30, is_available=True),
    MenuItem(name="Kulcha", description="Soft stuffed kulcha", category=MenuCategory.MAIN, price=45, is_available=True),
    MenuItem(name="Lachha Paratha", description="Layered paratha", category=MenuCategory.MAIN, price=60, is_available=True),

    # South Indian
    MenuItem(name="Masala Dosa", description="Dosa stuffed with potato masala", category=MenuCategory.MAIN, price=120, is_available=True),
    MenuItem(name="Idli Sambar", description="Idli served with sambar", category=MenuCategory.MAIN, price=90, is_available=True),
    MenuItem(name="Vada Sambar", description="Medu vada with sambar", category=MenuCategory.MAIN, price=95, is_available=True),
    MenuItem(name="Plain Dosa", description="Crispy plain dosa", category=MenuCategory.MAIN, price=80, is_available=True),
    MenuItem(name="Rava Dosa", description="Crispy rava dosa", category=MenuCategory.MAIN, price=130, is_available=True),
    MenuItem(name="Onion Uttapam", description="Uttapam topped with onions", category=MenuCategory.MAIN, price=140, is_available=True),

    # Chinese
    MenuItem(name="Veg Fried Rice", description="Veg fried rice with sauces", category=MenuCategory.MAIN, price=140, is_available=True),
    MenuItem(name="Chicken Fried Rice", description="Chicken fried rice", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Veg Noodles", description="Stir-fried veg noodles", category=MenuCategory.MAIN, price=130, is_available=True),
    MenuItem(name="Chicken Noodles", description="Noodles tossed with chicken", category=MenuCategory.MAIN, price=170, is_available=True),
    MenuItem(name="Paneer Chilli", description="Crispy paneer in chilli sauce", category=MenuCategory.APPETIZER, price=150, is_available=True),
    MenuItem(name="Chicken Chilli", description="Chicken tossed in chilli sauce", category=MenuCategory.APPETIZER, price=190, is_available=True),

    # Desserts
    MenuItem(name="Gulab Jamun", description="Warm sweet dumplings", category=MenuCategory.DESSERT, price=60, is_available=True),
    MenuItem(name="Rasmalai", description="Paneer soaked in saffron milk", category=MenuCategory.DESSERT, price=90, is_available=True),
    MenuItem(name="Kesar Kulfi", description="Saffron-flavored kulfi", category=MenuCategory.DESSERT, price=80, is_available=True),
    MenuItem(name="Ice Cream (Vanilla)", description="Vanilla scoop", category=MenuCategory.DESSERT, price=50, is_available=True),
    MenuItem(name="Chocolate Brownie Deluxe", description="Brownie with chocolate drizzle", category=MenuCategory.DESSERT, price=120, is_available=True),
    MenuItem(name="Gajar Ka Halwa", description="Carrot dessert with nuts", category=MenuCategory.DESSERT, price=80, is_available=True),
    MenuItem(name="Tiramisu (Premium)", description="Italian tiramisu slice", category=MenuCategory.DESSERT, price=160, is_available=True),

    # Beverages
    MenuItem(name="Masala Chai", description="Indian masala tea", category=MenuCategory.BEVERAGE, price=20, is_available=True),
    MenuItem(name="Cold Coffee", description="Cold coffee milkshake", category=MenuCategory.BEVERAGE, price=110, is_available=True),
    MenuItem(name="Fresh Lime Soda", description="Lemon soda sweet or salty", category=MenuCategory.BEVERAGE, price=80, is_available=True),
    MenuItem(name="Coca Cola Bottle", description="Chilled Coke", category=MenuCategory.BEVERAGE, price=40, is_available=True),
    MenuItem(name="Mineral Water", description="Packaged drinking water", category=MenuCategory.BEVERAGE, price=30, is_available=True),
    MenuItem(name="Sweet Lassi", description="Sweet yogurt drink", category=MenuCategory.BEVERAGE, price=60, is_available=True),
    MenuItem(name="Salted Lassi", description="Salted yogurt drink", category=MenuCategory.BEVERAGE, price=50, is_available=True),
    MenuItem(name="Mango Shake", description="Mango milkshake blend", category=MenuCategory.BEVERAGE, price=120, is_available=True),

]


    try:
        # Add all items to database
        db.add_all(menu_items)
        db.commit()

        print(f"\n✅ Successfully added {len(menu_items)} menu items!")
        print("\nMenu Summary:")
        print(f"  - Appetizers: 3 items")
        print(f"  - Main Course: 5 items")
        print(f"  - Desserts: 3 items")
        print(f"  - Beverages: 3 items")
        print(f"\nTotal: {len(menu_items)} items")

    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_menu()
