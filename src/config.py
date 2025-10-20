import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    # LiveKit Configuration (Phase 2: optional; empty by default)
    LIVEKIT_URL: str = os.getenv("LIVEKIT_URL", "")
    LIVEKIT_API_KEY: str = os.getenv("LIVEKIT_API_KEY", "")
    LIVEKIT_API_SECRET: str = os.getenv("LIVEKIT_API_SECRET", "")
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ai_supervisor.db")
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Business Configuration
    SALON_NAME: str = "Bella Vista Salon & Spa"
    SALON_HOURS: str = "Monday-Friday: 9AM-7PM, Saturday: 9AM-5PM, Sunday: Closed"
    SALON_PHONE: str = "(555) 123-4567"
    SALON_ADDRESS: str = "123 Main Street, Downtown"
    
    # Request timeout (in minutes)
    REQUEST_TIMEOUT_MINUTES: int = 30


settings = Settings()

