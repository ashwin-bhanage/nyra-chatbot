"""
Seed script - Full Indian restaurant menu (grouped)
Drop/clear dependent data and insert a comprehensive menu
Prices are in Indian Rupees (integers)
No images (image_url = None)
"""

from app.database import SessionLocal
from app.models.menu import MenuItem, MenuCategory
from app.models.order import Order, OrderItem
from app.models.chat_log import ChatLog

def clear_all_data(db):
    """Clear existing data in correct order (respecting foreign keys)"""
    print("🗑️  Clearing existing data...")

    # delete children first
    try:
        deleted = db.query(OrderItem).delete()
        print(f"   ✅ Cleared order_items ({deleted} rows)")
    except Exception as e:
        print(f"   ⚠️ order_items delete error: {e}")

    try:
        deleted = db.query(Order).delete()
        print(f"   ✅ Cleared orders ({deleted} rows)")
    except Exception as e:
        print(f"   ⚠️ orders delete error: {e}")

    try:
        deleted = db.query(ChatLog).delete()
        print(f"   ✅ Cleared chat_logs ({deleted} rows)")
    except Exception as e:
        print(f"   ⚠️ chat_logs delete error: {e}")

    try:
        deleted = db.query(MenuItem).delete()
        print(f"   ✅ Cleared menu_items ({deleted} rows)")
    except Exception as e:
        print(f"   ⚠️ menu_items delete error: {e}")

    db.commit()
    print("✅ All specified data cleared successfully!\n")


