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
        # Appetizers
        MenuItem(
            name="Garlic Bread",
            description="Crispy bread with garlic butter",
            category=MenuCategory.APPETIZER,
            price=5.99,
            is_available=True
        ),
        MenuItem(
            name="Chicken Wings",
            description="Spicy buffalo wings with ranch dip",
            category=MenuCategory.APPETIZER,
            price=8.99,
            is_available=True
        ),
        MenuItem(
            name="Mozzarella Sticks",
            description="Fried mozzarella with marinara sauce",
            category=MenuCategory.APPETIZER,
            price=6.99,
            is_available=True
        ),

        # Main Course
        MenuItem(
            name="Margherita Pizza",
            description="Classic pizza with tomato, mozzarella, and basil",
            category=MenuCategory.MAIN,
            price=12.99,
            is_available=True
        ),
        MenuItem(
            name="Pepperoni Pizza",
            description="Pizza loaded with pepperoni slices",
            category=MenuCategory.MAIN,
            price=14.99,
            is_available=True
        ),
        MenuItem(
            name="Chicken Burger",
            description="Grilled chicken burger with fries",
            category=MenuCategory.MAIN,
            price=11.99,
            is_available=True
        ),
        MenuItem(
            name="Pasta Alfredo",
            description="Creamy alfredo pasta with chicken",
            category=MenuCategory.MAIN,
            price=13.99,
            is_available=True
        ),
        MenuItem(
            name="Caesar Salad",
            description="Fresh romaine lettuce with Caesar dressing",
            category=MenuCategory.MAIN,
            price=9.99,
            is_available=True
        ),

        # Desserts
        MenuItem(
            name="Chocolate Brownie",
            description="Warm brownie with vanilla ice cream",
            category=MenuCategory.DESSERT,
            price=6.99,
            is_available=True
        ),
        MenuItem(
            name="Cheesecake",
            description="Classic New York style cheesecake",
            category=MenuCategory.DESSERT,
            price=7.99,
            is_available=True
        ),
        MenuItem(
            name="Tiramisu",
            description="Italian coffee-flavored dessert",
            category=MenuCategory.DESSERT,
            price=8.99,
            is_available=True
        ),

        # Beverages
        MenuItem(
            name="Coca Cola",
            description="Chilled soft drink",
            category=MenuCategory.BEVERAGE,
            price=2.99,
            is_available=True
        ),
        MenuItem(
            name="Fresh Orange Juice",
            description="Freshly squeezed orange juice",
            category=MenuCategory.BEVERAGE,
            price=4.99,
            is_available=True
        ),
        MenuItem(
            name="Iced Coffee",
            description="Cold brew coffee with ice",
            category=MenuCategory.BEVERAGE,
            price=4.99,
            is_available=True
        ),
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
