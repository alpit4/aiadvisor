"""
Voice AI Agent for LiveKit integration
Handles voice calls and escalates to human supervisors when needed
"""

import asyncio
import logging
from typing import Optional
from livekit import rtc
from livekit.agents import AutoSubscribe, JobContext, WorkerOptions, cli
from livekit.agents.voice_assistant import VoiceAssistant, VoiceAssistantOptions
from livekit.plugins import openai

from .config import settings
from .database import get_db_session, HelpRequest
from .knowledge_base import KnowledgeBase
from .supervisor_notifier import SupervisorNotifier
from .supervisor_ui_simple import app as supervisor_app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SalonVoiceAgent:
    """Voice AI agent for salon customer service"""
    
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.supervisor_notifier = SupervisorNotifier()
        self.current_request: Optional[HelpRequest] = None
        
    async def handle_voice_call(self, ctx: JobContext):
        """Handle incoming voice calls"""
        logger.info("Voice call started")
        
        # Wait for participant to join
        await ctx.wait_for_participant_connected()
        participant = ctx.room.remote_participants[0]
        logger.info(f"Participant connected: {participant.identity}")
        
        # Create voice assistant
        assistant = VoiceAssistant(
            options=VoiceAssistantOptions(
                instructions=f"""
                You are a helpful AI assistant for {settings.SALON_NAME}.
                You can help customers with:
                - Business hours: {settings.SALON_HOURS}
                - Phone number: {settings.SALON_PHONE}
                - Address: {settings.SALON_ADDRESS}
                - Services and pricing
                - Appointments and walk-ins
                
                If you don't know the answer to a question, say:
                "I don't have that information right now. Let me connect you with a human supervisor who can help you better."
                """,
                voice="alloy",  # OpenAI voice
                language="en",
            )
        )
        
        # Start the assistant
        await assistant.start(ctx.room)
        
        # Handle conversation
        try:
            while True:
                # Check if we have a pending request that needs escalation
                if self.current_request and self.current_request.status == "pending":
                    # Check if we should escalate this request
                    if await self.should_escalate():
                        await self.escalate_to_supervisor(participant.identity)
                        break
                
                await asyncio.sleep(1)
                
        except Exception as e:
            logger.error(f"Error in voice call: {e}")
        finally:
            await assistant.aclose()
            logger.info("Voice call ended")
    
    async def should_escalate(self) -> bool:
        """Determine if current request should be escalated"""
        if not self.current_request:
            return False
            
        # Check if request has been pending for too long
        # or if it's a complex question that needs human help
        return True  # For demo purposes, always escalate
    
    async def escalate_to_supervisor(self, customer_phone: str):
        """Escalate current request to human supervisor"""
        logger.info(f"Escalating request for {customer_phone} to supervisor")
        
        if self.current_request:
            # Notify supervisor
            await self.supervisor_notifier.notify_supervisor(
                self.current_request.id,
                f"Voice call escalation from {customer_phone}"
            )
            
            # Update request status
            with get_db_session() as db:
                request = db.query(HelpRequest).filter(
                    HelpRequest.id == self.current_request.id
                ).first()
                if request:
                    request.status = "pending"
                    db.commit()

# Global agent instance
agent = SalonVoiceAgent()

async def entrypoint(ctx: JobContext):
    """Entry point for LiveKit agent"""
    await agent.handle_voice_call(ctx)

if __name__ == "__main__":
    # Configure OpenAI
    openai.api_key = settings.OPENAI_API_KEY
    
    # Start the agent
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            auto_subscribe=AutoSubscribe.AUDIO_ONLY,
        )
    )
