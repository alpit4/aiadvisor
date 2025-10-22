"""
Interactive Voice Demo
Allows you to type questions and see AI responses in real-time
"""

import asyncio
import logging
from src.config import settings
from src.knowledge_base import KnowledgeBase
from src.supervisor_notifier import SupervisorNotifier
from src.database import get_db_session, HelpRequest

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InteractiveVoiceDemo:
    """Interactive voice demo for real-time testing"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.supervisor_notifier = SupervisorNotifier()
        self.request_count = 0
        
    async def start_interactive_demo(self):
        """Start interactive voice demo"""
        print("🎤 Interactive Voice AI Demo")
        print("=" * 50)
        print(f"📞 Salon: {settings.SALON_NAME}")
        print(f"🕒 Hours: {settings.SALON_HOURS}")
        print(f"📱 Phone: {settings.SALON_PHONE}")
        print()
        print("💡 Type your questions as if you're calling the salon")
        print("💡 Type 'quit' to exit")
        print("=" * 50)
        
        while True:
            try:
                # Get user input
                question = input("\n🗣️  Your question: ").strip()
                
                if question.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Demo ended. Thank you!")
                    break
                
                if not question:
                    continue
                
                # Process the question
                await self.process_question(question)
                
            except KeyboardInterrupt:
                print("\n\n👋 Demo ended by user")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    async def process_question(self, question: str):
        """Process a customer question"""
        self.request_count += 1
        
        print(f"\n🤖 AI is thinking...")
        
        # Try to answer from knowledge base
        answer = await self.knowledge_base.get_answer(question)
        
        if answer:
            print(f"🤖 AI Response: {answer}")
            print("✅ Question answered from knowledge base")
        else:
            print("🤖 AI Response: I don't have that information right now.")
            print("🔄 Escalating to human supervisor...")
            
            # Create help request
            request = HelpRequest(
                customer_phone="555-123-4567",
                customer_name=f"Interactive Customer {self.request_count}",
                question=question,
                context="Interactive voice demo",
                status="PENDING"
            )
            
            with get_db_session() as db:
                db.add(request)
                db.commit()
                db.refresh(request)
            
            # Notify supervisor
            await self.supervisor_notifier.notify_supervisor(
                request.id,
                f"Interactive Customer {self.request_count}",
                question
            )
            
            print(f"📋 Help Request #{request.id} created and sent to supervisor")
            print("👨‍💼 Supervisor will respond via dashboard at http://localhost:8000/supervisor")

async def main():
    """Main function"""
    demo = InteractiveVoiceDemo()
    await demo.start_interactive_demo()

if __name__ == "__main__":
    print("Starting interactive voice demo...")
    asyncio.run(main())
