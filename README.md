# 🍛 Nyra Chatbot - AI-Powered Restaurant Ordering System

An intelligent restaurant chatbot built with FastAPI, React, and Google Gemini AI that enables customers to browse menus, place orders, and make reservations through natural conversation.

![Chat Interface](./assets/Chat-Container.png)

## 🌟 Features

### 🤖 AI Chat Assistant
- Natural language understanding powered by Google Gemini
- Context-aware conversations
- Multi-intent detection (orders, reservations, menu queries)
- Fuzzy matching for menu items

### 🍽️ Menu Management
- 100+ Indian cuisine items across 4 categories
- Real-time menu browsing
- Category-wise filtering (Appetizers, Mains, Desserts, Beverages)
- Detailed item descriptions and pricing

### 🛒 Smart Cart System
- Add items via chat or manual selection
- Real-time cart synchronization
- Quantity management
- Order total calculation with delivery fees

### 📅 Reservations
- Table booking through chat
- Date, time, and party size selection
- Special requests support

### 🎨 Modern UI/UX
- Responsive design for mobile and desktop
- Dark/Light mode toggle
- Smooth animations with Framer Motion
- Beautiful Tailwind CSS styling

---

## 🚀 Live Demo

- **Frontend**: [https://nyra-chatbot.vercel.app](https://nyra-chatbot.vercel.app)
- **Backend API**: [https://nyra-chatbot-api.onrender.com](https://nyra-chatbot-api.onrender.com)
- **API Documentation**: [https://nyra-chatbot-api.onrender.com/docs](https://nyra-chatbot-api.onrender.com/docs)

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.115.0
- **Database**: PostgreSQL (Production) / MySQL (Development)
- **ORM**: SQLAlchemy 2.0.36
- **AI**: Google Gemini API (gemini-2.5-flash)
- **Authentication**: JWT (planned)

### Frontend
- **Framework**: React 19.2.0
- **Build Tool**: Vite 6.4.1
- **Styling**: Tailwind CSS 4.1.17
- **Animations**: Framer Motion 12.23.24
- **HTTP Client**: Axios 1.13.2
- **Icons**: Lucide React 0.554.0

### Deployment
- **Backend**: Render.com (Free Tier)
- **Frontend**: Vercel (Free Tier)
- **Database**: Render PostgreSQL (Free Tier)

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- MySQL (for local development) or PostgreSQL
- Google Gemini API Key

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/ashwin-bhanage/nyra-chatbot.git
cd nyra-chatbot/backend
```

2. **Create virtual environment**
```bash
python -m venv virtual
source virtual/bin/activate  # On Windows: virtual\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**
```bash
cp .env.example .env
```

Edit `.env`:
```env
# Database (MySQL for local dev)
DB_HOST=localhost
DB_PORT=3306
DB_NAME=nyra_db
DB_USER=root
DB_PASSWORD=your_password

# For production (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:port/database

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here

# Restaurant Info
RESTAURANT_NAME=Royal Spice Kitchen
RESTAURANT_HOURS=11:00 AM - 11:00 PM
DELIVERY_AVAILABLE=true

# CORS
FRONTEND_URL=http://localhost:3000
```

5. **Create database tables**
```bash
python create_tables.py
```

6. **Seed menu data**
```bash
python seed_menu.py
```

7. **Run the server**
```bash
uvicorn app.main:app --reload
```

Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment**
```bash
# Create .env.development
echo "VITE_API_URL=" > .env.development
```

4. **Run development server**
```bash
npm run dev
```

Frontend will be available at `http://localhost:3000`

---

## 📁 Project Structure

```
nyra-chatbot/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   ├── routers/         # API endpoints
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   │   ├── chat_service.py
│   │   │   ├── gemini_service.py
│   │   │   └── reservation_service.py
│   │   ├── config.py        # Configuration
│   │   ├── database.py      # Database connection
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   ├── Procfile            # Render deployment
│   └── runtime.txt         # Python version
│
└── frontend/
    ├── src/
    │   ├── components/      # React components
    │   │   ├── ChatContainer.jsx
    │   │   ├── CartDrawer.jsx
    │   │   ├── MenuItemCard.jsx
    │   │   └── MessageBubble.jsx
    │   ├── context/         # React Context
    │   │   └── CartContext.jsx
    │   ├── config.js        # API configuration
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    └── vercel.json         # Vercel deployment
```

---

## 🔑 API Endpoints

### Chat
- `POST /api/v1/chat` - Send message to chatbot

### Menu
- `GET /api/v1/menu` - Get all menu items
- `GET /api/v1/menu/{id}` - Get specific item
- `GET /api/v1/menu/category/{category}` - Get items by category

### Orders
- `POST /api/v1/order` - Place an order
- `GET /api/v1/orders` - Get user orders
- `GET /api/v1/orders/{id}` - Get specific order

### Reservations
- `POST /api/v1/reservations` - Create reservation
- `GET /api/v1/reservations` - Get user reservations

---

## 🤖 Chat Commands

The chatbot understands natural language. Try these examples:

### Ordering
```
"Add 2 Chicken Biryani"
"I want Paneer Tikka"
"Order veg biryani"
"Give me 1 butter naan and 2 lassi"
```

### Menu Browsing
```
"Show me desserts"
"What biryanis do you have?"
"Show menu"
"List all beverages"
```

### Cart & Checkout
```
"What's in my cart?"
"Checkout"
"Show total"
"Place order"
```

### Reservations
```
"Book a table for 4 on December 25 at 7 PM"
"Reserve table for two tomorrow at 8"
```

---

## 🎨 Screenshots

### Chat Interface
![Chat Interface](./assets/Chat-Container.png)

### Menu View
![Menu](./assets/Menu-Card2.png)

### Cart Drawer
![Cart](./assets/Cart-Drawer.png)

---

## 🚀 Deployment

### Backend (Render)

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy backend"
git push origin main
```

2. **Create Web Service on Render**
- Connect GitHub repository
- Root Directory: `backend`
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT`

3. **Add Environment Variables**
```
DATABASE_URL=<postgres_url>
GEMINI_API_KEY=<your_key>
RESTAURANT_NAME=Royal Spice Kitchen
FRONTEND_URL=https://your-app.vercel.app
ENVIRONMENT=production
```

4. **Create PostgreSQL Database**
- Add PostgreSQL add-on
- Copy connection string to DATABASE_URL

### Frontend (Vercel)

1. **Push to GitHub**
```bash
git add .
git commit -m "Deploy frontend"
git push origin main
```

2. **Import Project to Vercel**
- Connect GitHub repository
- Framework: Vite
- Root Directory: `frontend`
- Build Command: `npm run build`
- Output Directory: `dist`

3. **Add Environment Variable**
```
VITE_API_URL=https://your-backend.onrender.com
```

---

## 🐛 Troubleshooting

### Backend Issues

**Database Connection Error**
```bash
# Check PostgreSQL URL format
DATABASE_URL=postgresql://user:password@host:port/database
```

**Import Errors**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### Frontend Issues

**API Connection Failed**
- Verify `VITE_API_URL` in `.env.production`
- Check CORS settings in backend

**Build Errors**
```bash
# Clear cache and rebuild
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Ashwin Bhanage**
- GitHub: [@ashwin-bhanage](https://github.com/ashwin-bhanage)
- Project Link: [https://github.com/ashwin-bhanage/nyra-chatbot](https://github.com/ashwin-bhanage/nyra-chatbot)

---

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [Google Gemini](https://ai.google.dev/) - AI language model
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS
- [Framer Motion](https://www.framer.com/motion/) - Animation library
- [Render](https://render.com/) - Backend hosting
- [Vercel](https://vercel.com/) - Frontend hosting

---

## 📊 Project Stats

- **Lines of Code**: ~5,000+
- **API Endpoints**: 15+
- **Menu Items**: 101
- **Categories**: 4 (Appetizers, Mains, Desserts, Beverages)
- **Development Time**: 2 weeks
- **Technologies Used**: 10+

---

## 🔮 Future Enhancements

- [ ] User authentication & profiles
- [ ] Order history & tracking
- [ ] Payment gateway integration (Stripe/Razorpay)
- [ ] Admin dashboard for menu management
- [ ] Email/SMS notifications
- [ ] WhatsApp bot integration
- [ ] Multi-language support
- [ ] Analytics dashboard
- [ ] Loyalty rewards program
- [ ] Voice ordering capability

---

## 📞 Support

For support, email bhanageashwin28@gmail.com or open an issue on GitHub.

---

<div align="center">
  <p>Made with ❤️ and lots of ☕</p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>