def seed_real_menu():
    db = SessionLocal()

    # Clear existing data first
    clear_all_data(db)

    print("Adding real restaurant menu items...")

    # ===== Helper: price choices per section (INR, integers) =====
    # We'll choose realistic fixed prices for each item below.

    menu_items = [

    # =====================================================================
    # 🥣 SOUPS (STARTERS / APPETIZERS)
    # =====================================================================
    MenuItem(name="Tomato Shorba", description="Mildly spiced tomato broth.", category=MenuCategory.APPETIZER, price=80, is_available=True),
    MenuItem(name="Dal Shorba", description="Rich lentil soup.", category=MenuCategory.APPETIZER, price=90, is_available=True),
    MenuItem(name="Veg Manchow Soup", description="Hot Indo-Chinese soup with crispy noodles.", category=MenuCategory.APPETIZER, price=120, is_available=True),
    MenuItem(name="Chicken Manchow Soup", description="Manchow soup with shredded chicken.", category=MenuCategory.APPETIZER, price=140, is_available=True),
    MenuItem(name="Veg Hot & Sour Soup", description="Tangy spicy soup with vegetables.", category=MenuCategory.APPETIZER, price=120, is_available=True),
    MenuItem(name="Chicken Hot & Sour Soup", description="Hot and sour chicken broth.", category=MenuCategory.APPETIZER, price=150, is_available=True),
    MenuItem(name="Sweet Corn Veg Soup", description="Mild creamy sweet corn soup.", category=MenuCategory.APPETIZER, price=110, is_available=True),
    MenuItem(name="Sweet Corn Chicken Soup", description="Chicken and sweetcorn soup.", category=MenuCategory.APPETIZER, price=130, is_available=True),

    # =====================================================================
    # 🧆 VEG STARTERS
    # =====================================================================
    MenuItem(name="Paneer Tikka (Malai/Achari)", description="Marinated grilled cottage cheese.", category=MenuCategory.APPETIZER, price=240, is_available=True),
    MenuItem(name="Tandoori Aloo", description="Roasted potatoes with spices.", category=MenuCategory.APPETIZER, price=150, is_available=True),
    MenuItem(name="Veg Seekh Kebab", description="Minced vegetable kebabs.", category=MenuCategory.APPETIZER, price=150, is_available=True),
    MenuItem(name="Veg Pakora", description="Fritters made with mixed vegetables.", category=MenuCategory.APPETIZER, price=90, is_available=True),
    MenuItem(name="Paneer Pakora", description="Deep-fried paneer fritters.", category=MenuCategory.APPETIZER, price=130, is_available=True),
    MenuItem(name="Aloo Tikki Chaat", description="Crispy tikki with chutneys.", category=MenuCategory.APPETIZER, price=110, is_available=True),
    MenuItem(name="Hara Bhara Kebab", description="Green peas-spinach kebabs.", category=MenuCategory.APPETIZER, price=160, is_available=True),
    MenuItem(name="Dahi Ke Kebab", description="Yogurt-based creamy kebabs.", category=MenuCategory.APPETIZER, price=180, is_available=True),
    MenuItem(name="Samosa (2 pcs)", description="Fried pastry with potato filling.", category=MenuCategory.APPETIZER, price=40, is_available=True),
    MenuItem(name="Corn Cheese Balls", description="Cheesy corn-filled fried balls.", category=MenuCategory.APPETIZER, price=130, is_available=True),
    MenuItem(name="Tandoori Mushroom", description="Spicy marinated mushroom tikka.", category=MenuCategory.APPETIZER, price=180, is_available=True),

    # =====================================================================
    # 🍗 NON-VEG STARTERS
    # =====================================================================
    MenuItem(name="Chicken Tikka", description="Boneless chicken grilled with spices.", category=MenuCategory.APPETIZER, price=260, is_available=True),
    MenuItem(name="Chicken 65", description="Crispy spicy fried chicken bites.", category=MenuCategory.APPETIZER, price=230, is_available=True),
    MenuItem(name="Tandoori Chicken (Half)", description="Classic tandoor roasted chicken.", category=MenuCategory.APPETIZER, price=280, is_available=True),
    MenuItem(name="Mutton Seekh Kebab", description="Juicy minced lamb kebabs.", category=MenuCategory.APPETIZER, price=330, is_available=True),
    MenuItem(name="Amritsari Fish Fry", description="Spicy fried fish with gram flour.", category=MenuCategory.APPETIZER, price=300, is_available=True),
    MenuItem(name="Chicken Lollipop", description="Crispy chicken drumettes.", category=MenuCategory.APPETIZER, price=260, is_available=True),
    MenuItem(name="Prawn Koliwada", description="Crispy, tangy fried prawns.", category=MenuCategory.APPETIZER, price=360, is_available=True),

    # =====================================================================
    # 🍜 INDO-CHINESE (MAINS)
    # =====================================================================
    MenuItem(name="Veg Spring Rolls", description="Crispy vegetable rolls.", category=MenuCategory.MAIN, price=150, is_available=True),
    MenuItem(name="Chicken Spring Rolls", description="Crispy chicken rolls.", category=MenuCategory.MAIN, price=180, is_available=True),

    MenuItem(name="Chilli Paneer Dry", description="Paneer tossed in chilli sauce.", category=MenuCategory.MAIN, price=220, is_available=True),
    MenuItem(name="Chilli Chicken Dry", description="Fried chicken tossed in chilli sauce.", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Gobi Manchurian Dry", description="Crispy cauliflower in Manchurian sauce.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Chicken Manchurian", description="Chicken balls in brown gravy.", category=MenuCategory.MAIN, price=260, is_available=True),

    MenuItem(name="Veg Fried Rice", description="Chinese-style fried rice.", category=MenuCategory.MAIN, price=150, is_available=True),
    MenuItem(name="Egg Fried Rice", description="Rice tossed with eggs.", category=MenuCategory.MAIN, price=160, is_available=True),
    MenuItem(name="Chicken Fried Rice", description="Fried rice with shredded chicken.", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Schezwan Veg Fried Rice", description="Spicy red fried rice.", category=MenuCategory.MAIN, price=170, is_available=True),
    MenuItem(name="Schezwan Chicken Fried Rice", description="Fiery fried rice with chicken.", category=MenuCategory.MAIN, price=210, is_available=True),

    MenuItem(name="Veg Hakka Noodles", description="Stir-fried noodles with vegetables.", category=MenuCategory.MAIN, price=160, is_available=True),
    MenuItem(name="Chicken Hakka Noodles", description="Noodles with chicken strips.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Schezwan Noodles", description="Spicy Indo-Chinese noodles.", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Schezwan Chicken Noodles", description="Fiery red chicken noodles.", category=MenuCategory.MAIN, price=220, is_available=True),

    MenuItem(name="Veg Manchurian Gravy", description="Veg dumplings in gravy.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Chicken Chilli Garlic", description="Chicken in garlic-chilli sauce.", category=MenuCategory.MAIN, price=260, is_available=True),

    # =====================================================================
    # 🍛 MAIN COURSE – VEG
    # =====================================================================
    MenuItem(name="Paneer Butter Masala", description="Creamy tomato-based paneer curry.", category=MenuCategory.MAIN, price=240, is_available=True),
    MenuItem(name="Paneer Lababdar", description="Rich and thick gravy paneer.", category=MenuCategory.MAIN, price=250, is_available=True),
    MenuItem(name="Kadhai Paneer", description="Paneer with capsicum & spices.", category=MenuCategory.MAIN, price=240, is_available=True),
    MenuItem(name="Shahi Paneer", description="Paneer simmered in cashew gravy.", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Palak Paneer", description="Paneer in creamy spinach gravy.", category=MenuCategory.MAIN, price=220, is_available=True),
    MenuItem(name="Matar Paneer", description="Green peas & paneer curry.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Malai Kofta", description="Rich kofta in creamy gravy.", category=MenuCategory.MAIN, price=240, is_available=True),
    MenuItem(name="Navratan Korma", description="Mixed veg in sweet mild gravy.", category=MenuCategory.MAIN, price=220, is_available=True),
    MenuItem(name="Veg Kolhapuri", description="Spicy thick Maharashtrian curry.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Mix Veg Curry", description="Classic mixed vegetable curry.", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Baingan Bharta", description="Smoky roasted eggplant mash.", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Dum Aloo Kashmiri", description="Baby potatoes in rich gravy.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Chole Masala", description="Punjabi-style chickpeas.", category=MenuCategory.MAIN, price=150, is_available=True),

    # =====================================================================
    # 🍗 MAIN COURSE – NON-VEG
    # =====================================================================
    MenuItem(name="Butter Chicken", description="Creamy tomato chicken curry.", category=MenuCategory.MAIN, price=300, is_available=True),
    MenuItem(name="Chicken Curry (Home Style)", description="Traditional Indian chicken curry.", category=MenuCategory.MAIN, price=240, is_available=True),
    MenuItem(name="Kadai Chicken", description="Chicken cooked with onions & capsicum.", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Chicken Tikka Masala", description="Chicken tikka in spicy masala gravy.", category=MenuCategory.MAIN, price=280, is_available=True),
    MenuItem(name="Pepper Chicken", description="South Indian pepper chicken.", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Egg Curry", description="Boiled eggs in masala gravy.", category=MenuCategory.MAIN, price=160, is_available=True),
    MenuItem(name="Mutton Curry", description="Slow-cooked mutton curry.", category=MenuCategory.MAIN, price=380, is_available=True),
    MenuItem(name="Rogan Josh", description="Kashmiri aromatic lamb curry.", category=MenuCategory.MAIN, price=380, is_available=True),
    MenuItem(name="Prawn Curry", description="Prawns cooked in coconut gravy.", category=MenuCategory.MAIN, price=340, is_available=True),

    # =====================================================================
    # 🍚 RICE & BIRYANI
    # =====================================================================
    MenuItem(name="Steamed Rice", description="Plain basmati rice.", category=MenuCategory.MAIN, price=80, is_available=True),
    MenuItem(name="Jeera Rice", description="Cumin-flavoured rice.", category=MenuCategory.MAIN, price=110, is_available=True),
    MenuItem(name="Veg Pulao", description="Flavoured rice with vegetables.", category=MenuCategory.MAIN, price=140, is_available=True),
    MenuItem(name="Kashmiri Pulao", description="Sweet aromatic pulao.", category=MenuCategory.MAIN, price=200, is_available=True),

    MenuItem(name="Veg Biryani", description="Aromatic dum biryani.", category=MenuCategory.MAIN, price=200, is_available=True),
    MenuItem(name="Egg Biryani", description="Biryani with boiled eggs.", category=MenuCategory.MAIN, price=180, is_available=True),
    MenuItem(name="Chicken Biryani", description="Hyderabadi dum biryani.", category=MenuCategory.MAIN, price=260, is_available=True),
    MenuItem(name="Mutton Biryani", description="Rich and spicy mutton biryani.", category=MenuCategory.MAIN, price=350, is_available=True),

    # =====================================================================
    # 🍞 INDIAN BREADS
    # =====================================================================
    MenuItem(name="Tandoori Roti", description="Whole wheat tandoor roti.", category=MenuCategory.MAIN, price=20, is_available=True),
    MenuItem(name="Butter Roti", description="Tandoori roti brushed with butter.", category=MenuCategory.MAIN, price=25, is_available=True),
    MenuItem(name="Plain Naan", description="Classic tandoor-baked naan.", category=MenuCategory.MAIN, price=30, is_available=True),
    MenuItem(name="Butter Naan", description="Soft naan brushed with butter.", category=MenuCategory.MAIN, price=40, is_available=True),
    MenuItem(name="Garlic Naan", description="Naan topped with garlic.", category=MenuCategory.MAIN, price=50, is_available=True),
    MenuItem(name="Lachha Paratha", description="Layered whole wheat paratha.", category=MenuCategory.MAIN, price=60, is_available=True),
    MenuItem(name="Aloo Paratha", description="Potato-stuffed paratha.", category=MenuCategory.MAIN, price=80, is_available=True),
    MenuItem(name="Paneer Paratha", description="Stuffed paratha with paneer.", category=MenuCategory.MAIN, price=100, is_available=True),
    MenuItem(name="Cheese Naan", description="Cheese-stuffed naan.", category=MenuCategory.MAIN, price=120, is_available=True),

    # =====================================================================
    # 🍨 DESSERTS
    # =====================================================================
    MenuItem(name="Gulab Jamun (2 pcs)", description="Warm deep-fried sweet dumplings.", category=MenuCategory.DESSERT, price=60, is_available=True),
    MenuItem(name="Gajar Ka Halwa", description="Carrot halwa slow cooked in ghee.", category=MenuCategory.DESSERT, price=90, is_available=True),
    MenuItem(name="Jalebi with Rabri", description="Crispy jalebi topped with rabri.", category=MenuCategory.DESSERT, price=80, is_available=True),
    MenuItem(name="Ras Malai", description="Soft chenna patties in sweet milk.", category=MenuCategory.DESSERT, price=90, is_available=True),
    MenuItem(name="Kulfi (Pista/Malai/Mango)", description="Traditional frozen dessert.", category=MenuCategory.DESSERT, price=80, is_available=True),
    MenuItem(name="Matka Kulfi", description="Kulfi served in a clay pot.", category=MenuCategory.DESSERT, price=100, is_available=True),
    MenuItem(name="Rabri Falooda", description="Falooda topped with rabri.", category=MenuCategory.DESSERT, price=140, is_available=True),
    MenuItem(name="Moong Dal Halwa", description="Rich halwa cooked in desi ghee.", category=MenuCategory.DESSERT, price=120, is_available=True),
    MenuItem(name="Brownie with Ice Cream", description="Hot brownie with vanilla scoop.", category=MenuCategory.DESSERT, price=160, is_available=True),

    # =====================================================================
    # 🥤 BEVERAGES
    # =====================================================================
    MenuItem(name="Masala Chai", description="Indian spiced tea.", category=MenuCategory.BEVERAGE, price=30, is_available=True),
    MenuItem(name="Filter Coffee", description="South Indian-style coffee.", category=MenuCategory.BEVERAGE, price=40, is_available=True),
    MenuItem(name="Sweet Lassi", description="Classic Punjabi lassi.", category=MenuCategory.BEVERAGE, price=80, is_available=True),
    MenuItem(name="Salted Lassi", description="Savory yogurt drink.", category=MenuCategory.BEVERAGE, price=80, is_available=True),
    MenuItem(name="Mango Lassi", description="Thick mango yogurt drink.", category=MenuCategory.BEVERAGE, price=110, is_available=True),
    MenuItem(name="Buttermilk (Chaas)", description="Refreshing chaas.", category=MenuCategory.BEVERAGE, price=60, is_available=True),
    MenuItem(name="Fresh Lime Soda", description="Sweet or salted lime soda.", category=MenuCategory.BEVERAGE, price=50, is_available=True),
    MenuItem(name="Cold Coffee", description="Creamy iced coffee.", category=MenuCategory.BEVERAGE, price=120, is_available=True),
    MenuItem(name="Orange Juice", description="Fresh orange juice.", category=MenuCategory.BEVERAGE, price=120, is_available=True),
    MenuItem(name="Pineapple Juice", description="Fresh pineapple juice.", category=MenuCategory.BEVERAGE, price=120, is_available=True),

]


    try:
        db.add_all(menu_items)
        db.commit()

        # Count by category
        appetizers = db.query(MenuItem).filter(MenuItem.category == MenuCategory.APPETIZER).count()
        mains = db.query(MenuItem).filter(MenuItem.category == MenuCategory.MAIN).count()
        desserts = db.query(MenuItem).filter(MenuItem.category == MenuCategory.DESSERT).count()
        beverages = db.query(MenuItem).filter(MenuItem.category == MenuCategory.BEVERAGE).count()
        total = db.query(MenuItem).count()

        print(f"\n✅ Successfully added {total} menu items!")
        print("\n🍽️  Menu Summary:")
        print(f"  📍 Starters/Appetizers: {appetizers} items")
        print(f"  🍛 Main Course: {mains} items")
        print(f"  🍨 Desserts: {desserts} items")
        print(f"  🥤 Beverages: {beverages} items")
        print(f"\n  Total: {total} items")

    except Exception as e:
        db.rollback()
        print(f"❌ Error while seeding menu: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🍛 SEED: Comprehensive Indian Restaurant Menu")
    print("="*60)
    seed_real_menu()
    print("\n" + "="*60)
    print("✅ Done.")
    print("="*60)
