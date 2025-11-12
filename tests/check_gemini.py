# Check if all imports are working

print("Checking imports...")

try:
    print("\n1. Checking config...")
    from app.config import settings
    print(f"   ✅ Config loaded: {settings.APP_NAME}")
except Exception as e:
    print(f"   ❌ Config error: {e}")

try:
    print("\n2. Checking database...")
    from app.database import engine
    print("   ✅ Database imported")
except Exception as e:
    print(f"   ❌ Database error: {e}")

try:
    print("\n3. Checking models...")
    from app.models import User, MenuItem, ChatLog
    print("   ✅ Models imported")
except Exception as e:
    print(f"   ❌ Models error: {e}")

try:
    print("\n4. Checking schemas...")
    from app.schemas.chat import ChatRequest, ChatResponse
    from app.schemas.menu import MenuItemResponse
    print("   ✅ Schemas imported")
except Exception as e:
    print(f"   ❌ Schemas error: {e}")

try:
    print("\n5. Checking Gemini service...")
    from app.services.gemini_service import gemini_service
    print("   ✅ Gemini service imported")
except Exception as e:
    print(f"   ❌ Gemini service error: {e}")

try:
    print("\n6. Checking chat service...")
    from app.services.chat_service import chat_service
    print("   ✅ Chat service imported")
except Exception as e:
    print(f"   ❌ Chat service error: {e}")

try:
    print("\n7. Checking menu router...")
    from app.routers import menu
    print("   ✅ Menu router imported")
except Exception as e:
    print(f"   ❌ Menu router error: {e}")

try:
    print("\n8. Checking chat router...")
    from app.routers import chat
    print("   ✅ Chat router imported")
except Exception as e:
    print(f"   ❌ Chat router error: {e}")

try:
    print("\n9. Checking main app...")
    from app.main import app
    print("   ✅ Main app imported")
    print(f"   Routes registered: {len(app.routes)}")
except Exception as e:
    print(f"   ❌ Main app error: {e}")

print("\n" + "="*50)
print("Import check complete!")
print("="*50)
