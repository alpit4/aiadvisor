"""
Voice Call Manager
Handles creating and managing voice calls with LiveKit
"""

import asyncio
import logging
from typing import Optional
from livekit import rtc
from livekit.agents import JobContext, WorkerOptions, cli
from livekit.plugins import openai

from .config import settings
from .voice_agent import SalonVoiceAgent

logger = logging.getLogger(__name__)

class VoiceCallManager:
    """Manages voice calls and agent interactions"""
    
    def __init__(self):
        self.agent = SalonVoiceAgent()
        self.active_calls = {}
        
    async def start_voice_call(self, room_name: str, participant_identity: str = "customer"):
        """Start a new voice call"""
        try:
            logger.info(f"Starting voice call in room: {room_name}")
            
            # Create room options
            room_options = rtc.RoomOptions(
                auto_subscribe=rtc.AutoSubscribe.AUDIO_ONLY,
            )
            
            # Connect to room
            room = rtc.Room(room_options)
            await room.connect(settings.LIVEKIT_URL, settings.LIVEKIT_API_KEY, settings.LIVEKIT_API_SECRET)
            
            # Join room
            await room.join(room_name, participant_identity)
            
            # Create job context
            ctx = JobContext(
                room=room,
                participant=room.local_participant,
            )
            
            # Start agent
            await self.agent.handle_voice_call(ctx)
            
        except Exception as e:
            logger.error(f"Error starting voice call: {e}")
            raise
    
    async def stop_voice_call(self, room_name: str):
        """Stop a voice call"""
        if room_name in self.active_calls:
            call = self.active_calls[room_name]
            await call.disconnect()
            del self.active_calls[room_name]
            logger.info(f"Stopped voice call: {room_name}")

# Global voice manager
voice_manager = VoiceCallManager()

async def start_demo_call():
    """Start a demo voice call"""
    room_name = "salon-demo"
    participant_identity = "customer"
    
    try:
        await voice_manager.start_voice_call(room_name, participant_identity)
    except Exception as e:
        logger.error(f"Demo call failed: {e}")

if __name__ == "__main__":
    # Configure OpenAI
    openai.api_key = settings.OPENAI_API_KEY
    
    # Start demo call
    asyncio.run(start_demo_call())
