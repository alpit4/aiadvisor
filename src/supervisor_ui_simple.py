"""
Simplified Supervisor UI without LiveKit dependencies
"""
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from .database import get_db, HelpRequest, KnowledgeEntry, RequestStatus
from .config import settings

# Create FastAPI app for supervisor UI
app = FastAPI(title="Supervisor Dashboard")

# Templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: Session = Depends(get_db)):
    """Main supervisor dashboard"""
    try:
        # Get pending requests
        pending_requests = db.query(HelpRequest).filter(
            HelpRequest.status == RequestStatus.PENDING
        ).order_by(HelpRequest.created_at.desc()).all()
        
        # Get recent resolved requests
        resolved_requests = db.query(HelpRequest).filter(
            HelpRequest.status == RequestStatus.RESOLVED
        ).order_by(HelpRequest.resolved_at.desc()).limit(10).all()
        
        # Get knowledge entries
        knowledge_entries = db.query(KnowledgeEntry).filter(
            KnowledgeEntry.is_active == True
        ).order_by(KnowledgeEntry.created_at.desc()).limit(20).all()
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "pending_requests": pending_requests,
            "resolved_requests": resolved_requests,
            "knowledge_entries": knowledge_entries,
            "salon_name": settings.SALON_NAME
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/requests", response_class=HTMLResponse)
async def requests_page(request: Request, db: Session = Depends(get_db)):
    """Requests management page"""
    try:
        # Get all requests
        all_requests = db.query(HelpRequest).order_by(
            HelpRequest.created_at.desc()
        ).all()
        
        return templates.TemplateResponse("requests.html", {
            "request": request,
            "requests": all_requests
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/respond/{request_id}")
async def respond_to_request(
    request_id: int,
    response: str = Form(...),
    db: Session = Depends(get_db)
):
    """Handle supervisor response to a help request"""
    try:
        # Get the help request
        help_request = db.query(HelpRequest).filter(
            HelpRequest.id == request_id
        ).first()
        
        if not help_request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        if help_request.status != RequestStatus.PENDING:
            raise HTTPException(status_code=400, detail="Request already processed")
        
        # Update request status
        help_request.status = RequestStatus.RESOLVED
        help_request.supervisor_response = response
        help_request.resolved_at = datetime.utcnow()
        db.commit()
        
        # Add to knowledge base
        from .knowledge_base import KnowledgeBase
        kb = KnowledgeBase()
        await kb.add_knowledge(
            question=help_request.question,
            answer=response,
            context=f"Learned from supervisor response to request #{request_id}",
            source_request_id=request_id
        )
        
        # Notify customer (simulate)
        print(f"\n📱 CUSTOMER NOTIFICATION:")
        print(f"   To: {help_request.customer_phone}")
        print(f"   Message: {response}")
        print(f"   Time: {datetime.utcnow()}\n")
        
        return {"status": "success", "message": "Response submitted successfully"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/timeout/{request_id}")
async def timeout_request(
    request_id: int,
    db: Session = Depends(get_db)
):
    """Mark request as unresolved due to timeout"""
    try:
        # Get the help request
        help_request = db.query(HelpRequest).filter(
            HelpRequest.id == request_id
        ).first()
        
        if not help_request:
            raise HTTPException(status_code=404, detail="Request not found")
        
        # Update request status
        help_request.status = RequestStatus.UNRESOLVED
        help_request.resolved_at = datetime.utcnow()
        db.commit()
        
        # Notify customer about timeout
        print(f"\n TIMEOUT NOTIFICATION:")
        print(f"   Request #{request_id} timed out")
        print(f"   Customer: {help_request.customer_name} ({help_request.customer_phone})")
        print(f"   Question: {help_request.question}\n")
        
        return {"status": "success", "message": "Request marked as unresolved"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/knowledge", response_class=HTMLResponse)
async def knowledge_page(request: Request, db: Session = Depends(get_db)):
    """Knowledge base management page"""
    try:
        # Get all knowledge entries
        knowledge_entries = db.query(KnowledgeEntry).filter(
            KnowledgeEntry.is_active == True
        ).order_by(KnowledgeEntry.created_at.desc()).all()
        
        return templates.TemplateResponse("knowledge.html", {
            "request": request,
            "knowledge_entries": knowledge_entries
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/knowledge/{knowledge_id}/deactivate")
async def deactivate_knowledge(
    knowledge_id: int,
    db: Session = Depends(get_db)
):
    """Deactivate a knowledge entry"""
    try:
        # Get the knowledge entry
        entry = db.query(KnowledgeEntry).filter(
            KnowledgeEntry.id == knowledge_id
        ).first()
        
        if not entry:
            raise HTTPException(status_code=404, detail="Knowledge entry not found")
        
        # Deactivate entry
        entry.is_active = False
        db.commit()
        
        return {"status": "success", "message": "Knowledge entry deactivated"}
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats(db: Session = Depends(get_db)):
    """Get system statistics"""
    try:
        # Count requests by status
        pending_count = db.query(HelpRequest).filter(
            HelpRequest.status == RequestStatus.PENDING
        ).count()
        
        resolved_count = db.query(HelpRequest).filter(
            HelpRequest.status == RequestStatus.RESOLVED
        ).count()
        
        unresolved_count = db.query(HelpRequest).filter(
            HelpRequest.status == RequestStatus.UNRESOLVED
        ).count()
        
        # Count knowledge entries
        knowledge_count = db.query(KnowledgeEntry).filter(
            KnowledgeEntry.is_active == True
        ).count()
        
        return {
            "pending_requests": pending_count,
            "resolved_requests": resolved_count,
            "unresolved_requests": unresolved_count,
            "knowledge_entries": knowledge_count,
            "total_requests": pending_count + resolved_count + unresolved_count
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def create_supervisor_app():
    """Create the supervisor FastAPI app"""
    return app


