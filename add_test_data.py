"""
Add test data to the system
"""
import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.database import SessionLocal, HelpRequest, RequestStatus


def add_test_requests():
    """Add some test help requests"""
    print("Adding test help requests...")
    
    db = SessionLocal()
    try:
        # Create test requests
        test_requests = [
            {
                "customer_phone": "555-123-4567",
                "customer_name": "Jane Smith",
                "question": "Do you offer pet grooming services?",
                "context": "Customer asking about pet grooming"
            },
            {
                "customer_phone": "555-987-6543",
                "customer_name": "Bob Johnson",
                "question": "What are your prices for hair coloring?",
                "context": "Customer asking about hair coloring prices"
            },
            {
                "customer_phone": "555-456-7890",
                "customer_name": "Alice Brown",
                "question": "Do you have any special packages for bridal parties?",
                "context": "Customer asking about bridal party packages"
            }
        ]
        
        for req_data in test_requests:
            # Check if request already exists
            existing = db.query(HelpRequest).filter(
                HelpRequest.customer_phone == req_data["customer_phone"],
                HelpRequest.question == req_data["question"]
            ).first()
            
            if not existing:
                request = HelpRequest(
                    customer_phone=req_data["customer_phone"],
                    customer_name=req_data["customer_name"],
                    question=req_data["question"],
                    context=req_data["context"],
                    status=RequestStatus.PENDING
                )
                db.add(request)
                print(f"Added request: {req_data['customer_name']} - {req_data['question'][:50]}...")
            else:
                print(f"Request already exists: {req_data['customer_name']}")
        
        db.commit()
        print("Test data added successfully!")
        
    except Exception as e:
        print(f"Error adding test data: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Add test data to the system"""
    print("Adding Test Data to AI Supervisor System")
    print("=" * 50)
    
    add_test_requests()
    
    print("\n Next steps:")
    print("1. Run: python simple_main.py")
    print("2. Open: http://localhost:8000/supervisor")
    print("3. You should see the test requests in the dashboard")


if __name__ == "__main__":
    main()


