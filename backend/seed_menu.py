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

        # ========== SOUPS -> mapped to APPETIZER ==========
        MenuItem(name="Tamatar Shorba", description="Mildly spiced tomato soup.", category=MenuCategory.APPETIZER, price=80, is_available=True, image_url=None),
        MenuItem(name="Dal Soup", description="Lightly seasoned lentil broth.", category=MenuCategory.APPETIZER, price=90, is_available=True, image_url=None),
        MenuItem(name="Manchow Soup (Veg/Chicken)", description="Thick soup with crispy noodles - veg or chicken.", category=MenuCategory.APPETIZER, price=120, is_available=True, image_url=None),
        MenuItem(name="Hot & Sour Soup (Veg/Chicken)", description="Spicy and tangy broth - veg or chicken.", category=MenuCategory.APPETIZER, price=120, is_available=True, image_url=None),
        MenuItem(name="Sweet Corn Soup (Veg/Chicken)", description="Light, creamy soup with sweet corn - veg or chicken.", category=MenuCategory.APPETIZER, price=120, is_available=True, image_url=None),

        # ========== APPETIZERS_INDIAN -> APPETIZER ==========
        MenuItem(name="Paneer Tikka (Malai/Achari)", description="Creamy or pickled-spice marinated cottage cheese.", category=MenuCategory.APPETIZER, price=240, is_available=True, image_url=None),
        MenuItem(name="Tandoori Aloo", description="Spiced potatoes grilled in the tandoor.", category=MenuCategory.APPETIZER, price=140, is_available=True, image_url=None),
        MenuItem(name="Vegetable Samosa (2 pcs)", description="Flaky pastry with spiced potato and peas.", category=MenuCategory.APPETIZER, price=50, is_available=True, image_url=None),
        MenuItem(name="Onion Bhaji / Vegetable Pakora", description="Assorted vegetable fritters.", category=MenuCategory.APPETIZER, price=80, is_available=True, image_url=None),
        MenuItem(name="Aloo Tikki Chaat", description="Spiced potato patty with chutneys and yogurt.", category=MenuCategory.APPETIZER, price=110, is_available=True, image_url=None),
        MenuItem(name="Hara Bhara Kebab", description="Spinach and vegetable patties.", category=MenuCategory.APPETIZER, price=150, is_available=True, image_url=None),
        MenuItem(name="Dahi Ke Kebab", description="Crispy hung curd patties.", category=MenuCategory.APPETIZER, price=170, is_available=True, image_url=None),
        MenuItem(name="Tandoori Chicken (Half)", description="Classic yogurt-marinated chicken pieces.", category=MenuCategory.APPETIZER, price=280, is_available=True, image_url=None),
        MenuItem(name="Chicken Tikka (Classic/Pahadi)", description="Boneless chicken with standard or green herb marinade.", category=MenuCategory.APPETIZER, price=260, is_available=True, image_url=None),
        MenuItem(name="Mutton Seekh Kebab", description="Spiced minced lamb/grilled on skewers.", category=MenuCategory.APPETIZER, price=320, is_available=True, image_url=None),
        MenuItem(name="Amritsari Fish Fry", description="Crispy, tangy fish fritters.", category=MenuCategory.APPETIZER, price=280, is_available=True, image_url=None),
        MenuItem(name="Chicken 65", description="Spicy South Indian style dry chicken.", category=MenuCategory.APPETIZER, price=230, is_available=True, image_url=None),

        # ========== INDO-CHINESE / FUSION -> MAIN (or APPETIZER for starters) ==========
        MenuItem(name="Chilli Paneer (Dry)", description="Paneer tossed with bell peppers and chilli sauce.", category=MenuCategory.MAIN, price=220, is_available=True, image_url=None),
        MenuItem(name="Gobi Manchurian (Dry)", description="Crispy cauliflower florets in Manchurian sauce.", category=MenuCategory.MAIN, price=200, is_available=True, image_url=None),
        MenuItem(name="Crispy Chilli Potato", description="Shredded potatoes in sweet-spicy sauce.", category=MenuCategory.MAIN, price=180, is_available=True, image_url=None),
        MenuItem(name="Chicken Lollipop", description="Battered and fried chicken drumettes.", category=MenuCategory.MAIN, price=260, is_available=True, image_url=None),
        MenuItem(name="Vegetable Manchurian (Gravy)", description="Veg dumplings in a spiced brown sauce.", category=MenuCategory.MAIN, price=200, is_available=True, image_url=None),
        MenuItem(name="Chilli Chicken (Gravy)", description="Chicken in a thick, spicy sauce.", category=MenuCategory.MAIN, price=260, is_available=True, image_url=None),
        MenuItem(name="Veg/Chicken in Hot Garlic Sauce", description="Choice of veg or chicken in pungent garlic sauce.", category=MenuCategory.MAIN, price=250, is_available=True, image_url=None),
        MenuItem(name="Vegetable Hakka Noodles", description="Stir-fried noodles with crisp veggies.", category=MenuCategory.MAIN, price=160, is_available=True, image_url=None),
        MenuItem(name="Chicken Schezwan Noodles", description="Fiery noodles tossed in Schezwan sauce.", category=MenuCategory.MAIN, price=200, is_available=True, image_url=None),
        MenuItem(name="Vegetable Fried Rice", description="Classic stir-fried rice.", category=MenuCategory.MAIN, price=150, is_available=True, image_url=None),
        MenuItem(name="Egg/Chicken Schezwan Fried Rice", description="Fried rice with egg or chicken and Schezwan sauce.", category=MenuCategory.MAIN, price=180, is_available=True, image_url=None),

        # ========== MAIN COURSE - VEG -> MAIN ==========
        MenuItem(name="Paneer Butter Masala", description="Cottage cheese in a rich, creamy tomato sauce.", category=MenuCategory.MAIN, price=240, is_available=True, image_url=None),
        MenuItem(name="Shahi Paneer", description="Paneer in a mild, cashew-cream gravy.", category=MenuCategory.MAIN, price=260, is_available=True, image_url=None),
        MenuItem(name="Palak Paneer", description="Paneer in creamy spinach gravy.", category=MenuCategory.MAIN, price=220, is_available=True, image_url=None),
        MenuItem(name="Malai Kofta", description="Vegetable/paneer dumplings in a cream sauce.", category=MenuCategory.MAIN, price=240, is_available=True, image_url=None),
        MenuItem(name="Bhendi Masala", description="Okra sautéed with spices.", category=MenuCategory.MAIN, price=160, is_available=True, image_url=None),
        MenuItem(name="Navratan Korma", description="Mixed vegetables in a mild, creamy sauce.", category=MenuCategory.MAIN, price=220, is_available=True, image_url=None),
        MenuItem(name="Aloo Gobi Adraki", description="Potato and cauliflower with ginger.", category=MenuCategory.MAIN, price=150, is_available=True, image_url=None),
        MenuItem(name="Veg Kolhapuri", description="Fiery, spicy, thick gravy (Western India).", category=MenuCategory.MAIN, price=200, is_available=True, image_url=None),

        # ========== MAIN COURSE - NON-VEG -> MAIN ==========
        MenuItem(name="Butter Chicken (Murgh Makhani)", description="Tandoori chicken in a sweet and tangy cream sauce.", category=MenuCategory.MAIN, price=300, is_available=True, image_url=None),
        MenuItem(name="Chicken Tikka Masala", description="Grilled chicken in spiced tomato and onion gravy.", category=MenuCategory.MAIN, price=280, is_available=True, image_url=None),
        MenuItem(name="Kadai Chicken", description="Chicken cooked with capsicum, onion, and coarse spices.", category=MenuCategory.MAIN, price=260, is_available=True, image_url=None),
        MenuItem(name="Rogan Josh (Lamb/Goat)", description="Fragrant Kashmiri aromatic curry.", category=MenuCategory.MAIN, price=380, is_available=True, image_url=None),
        MenuItem(name="Laal Maas", description="Fiery Rajasthani mutton curry.", category=MenuCategory.MAIN, price=380, is_available=True, image_url=None),
        MenuItem(name="Prawn Korma / Curry", description="Prawns in a rich, mild or spiced sauce.", category=MenuCategory.MAIN, price=340, is_available=True, image_url=None),
        MenuItem(name="Vindaloo (Chicken/Lamb)", description="Goan, spicy, and tangy curry with vinegar.", category=MenuCategory.MAIN, price=320, is_available=True, image_url=None),
        MenuItem(name="Malabar Fish Curry", description="Fish cooked in coconut milk (South Indian style).", category=MenuCategory.MAIN, price=300, is_available=True, image_url=None),

        # ========== DALS AND LEGUMES -> MAIN ==========
        MenuItem(name="Dal Makhani", description="Slow-cooked black lentils with cream and butter.", category=MenuCategory.MAIN, price=180, is_available=True, image_url=None),
        MenuItem(name="Yellow Dal Tadka", description="Tempered pigeon pea lentils.", category=MenuCategory.MAIN, price=140, is_available=True, image_url=None),
        MenuItem(name="Rajma Masala", description="Red kidney beans curry.", category=MenuCategory.MAIN, price=160, is_available=True, image_url=None),
        MenuItem(name="Chole Bhature", description="Chickpea curry served with large, fried bread.", category=MenuCategory.MAIN, price=160, is_available=True, image_url=None),

        # ========== RICE AND BIRYANI -> MAIN ==========
        MenuItem(name="Basmati Rice (Steamed)", description="Plain steamed rice.", category=MenuCategory.MAIN, price=80, is_available=True, image_url=None),
        MenuItem(name="Jeera Rice", description="Rice tempered with cumin seeds and ghee.", category=MenuCategory.MAIN, price=110, is_available=True, image_url=None),
        MenuItem(name="Matar Pulao", description="Rice with green peas.", category=MenuCategory.MAIN, price=140, is_available=True, image_url=None),
        MenuItem(name="Kashmiri Pulao", description="Sweet pulao with nuts and fruits.", category=MenuCategory.MAIN, price=200, is_available=True, image_url=None),
        MenuItem(name="Vegetable Dum Biryani", description="Layered, spiced rice with vegetables.", category=MenuCategory.MAIN, price=220, is_available=True, image_url=None),
        MenuItem(name="Chicken Dum Biryani", description="Layered, spiced rice with chicken.", category=MenuCategory.MAIN, price=260, is_available=True, image_url=None),
        MenuItem(name="Mutton Dum Biryani", description="Layered, spiced rice with mutton.", category=MenuCategory.MAIN, price=350, is_available=True, image_url=None),

        # ========== INDIAN BREADS -> MAIN (we map breads to MAIN) ==========
        MenuItem(name="Plain Naan", description="Leavened bread baked in Tandoor.", category=MenuCategory.MAIN, price=30, is_available=True, image_url=None),
        MenuItem(name="Butter Naan", description="Naan brushed with butter.", category=MenuCategory.MAIN, price=40, is_available=True, image_url=None),
        MenuItem(name="Garlic Naan", description="Naan with fresh garlic.", category=MenuCategory.MAIN, price=50, is_available=True, image_url=None),
        MenuItem(name="Tandoori Roti", description="Whole wheat bread baked in Tandoor.", category=MenuCategory.MAIN, price=25, is_available=True, image_url=None),
        MenuItem(name="Tawa Roti / Chapati", description="Plain whole wheat bread (pan-cooked).", category=MenuCategory.MAIN, price=20, is_available=True, image_url=None),
        MenuItem(name="Lachha Paratha", description="Flaky layered whole wheat bread.", category=MenuCategory.MAIN, price=60, is_available=True, image_url=None),
        MenuItem(name="Aloo Paratha", description="Whole wheat bread stuffed with spiced potato.", category=MenuCategory.MAIN, price=80, is_available=True, image_url=None),
        MenuItem(name="Keema Naan", description="Naan stuffed with spiced minced meat.", category=MenuCategory.MAIN, price=120, is_available=True, image_url=None),
        MenuItem(name="Peshwari Naan", description="Sweet naan with nut/raisin filling.", category=MenuCategory.MAIN, price=100, is_available=True, image_url=None),

        # ========== DESSERTS -> DESSERT ==========
        MenuItem(name="Gulab Jamun (Hot)", description="Deep-fried milk solids in sugar syrup (served warm).", category=MenuCategory.DESSERT, price=60, is_available=True, image_url=None),
        MenuItem(name="Gajar Ka Halwa (Hot)", description="Slow-cooked carrot pudding (served warm).", category=MenuCategory.DESSERT, price=90, is_available=True, image_url=None),
        MenuItem(name="Jalebi with Rabri", description="Crispy coils with thickened milk.", category=MenuCategory.DESSERT, price=80, is_available=True, image_url=None),
        MenuItem(name="Ras Malai", description="Chilled saffron-milk cheese patties.", category=MenuCategory.DESSERT, price=90, is_available=True, image_url=None),
        MenuItem(name="Kulfi (Pista/Malai/Mango)", description="Traditional frozen dairy dessert.", category=MenuCategory.DESSERT, price=80, is_available=True, image_url=None),
        MenuItem(name="Ice Cream (Vanilla/Chocolate)", description="Basic ice cream scoops.", category=MenuCategory.DESSERT, price=60, is_available=True, image_url=None),

        # ========== BEVERAGES -> BEVERAGE ==========
        MenuItem(name="Masala Chai", description="Hot spiced Indian tea.", category=MenuCategory.BEVERAGE, price=30, is_available=True, image_url=None),
        MenuItem(name="Indian Filter Coffee", description="South Indian style coffee.", category=MenuCategory.BEVERAGE, price=40, is_available=True, image_url=None),
        MenuItem(name="Mango Lassi", description="Sweet and thick yogurt drink.", category=MenuCategory.BEVERAGE, price=110, is_available=True, image_url=None),
        MenuItem(name="Sweet/Salted Lassi", description="Traditional yogurt drink.", category=MenuCategory.BEVERAGE, price=80, is_available=True, image_url=None),
        MenuItem(name="Buttermilk (Chaas)", description="Spiced, thin yogurt drink.", category=MenuCategory.BEVERAGE, price=60, is_available=True, image_url=None),
        MenuItem(name="Fresh Lime Soda (Sweet/Salt)", description="Simple lime cooler.", category=MenuCategory.BEVERAGE, price=50, is_available=True, image_url=None),
        MenuItem(name="Jal Jeera", description="Tangy, cumin-based cooler.", category=MenuCategory.BEVERAGE, price=60, is_available=True, image_url=None),

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
