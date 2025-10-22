"""
Voice Demo Script
Demonstrates the voice AI system with LiveKit integration
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.config import settings
from src.voice_manager import voice_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_voice_demo():
    """Run the voice AI demo"""
    print("🎤 Frontdesk AI Supervisor - Voice Demo")
    print("=" * 50)
    
    # Check if we have the required credentials
    if not settings.LIVEKIT_URL or not settings.LIVEKIT_API_KEY or not settings.LIVEKIT_API_SECRET:
        print("❌ Missing LiveKit credentials!")
        print("Please set LIVEKIT_URL, LIVEKIT_API_KEY, and LIVEKIT_API_SECRET in your .env file")
        return
    
    if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_key_here":
        print("❌ Missing OpenAI API key!")
        print("Please set OPENAI_API_KEY in your .env file")
        return
    
    print("✅ Credentials found")
    print(f"📞 Salon: {settings.SALON_NAME}")
    print(f"🌐 LiveKit URL: {settings.LIVEKIT_URL}")
    print()
    
    print("🚀 Starting voice call...")
    print("📱 You can now call the salon using LiveKit!")
    print("💡 The AI will answer and can escalate to human supervisors")
    print()
    
    try:
        # Start voice call
        room_name = "salon-demo"
        await voice_manager.start_voice_call(room_name)
        
    except KeyboardInterrupt:
        print("\n Demo stopped by user")
    except Exception as e:
        print(f"Demo failed: {e}")
        logger.error(f"Demo error: {e}")

def main():
    """Main function"""
    print("Setting up voice demo...")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print(".env file not found!")
        print("Please create a .env file with your LiveKit and OpenAI credentials")
        return
    
    # Run the demo
    asyncio.run(run_voice_demo())

if __name__ == "__main__":
    main()
