"""
Knowledge base management system
"""
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from .database import SessionLocal, KnowledgeEntry
from .config import settings

logger = logging.getLogger(__name__)


class KnowledgeBase:
    """Manages the AI agent's knowledge base"""
    
    def __init__(self):
        self.db = SessionLocal()
    
    async def initialize(self):
        """Initialize knowledge base with default salon information"""
        try:
            # Add default salon knowledge
            default_knowledge = [
                {
                    "question": "What are your hours?",
                    "answer": f"Our hours are {settings.SALON_HOURS}",
                    "context": "Business hours information"
                },
                {
                    "question": "What services do you offer?",
                    "answer": "We offer haircuts, hair coloring, manicures, pedicures, facials, massage therapy, and waxing services.",
                    "context": "Service offerings"
                },
                {
                    "question": "How much does a haircut cost?",
                    "answer": "Our haircuts range from $45 to $65 depending on the stylist and service.",
                    "context": "Pricing information"
                },
                {
                    "question": "Do you take walk-ins?",
                    "answer": "Yes, we accept walk-ins based on availability. We recommend calling ahead to check availability.",
                    "context": "Appointment policy"
                },
                {
                    "question": "What is your phone number?",
                    "answer": f"Our phone number is {settings.SALON_PHONE}",
                    "context": "Contact information"
                },
                {
                    "question": "Where are you located?",
                    "answer": f"We are located at {settings.SALON_ADDRESS}",
                    "context": "Location information"
                }
            ]
            
            for knowledge in default_knowledge:
                await self.add_knowledge(
                    question=knowledge["question"],
                    answer=knowledge["answer"],
                    context=knowledge["context"]
                )
            
            logger.info("Knowledge base initialized with default information")
            
        except Exception as e:
            logger.error(f" Error initializing knowledge base: {e}")
    
    async def get_answer(self, question: str) -> Optional[str]:
        """Get answer for a question from knowledge base"""
        try:
            # Simple keyword matching for now
            # In a real implementation, we'd use semantic search or embeddings
            
            # Normalize question
            question_lower = question.lower().strip()
            
            # Search for matching knowledge entries
            entries = self.db.query(KnowledgeEntry).filter(
                KnowledgeEntry.is_active == True
            ).all()
            
            for entry in entries:
                # Simple keyword matching
                if self._questions_match(question_lower, entry.question.lower()):
                    logger.info(f"📖 Found knowledge match: {entry.question}")
                    return entry.answer
            
            logger.info(f"No knowledge found for: {question}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting answer: {e}")
            return None
    
    def _questions_match(self, question1: str, question2: str) -> bool:
        """Simple question matching logic"""
        # Extract key words from both questions
        words1 = set(question1.split())
        words2 = set(question2.split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by"}
        words1 = words1 - common_words
        words2 = words2 - common_words
        
        # Check for overlap
        overlap = len(words1.intersection(words2))
        total_words = len(words1.union(words2))
        
        # If more than 50% of words overlap, consider it a match
        return overlap / total_words > 0.5 if total_words > 0 else False
    
    async def add_knowledge(self, question: str, answer: str, context: str = None, source_request_id: int = None):
        """Add new knowledge to the knowledge base"""
        try:
            # Check for similar question already exists
            existing = self.db.query(KnowledgeEntry).filter(
                KnowledgeEntry.question.ilike(f"%{question}%")
            ).first()
            
            if existing:
                # Update existing entry
                existing.answer = answer
                existing.context = context
                existing.source_request_id = source_request_id
                logger.info(f"Updated existing knowledge entry: {existing.id}")
            else:
                # Create new entry
                entry = KnowledgeEntry(
                    question=question,
                    answer=answer,
                    context=context,
                    source_request_id=source_request_id
                )
                self.db.add(entry)
                logger.info(f"Added new knowledge entry: {question[:50]}...")
            
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Error adding knowledge: {e}")
            self.db.rollback()
    
    async def get_all_knowledge(self) -> List[Dict[str, Any]]:
        """Get all knowledge entries"""
        try:
            entries = self.db.query(KnowledgeEntry).filter(
                KnowledgeEntry.is_active == True
            ).order_by(KnowledgeEntry.created_at.desc()).all()
            
            return [
                {
                    "id": entry.id,
                    "question": entry.question,
                    "answer": entry.answer,
                    "context": entry.context,
                    "created_at": entry.created_at,
                    "source_request_id": entry.source_request_id
                }
                for entry in entries
            ]
            
        except Exception as e:
            logger.error(f"Error getting knowledge: {e}")
            return []
    
    async def deactivate_knowledge(self, knowledge_id: int):
        """Deactivate a knowledge entry"""
        try:
            entry = self.db.query(KnowledgeEntry).filter(
                KnowledgeEntry.id == knowledge_id
            ).first()
            
            if entry:
                entry.is_active = False
                self.db.commit()
                logger.info(f"Deactivated knowledge entry: {knowledge_id}")
            
        except Exception as e:
            logger.error(f"Error deactivating knowledge: {e}")
            self.db.rollback()
