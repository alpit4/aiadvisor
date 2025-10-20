"""
Simple test script to verify the system works
"""
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.config import settings
        print("✅ Config imported successfully")
        print(f"   Salon: {settings.SALON_NAME}")
    except Exception as e:
        print(f"❌ Config import failed: {e}")
        return False
    
    try:
        from src.database import init_db, HelpRequest, KnowledgeEntry
        print("✅ Database models imported successfully")
    except Exception as e:
        print(f"❌ Database import failed: {e}")
        return False
    
    try:
        from src.knowledge_base import KnowledgeBase
        print("✅ Knowledge base imported successfully")
    except Exception as e:
        print(f"❌ Knowledge base import failed: {e}")
        return False
    
    try:
        from src.supervisor_notifier import SupervisorNotifier
        print("✅ Supervisor notifier imported successfully")
    except Exception as e:
        print(f"❌ Supervisor notifier import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database initialization"""
    print("\n Testing database...")
    
    try:
        from src.database import init_db
        import asyncio
        
        async def run_init():
            await init_db()
            print("✅ Database initialized successfully")
        
        asyncio.run(run_init())
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality"""
    print("\n Testing knowledge base...")
    
    try:
        from src.knowledge_base import KnowledgeBase
        import asyncio
        
        async def run_test():
            kb = KnowledgeBase()
            await kb.initialize()
            print("✅ Knowledge base initialized successfully")
            
            # Test a known question
            answer = await kb.get_answer("What are your hours?")
            if answer:
                print(f"✅ Found answer: {answer}")
            else:
                print("❌ No answer found for known question")
                return False
            
            return True
        
        return asyncio.run(run_test())
    except Exception as e:
        print(f"❌ Knowledge base test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Frontdesk AI Supervisor System - Simple Test")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Check your Python environment.")
        return False
    
    # Test database
    if not test_database():
        print("\n❌ Database tests failed. Check SQLite installation.")
        return False
    
    # Test knowledge base
    if not test_knowledge_base():
        print("\n❌ Knowledge base tests failed.")
        return False
    
    print("\n All tests passed!")
    print("\n Next steps:")
    print("1. Run: python main.py")
    print("2. Open: http://localhost:8000/supervisor")
    print("3. Test the supervisor dashboard")
    
    return True

if __name__ == "__main__":
    main()


