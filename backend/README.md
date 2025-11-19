# 🍽️ AI Restaurant Chatbot - Complete Project Documentation

## 📚 Table of Contents
1. [Project Overview](#project-overview)
2. [Phase 1: Planning & Architecture](#phase-1-planning--architecture)
3. [Phase 2: Setup & Database](#phase-2-setup--database)
4. [Installation Guide](#installation-guide)
5. [Project Structure](#project-structure)
6. [Database Schema](#database-schema)
7. [API Endpoints](#api-endpoints)
8. [Code Files](#code-files)
9. [Testing Guide](#testing-guide)
10. [Deployment Guide](#deployment-guide)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

### 🎯 Objective
Build a complete AI-powered restaurant chatbot using:
- **Python** (main language)
- **FastAPI** (backend framework)
- **Gemini API** (AI/NLP)
- **MySQL** (database)
- **Render/AWS** (deployment)

### ✨ Features
- Menu queries
- Order placement & tracking
- Reservation handling
- FAQs automation
- Chat history logging
- WhatsApp integration (optional)

---

## Phase 1: Planning & Architecture

### System Architecture

```
┌─────────────────┐
│   User Interface│
│  (Web/WhatsApp) │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│        FastAPI Backend              │
│  ┌──────────────────────────────┐  │
│  │  API Endpoints                │  │
│  │  - /chat                      │  │
│  │  - /menu                      │  │
│  │  - /order                     │  │
│  │  - /reservation               │  │
│  └──────────────────────────────┘  │
│                                     │
│  ┌──────────────────────────────┐  │
│  │  Business Logic Layer        │  │
│  │  - Intent Classification     │  │
│  │  - Context Management        │  │
│  │  - Order Processing          │  │
│  └──────────────────────────────┘  │
└───────┬─────────────────┬───────────┘
        │                 │
        ▼                 ▼
┌───────────────┐   ┌──────────────┐
│  Gemini API   │   │   MySQL DB   │
│  (AI Brain)   │   │              │
└───────────────┘   │  - users     │
                    │  - menu      │
                    │  - orders    │
                    │  - chat_logs │
                    │  - reserv.   │
                    └──────────────┘
```

### Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API server |
| **AI Engine** | Google Gemini API | Natural language processing |
| **Database** | MySQL + SQLAlchemy | Data persistence |
| **Auth** | JWT (optional) | User authentication |
| **Frontend** | HTML/JS (simple) | Web chat interface |
| **Messaging** | Twilio (optional) | WhatsApp integration |
| **Deployment** | Render/AWS | Cloud hosting |

---

## Phase 2: Setup & Database

### Prerequisites
- Python 3.10 or higher
- MySQL 8.0 or higher
- VS Code (recommended)
- Git (optional)

---

## Installation Guide

### Step 1: Setup Environment

```bash
# Create project directory
mkdir restaurant-chatbot
cd restaurant-chatbot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

Create `requirements.txt`:

```txt
# Web Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0

# Database
sqlalchemy==2.0.25
pymysql==1.1.0

# Environment Variables
python-dotenv==1.0.0

# Data Validation
pydantic==2.5.3
pydantic-settings==2.1.0

# AI Integration
google-generativeai==0.3.2

# Utilities
python-multipart==0.0.6

# Testing
pytest==7.4.4
httpx==0.26.0
```

Install:
```bash
pip install -r requirements.txt
```

### Step 3: Create MySQL Database

```sql
-- Login to MySQL
mysql -u root -p

-- Create database
CREATE DATABASE restaurant_db;

-- Verify
SHOW DATABASES;

-- Use database
USE restaurant_db;

-- Exit
EXIT;
```

### Step 4: Configure Environment Variables

Create `.env` file:

```bash
# Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=restaurant_db
DB_USER=root
DB_PASSWORD=your_mysql_password_here

# Gemini API Key
# Get from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
APP_NAME=Restaurant Chatbot
DEBUG=True
API_VERSION=v1

# Restaurant Info
RESTAURANT_NAME=Tasty Bites Café
RESTAURANT_HOURS=11:00 AM - 11:00 PM
DELIVERY_AVAILABLE=true
```

---

## Project Structure

```
restaurant-chatbot/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration & env variables
│   ├── database.py             # Database connection
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py            # User model
│   │   ├── menu.py            # Menu items model
│   │   ├── order.py           # Orders model
│   │   ├── reservation.py     # Reservations model
│   │   └── chat_log.py        # Chat history model
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py            # Pydantic schemas for User
│   │   ├── menu.py            # Pydantic schemas for Menu
│   │   ├── order.py           # Pydantic schemas for Order
│   │   ├── reservation.py     # Pydantic schemas for Reservation
│   │   └── chat.py            # Pydantic schemas for Chat
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py            # Chat endpoints
│   │   ├── menu.py            # Menu endpoints
│   │   ├── order.py           # Order endpoints
│   │   └── reservation.py     # Reservation endpoints
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── gemini_service.py  # Gemini API integration
│   │   ├── chat_service.py    # Chat logic & context
│   │   ├── order_service.py   # Order processing
│   │   └── menu_service.py    # Menu operations
│   │
│   └── utils/
│       ├── __init__.py
│       ├── intent_classifier.py  # Intent detection
│       └── helpers.py            # Utility functions
│
├── tests/
│   ├── __init__.py
│   ├── test_chat.py
│   ├── test_order.py
│   └── test_menu.py
│
├── frontend/
│   ├── index.html             # Simple chat UI
│   ├── style.css
│   └── script.js
│
├── .env                        # Environment variables
├── .env.example               # Example env file
├── requirements.txt           # Python dependencies
├── create_tables.py           # Database initialization
├── seed_menu.py              # Sample menu data
├── README.md                  # Project documentation
└── render.yaml                # Render deployment config
```

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Menu Items Table
```sql
CREATE TABLE menu_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('appetizer', 'main', 'dessert', 'beverage') NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    image_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table
```sql
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Order Items Table
```sql
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price_at_order DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
);
```

### Reservations Table
```sql
CREATE TABLE reservations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    reservation_date DATE NOT NULL,
    reservation_time TIME NOT NULL,
    party_size INT NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    special_requests TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Chat Logs Table
```sql
CREATE TABLE chat_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    session_id VARCHAR(100) NOT NULL,
    user_message TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    intent VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

---

## API Endpoints

### Chat Endpoints
```
POST /api/v1/chat
- Send message and get AI response
Request: { "user_id": 1, "message": "Show me pizzas", "session_id": "abc123" }
Response: { "response": "Here are our pizzas...", "intent": "menu_query" }
```

### Menu Endpoints
```
GET /api/v1/menu
- Get all menu items (with filters)

GET /api/v1/menu/{item_id}
- Get specific menu item

GET /api/v1/menu/category/{category}
- Get items by category
```

### Order Endpoints
```
POST /api/v1/order
- Create new order

GET /api/v1/order/{order_id}
- Get order status

PUT /api/v1/order/{order_id}
- Update order

GET /api/v1/orders/user/{user_id}
- Get user's order history
```

### Reservation Endpoints
```
POST /api/v1/reservation
- Create reservation

GET /api/v1/reservation/{reservation_id}
- Get reservation details

PUT /api/v1/reservation/{reservation_id}
- Update reservation

DELETE /api/v1/reservation/{reservation_id}
- Cancel reservation
```

---

## Code Files

### 1. app/config.py

```python
"""
Configuration file - Loads environment variables
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database settings
    DB_HOST: str = "localhost"
    DB_PORT: int = 3306
    DB_NAME: str = "restaurant_db"
    DB_USER: str = "root"
    DB_PASSWORD: str

    # Gemini API
    GEMINI_API_KEY: str

    # App settings
    APP_NAME: str = "Restaurant Chatbot"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    # Restaurant info
    RESTAURANT_NAME: str = "Tasty Bites Café"
    RESTAURANT_HOURS: str = "11:00 AM - 11:00 PM"
    DELIVERY_AVAILABLE: bool = True

    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### 2. app/database.py

```python
"""
Database connection and session management
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    from app.models import user, menu, order, reservation, chat_log
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully!")

def drop_all_tables():
    print("⚠️  Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ All tables dropped!")
```

### 3. app/models/__init__.py

```python
"""
Models package - exports all database models
"""

from app.models.user import User
from app.models.menu import MenuItem
from app.models.order import Order, OrderItem
from app.models.reservation import Reservation
from app.models.chat_log import ChatLog

__all__ = [
    "User",
    "MenuItem",
    "Order",
    "OrderItem",
    "Reservation",
    "ChatLog"
]
```

### 4. app/models/user.py

```python
"""
User Model - Represents customers
"""

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    phone_number = Column(String(15), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    orders = relationship("Order", back_populates="user", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="user", cascade="all, delete-orphan")
    chat_logs = relationship("ChatLog", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', phone='{self.phone_number}')>"
```

### 5. app/models/menu.py

```python
"""
Menu Model - Represents menu items
"""

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class MenuCategory(str, enum.Enum):
    APPETIZER = "appetizer"
    MAIN = "main"
    DESSERT = "dessert"
    BEVERAGE = "beverage"

class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(Enum(MenuCategory), nullable=False, index=True)
    price = Column(Numeric(10, 2), nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    image_url = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order_items = relationship("OrderItem", back_populates="menu_item")

    def __repr__(self):
        return f"<MenuItem(id={self.id}, name='{self.name}', price=${self.price})>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "price": float(self.price),
            "is_available": self.is_available,
            "image_url": self.image_url
        }
```

### 6. app/models/order.py

```python
"""
Order Models - Orders and order items
"""

from sqlalchemy import Column, Integer, String, Text, Enum, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False, index=True)
    delivery_address = Column(Text, nullable=True)
    special_instructions = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Order(id={self.id}, user_id={self.user_id}, total=${self.total_amount})>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_order = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem(order_id={self.order_id}, menu_item_id={self.menu_item_id}, qty={self.quantity})>"
```

### 7. app/models/reservation.py

```python
"""
Reservation Model
"""

from sqlalchemy import Column, Integer, Date, Time, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ReservationStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    reservation_date = Column(Date, nullable=False, index=True)
    reservation_time = Column(Time, nullable=False)
    party_size = Column(Integer, nullable=False)
    status = Column(Enum(ReservationStatus), default=ReservationStatus.PENDING, nullable=False, index=True)
    special_requests = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation(id={self.id}, date={self.reservation_date}, party={self.party_size})>"
```

### 8. app/models/chat_log.py

```python
"""
ChatLog Model - Stores conversations
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    session_id = Column(String(100), nullable=False, index=True)
    user_message = Column(Text, nullable=False)
    bot_response = Column(Text, nullable=False)
    intent = Column(String(50), nullable=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("User", back_populates="chat_logs")

    def __repr__(self):
        return f"<ChatLog(id={self.id}, user_id={self.user_id}, intent='{self.intent}')>"

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "user_message": self.user_message,
            "bot_response": self.bot_response,
            "intent": self.intent,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
```

### 9. create_tables.py

```python
"""
Database initialization script
"""

from app.database import init_db, engine
from app.models import User, MenuItem, Order, OrderItem, Reservation, ChatLog

def main():
    print("=" * 50)
    print("DATABASE INITIALIZATION")
    print("=" * 50)

    try:
        print("\n1. Testing database connection...")
        connection = engine.connect()
        print("✅ Connection successful!")
        connection.close()

        print("\n2. Creating tables...")
        init_db()

        print("\n" + "=" * 50)
        print("✅ DATABASE SETUP COMPLETE!")
        print("=" * 50)
        print("\nTables created:")
        print("  - users")
        print("  - menu_items")
        print("  - orders")
        print("  - order_items")
        print("  - reservations")
        print("  - chat_logs")

    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
```

### 10. seed_menu.py

```python
"""
Seed script - Add sample menu items
"""

from app.database import SessionLocal
from app.models.menu import MenuItem, MenuCategory

def seed_menu():
    db = SessionLocal()

    menu_items = [
        # Appetizers
        MenuItem(name="Garlic Bread", description="Crispy bread with garlic butter",
                 category=MenuCategory.APPETIZER, price=5.99, is_available=True),
        MenuItem(name="Chicken Wings", description="Spicy buffalo wings",
                 category=MenuCategory.APPETIZER, price=8.99, is_available=True),
        MenuItem(name="Mozzarella Sticks", description="Fried mozzarella with marinara",
                 category=MenuCategory.APPETIZER, price=6.99, is_available=True),

        # Main Course
        MenuItem(name="Margherita Pizza", description="Classic pizza with tomato and mozzarella",
                 category=MenuCategory.MAIN, price=12.99, is_available=True),
        MenuItem(name="Pepperoni Pizza", description="Pizza loaded with pepperoni",
                 category=MenuCategory.MAIN, price=14.99, is_available=True),
        MenuItem(name="Chicken Burger", description="Grilled chicken burger with fries",
                 category=MenuCategory.MAIN, price=11.99, is_available=True),
        MenuItem(name="Pasta Alfredo", description="Creamy alfredo pasta",
                 category=MenuCategory.MAIN, price=13.99, is_available=True),
        MenuItem(name="Caesar Salad", description="Fresh romaine with Caesar dressing",
                 category=MenuCategory.MAIN, price=9.99, is_available=True),

        # Desserts
        MenuItem(name="Chocolate Brownie", description="Warm brownie with ice cream",
                 category=MenuCategory.DESSERT, price=6.99, is_available=True),
        MenuItem(name="Cheesecake", description="Classic New York cheesecake",
                 category=MenuCategory.DESSERT, price=7.99, is_available=True),
        MenuItem(name="Tiramisu", description="Italian coffee dessert",
                 category=MenuCategory.DESSERT, price=8.99, is_available=True),

        # Beverages
        MenuItem(name="Coca Cola", description="Chilled soft drink",
                 category=MenuCategory.BEVERAGE, price=2.99, is_available=True),
        MenuItem(name="Fresh Orange Juice", description="Freshly squeezed",
                 category=MenuCategory.BEVERAGE, price=4.99, is_available=True),
        MenuItem(name="Iced Coffee", description="Cold brew coffee",
                 category=MenuCategory.BEVERAGE, price=4.99, is_available=True),
    ]

    try:
        db.add_all(menu_items)
        db.commit()
        print(f"✅ Successfully added {len(menu_items)} menu items!")
    except Exception as e:
        db.rollback()
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_menu()
```

---

## Testing Guide

### Quick Setup Test

```bash
# 1. Test Python version
python --version

# 2. Test virtual environment
which python  # Should show venv path

# 3. Test database connection
python app/database.py

# 4. Create tables
python create_tables.py

# 5. Add menu data
python seed_menu.py

# 6. Verify in MySQL
mysql -u root -p
USE restaurant_db;
SHOW TABLES;
SELECT * FROM menu_items;
```

---

## Deployment Guide

### Render Deployment

1. Push code to GitHub
2. Create account on render.com
3. Create new Web Service
4. Connect GitHub repository
5. Set environment variables
6. Deploy

### AWS Deployment

1. Create EC2 instance
2. Install Python, MySQL
3. Clone repository
4. Setup environment
5. Run with systemd

---

## Troubleshooting

### Common Issues

**Issue: Database connection failed**
```bash
# Solution:
1. Check MySQL is running: sudo service mysql status
2. Verify credentials in .env
3. Create database: CREATE DATABASE restaurant_db;
```

**Issue: Module not found**
```bash
# Solution:
1. Activate venv: source venv/bin/activate
2. Install deps: pip install -r requirements.txt
```

**Issue: Import errors**
```bash
# Solution:
1. Add __init__.py files in all directories
2. Set PYTHONPATH: export PYTHONPATH="${PYTHONPATH}:/path/to/project"
```

---

## Next Steps

### Phase 3: Pydantic Schemas & FastAPI
- Create Pydantic schemas
- Setup FastAPI app
- Create menu endpoints
- Test with Postman

### Phase 4: Gemini Integration
- Connect Gemini API
- Implement chat logic
- Add intent detection
- Context management

### Phase 5: Order & Reservation
- Order placement endpoints
- Reservation system
- Status tracking
- Notifications

### Phase 6: Testing & Deployment
- Unit tests
- Integration tests
- Deploy to Render/AWS
- Monitor and debug

---

## Contact & Support

For issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Test each component individually
4. Use MySQL/Python debuggers

---

## License

This project is for educational purposes.

---

**Last Updated:** November 2025
**Version:** 1.0.0
**Status:** Phase 2 Complete ✅
