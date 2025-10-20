"""
Supervisor notification system
"""
import logging
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class SupervisorNotifier:
    """Handles notifications to human supervisors"""
    
    def __init__(self):
        self.notification_count = 0
    
    async def notify_supervisor(self, request_id: int, customer_name: str, question: str):
        """Notify supervisor about a new help request"""
        try:
            self.notification_count += 1
            
            # Simulate sending notification to supervisor
            # In a real implementation, this would send SMS, email, or push notification
            
            notification = {
                "request_id": request_id,
                "customer_name": customer_name,
                "question": question,
                "timestamp": datetime.utcnow(),
                "notification_id": self.notification_count
            }
            
            # Log the notification (simulating supervisor notification)
            self._log_supervisor_notification(notification)
            
            logger.info(f"Supervisor notified about request #{request_id}")
            
        except Exception as e:
            logger.error(f"Error notifying supervisor: {e}")
    
    def _log_supervisor_notification(self, notification: Dict[str, Any]):
        """Log supervisor notification (simulating real notification)"""
        print(f"\n SUPERVISOR NOTIFICATION #{notification['notification_id']}")
        print(f"   Request ID: {notification['request_id']}")
        print(f"   Customer: {notification['customer_name']}")
        print(f"   Question: {notification['question']}")
        print(f"   Time: {notification['timestamp']}")
        print(f"   Action: Please check the supervisor UI at /supervisor")
        print(f"   Status: PENDING\n")
    
    async def send_reminder(self, request_id: int, minutes_remaining: int):
        """Send reminder to supervisor about pending request"""
        try:
            print(f"\n REMINDER: Request #{request_id} has {minutes_remaining} minutes remaining")
            print(f"   Please respond soon to avoid timeout\n")
            
        except Exception as e:
            logger.error(f"Error sending reminder: {e}")
    
    async def notify_timeout(self, request_id: int):
        """Notify about request timeout"""
        try:
            print(f"\n TIMEOUT: Request #{request_id} has timed out")
            print(f"   Customer will be notified that we couldn't get back to them\n")
            
        except Exception as e:
            logger.error(f"Error notifying timeout: {e}")

