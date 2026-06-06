import os
import json
import time
from collections import defaultdict
from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional

from database import engine, Base, get_db
from models import ConsultationSession, BusinessAnalysis
from schemas import Message, ConsultationStartRequest, MessageRequest, SessionResponse, APIKeyRequest
from services.templates import TEMPLATES
from services.agents import DiscoveryAgent, AnalysisAgent, AutomationAgent, ROIAgent, RoadmapAgent
from services.pdf_generator import generate_pdf_report

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="FlowArchitect AI API", version="1.0.0")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global API key storage (can be overwritten via endpoints)
CONFIG = {
    "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", "")
}

class SimpleRateLimiter:
    def __init__(self, requests_per_minute: int = 30):
        self.requests_per_minute = requests_per_minute
        self.history = defaultdict(list)

    def is_rate_limited(self, ip: str) -> bool:
        now = time.time()
        self.history[ip] = [t for t in self.history[ip] if now - t < 60]
        if len(self.history[ip]) >= self.requests_per_minute:
            return True
        self.history[ip].append(now)
        return False

limiter = SimpleRateLimiter(requests_per_minute=25)

def get_agents():
    # Helper to instantiate agents with the current active API key
    key = CONFIG["GEMINI_API_KEY"]
    return {
        "discovery": DiscoveryAgent(api_key=key),
        "analysis": AnalysisAgent(api_key=key),
        "automation": AutomationAgent(api_key=key),
        "roi": ROIAgent(api_key=key),
        "roadmap": RoadmapAgent(api_key=key)
    }


@app.get("/api/health")
def health_check():
    return {"status": "ok", "live_mode": bool(CONFIG["GEMINI_API_KEY"])}

@app.post("/api/settings/apikey")
def save_api_key(req: APIKeyRequest):
    CONFIG["GEMINI_API_KEY"] = req.gemini_api_key.strip()
    # Test connection
    try:
        discovery = DiscoveryAgent(api_key=CONFIG["GEMINI_API_KEY"])
        return {"status": "success", "message": "API key updated", "live_mode": discovery.is_live}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/api/templates")
def get_templates():
    # Return available template keys and labels for front-end selection
    return [
        {"key": "dental_clinic", "label": "Dental Clinic"},
        {"key": "ecommerce_store", "label": "E-commerce Store"},
        {"key": "real_estate", "label": "Real Estate Agency"},
        {"key": "hospital", "label": "Hospital / Medical Center"},
        {"key": "coaching_institute", "label": "Coaching Institute"},
        {"key": "saas_startup", "label": "SaaS Startup"},
        {"key": "restaurant", "label": "Restaurant / Diner"},
        {"key": "marketing_agency", "label": "Digital Marketing Agency"}
    ]

@app.post("/api/consultation/start", response_model=SessionResponse)
def start_consultation(req: ConsultationStartRequest, db: Session = Depends(get_db)):
    # Create new consultation session
    session = ConsultationSession(
        industry=req.industry,
        company_name=req.company_name or "My Business",
        company_size=req.company_size,
        status="discovering",
        current_step=0
    )
    
    # If starting with a template (Demo Mode), populate immediately
    if req.template_key and req.template_key in TEMPLATES:
        tmpl = TEMPLATES[req.template_key]
        session.industry = tmpl["industry"]
        session.company_name = tmpl["company_name"]
        session.company_size = tmpl["company_size"]
        session.status = "completed"
        
        # Add confirmation message
        initial_msg = Message(
            sender="agent",
            agent_name="DiscoveryAgent",
            content=f"Hello! I have loaded the {tmpl['company_name']} profile successfully. Ready to run business diagnostics.",
            timestamp="Just now"
        )
        session.messages = json.dumps([initial_msg.dict()])
        db.add(session)
        db.commit()
        db.refresh(session)
        
        # Build BusinessAnalysis entry immediately for this template
        analysis = BusinessAnalysis(
            session_id=session.id,
            industry=tmpl["industry"],
            company_name=tmpl["company_name"],
            company_size=tmpl["company_size"],
            business_summary=json.dumps(tmpl["business_summary"]),
            pain_point_analysis=json.dumps(tmpl["pain_point_analysis"]),
            automation_readiness=json.dumps(tmpl["automation_readiness"]),
            recommendations=json.dumps(tmpl["recommendations"]),
            tech_stack=json.dumps(tmpl["tech_stack"]),
            roi_prediction=json.dumps(tmpl["roi_prediction"]),
            roadmap_plan=json.dumps(tmpl["roadmap_plan"]),
            workflow_diagram=json.dumps(tmpl["workflow_diagram"])
        )
        db.add(analysis)
        db.commit()
        
        # Reload session
        session.messages = json.dumps([initial_msg.dict()])
    else:
        # Standard onboarding
        welcome_msg = Message(
            sender="agent",
            agent_name="DiscoveryAgent",
            content="Welcome to FlowArchitect AI. I am your Lead Discovery Agent. To begin our operational consultation, what is your company name and which industry do you operate in?",
            timestamp="Just now"
        )
        session.messages = json.dumps([welcome_msg.dict()])
        db.add(session)
        db.commit()
        db.refresh(session)

    # Format response
    msg_list = json.loads(session.messages)
    return SessionResponse(
        id=session.id,
        industry=session.industry,
        company_name=session.company_name,
        company_size=session.company_size,
        status=session.status,
        current_step=session.current_step,
        messages=[Message(**m) for m in msg_list],
        created_at=session.created_at
    )

@app.get("/api/consultation/{session_id}", response_model=SessionResponse)
def get_consultation_session(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Consultation session not found")
    msg_list = json.loads(session.messages)
    return SessionResponse(
        id=session.id,
        industry=session.industry,
        company_name=session.company_name,
        company_size=session.company_size,
        status=session.status,
        current_step=session.current_step,
        messages=[Message(**m) for m in msg_list],
        created_at=session.created_at
    )

@app.post("/api/consultation/{session_id}/message", response_model=SessionResponse)
def send_message(session_id: str, req: MessageRequest, request: Request, db: Session = Depends(get_db)):
    # 1. Rate Limiting Security Check
    ip = request.client.host or "unknown"
    if limiter.is_rate_limited(ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please wait a moment before sending another message."
        )

    session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Consultation session not found")
        
    messages = json.loads(session.messages)

    # 2. Input Relevance / Sanity Check
    # Find the last question asked by the agent to validate against
    last_agent_question = "Welcome to FlowArchitect AI. To begin our operational consultation, what is your company name and which industry do you operate in?"
    for msg in reversed(messages):
        if msg.get("sender") == "agent":
            last_agent_question = msg.get("content", "")
            break

    agents = get_agents()
    validation_res = agents["discovery"].validate_user_response(last_agent_question, req.content)
    
    if not validation_res.get("valid", True):
        # Invalid / irrelevant answer: append message and ask again without advancing step
        user_msg = {
            "sender": "user",
            "content": req.content,
            "timestamp": "Just now"
        }
        agent_msg = {
            "sender": "agent",
            "agent_name": "DiscoveryAgent",
            "content": f"I'm sorry, I couldn't process that response. {validation_res.get('reason', 'Please provide a valid answer.')} Could you please re-answer: {last_agent_question}",
            "timestamp": "Just now"
        }
        
        messages.append(user_msg)
        messages.append(agent_msg)
        session.messages = json.dumps(messages)
        db.commit()
        db.refresh(session)
        
        return SessionResponse(
            id=session.id,
            industry=session.industry,
            company_name=session.company_name,
            company_size=session.company_size,
            status=session.status,
            current_step=session.current_step,
            messages=[Message(**m) for m in messages],
            created_at=session.created_at
        )

    # 3. Valid Answer: Advance and retrieve next question
    user_msg = {
        "sender": "user",
        "content": req.content,
        "timestamp": "Just now"
    }
    messages.append(user_msg)
    
    # Update quick metadata from first couple of replies if missing
    if session.current_step == 0:
        session.company_name = req.content[:100]
    elif session.current_step == 1:
        session.company_size = req.content[:50]
        
    # Increment step
    session.current_step += 1
    
    # Assemble simple context dictionary
    context = {
        "industry": session.industry,
        "company_name": session.company_name,
        "company_size": session.company_size
    }
    
    next_question = agents["discovery"].get_next_question(messages, context, session.current_step)
    
    # Update industry metadata if parsed by agent or user
    if session.current_step == 1 and not session.industry:
        session.industry = "Business Services"
        
    # Save agent response
    agent_msg = {
        "sender": "agent",
        "agent_name": next_question["agent_name"],
        "content": next_question["content"],
        "timestamp": "Just now"
    }
    messages.append(agent_msg)
    
    # Update session state
    session.messages = json.dumps(messages)
    
    if next_question.get("completed"):
        session.status = "analyzing"
        
    db.commit()
    db.refresh(session)
    
    return SessionResponse(
        id=session.id,
        industry=session.industry,
        company_name=session.company_name,
        company_size=session.company_size,
        status=session.status,
        current_step=session.current_step,
        messages=[Message(**m) for m in messages],
        created_at=session.created_at
    )


@app.post("/api/consultation/{session_id}/analyze")
def run_analysis(session_id: str, db: Session = Depends(get_db)):
    session = db.query(ConsultationSession).filter(ConsultationSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Consultation session not found")
        
    # Check if analysis already exists
    existing = db.query(BusinessAnalysis).filter(BusinessAnalysis.session_id == session_id).first()
    if existing:
        return {
            "session_id": session_id,
            "industry": existing.industry,
            "company_name": existing.company_name,
            "company_size": existing.company_size,
            "business_summary": json.loads(existing.business_summary),
            "pain_points": json.loads(existing.pain_point_analysis),
            "readiness_scores": json.loads(existing.automation_readiness),
            "recommendations": json.loads(existing.recommendations),
            "tech_stack": json.loads(existing.tech_stack),
            "roi_prediction": json.loads(existing.roi_prediction),
            "roadmap_plan": json.loads(existing.roadmap_plan),
            "workflow_diagram": json.loads(existing.workflow_diagram)
        }

        
    messages = json.loads(session.messages)
    agents = get_agents()
    
    context = {
        "industry": session.industry or "General Services",
        "company_name": session.company_name or "My Business",
        "company_size": session.company_size or "5-20 employees"
    }
    
    # 1. Run Analysis Agent
    analysis_res = agents["analysis"].analyze(messages, context)
    
    # 2. Run Automation Agent
    auto_res = agents["automation"].generate_recommendations(analysis_res)
    
    # 3. Run ROI Agent
    roi_res = agents["roi"].estimate_roi(analysis_res, context)
    
    # 4. Run Roadmap Agent
    roadmap_res = agents["roadmap"].generate_roadmap(auto_res["recommendations"], analysis_res["industry"])
    
    # 5. Build default workflow nodes/edges based on generated recommendations
    nodes = [
        {"id": "n1", "label": "Client Inquiry Received", "type": "trigger", "x": 100, "y": 200, "details": "Customer contact initiated."}
    ]
    edges = []
    
    x_offset = 280
    for idx, rec in enumerate(auto_res["recommendations"]):
        node_id = f"n{idx+2}"
        nodes.append({
            "id": node_id,
            "label": rec["title"],
            "type": "process" if idx < len(auto_res["recommendations"])-1 else "action",
            "x": x_offset,
            "y": 200,
            "details": rec["solution"]
        })
        edges.append({
            "source": f"n{idx+1}",
            "target": node_id
        })
        x_offset += 180
        
    # Add final conversion node
    nodes.append({
        "id": f"n{len(nodes)+1}",
        "label": "Operational Efficiency Unlocked",
        "type": "action",
        "x": x_offset,
        "y": 200,
        "details": "Friction resolved; automated checks and reports synchronized."
    })
    edges.append({
        "source": f"n{len(nodes)-1}",
        "target": f"n{len(nodes)}"
    })
    
    workflow_res = {
        "nodes": nodes,
        "edges": edges
    }
    
    # Save BusinessAnalysis record
    db_analysis = BusinessAnalysis(
        session_id=session_id,
        industry=analysis_res.get("industry", context["industry"]),
        company_name=analysis_res.get("company_name", context["company_name"]),
        company_size=analysis_res.get("company_size", context["company_size"]),
        business_summary=json.dumps(analysis_res.get("business_summary")),
        pain_point_analysis=json.dumps(analysis_res.get("pain_points")),
        automation_readiness=json.dumps(analysis_res.get("readiness_scores")),
        recommendations=json.dumps(auto_res.get("recommendations")),
        tech_stack=json.dumps(auto_res.get("tech_stack")),
        roi_prediction=json.dumps(roi_res),
        roadmap_plan=json.dumps(roadmap_res),
        workflow_diagram=json.dumps(workflow_res)
    )
    
    session.status = "completed"
    db.add(db_analysis)
    db.commit()
    
    return {
        "session_id": session_id,
        "industry": db_analysis.industry,
        "company_name": db_analysis.company_name,
        "company_size": db_analysis.company_size,
        "business_summary": analysis_res.get("business_summary"),
        "pain_points": analysis_res.get("pain_points"),
        "readiness_scores": analysis_res.get("readiness_scores"),
        "recommendations": auto_res.get("recommendations"),
        "tech_stack": auto_res.get("tech_stack"),
        "roi_prediction": roi_res,
        "roadmap_plan": roadmap_res,
        "workflow_diagram": workflow_res
    }

@app.get("/api/consultation/{session_id}/analysis")
def get_analysis(session_id: str, db: Session = Depends(get_db)):
    analysis = db.query(BusinessAnalysis).filter(BusinessAnalysis.session_id == session_id).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found. Run analyze first.")
        
    return {
        "session_id": session_id,
        "industry": analysis.industry,
        "company_name": analysis.company_name,
        "company_size": analysis.company_size,
        "business_summary": json.loads(analysis.business_summary),
        "pain_points": json.loads(analysis.pain_point_analysis),
        "readiness_scores": json.loads(analysis.automation_readiness),
        "recommendations": json.loads(analysis.recommendations),
        "tech_stack": json.loads(analysis.tech_stack),
        "roi_prediction": json.loads(analysis.roi_prediction),
        "roadmap_plan": json.loads(analysis.roadmap_plan),
        "workflow_diagram": json.loads(analysis.workflow_diagram)
    }

@app.get("/api/reports/{session_id}/pdf")
def download_pdf(session_id: str, db: Session = Depends(get_db)):
    analysis = db.query(BusinessAnalysis).filter(BusinessAnalysis.session_id == session_id).first()
    if not analysis:
        # See if we can load template directly as a fallback
        if session_id in TEMPLATES:
            # Generate from template mock
            tmpl = TEMPLATES[session_id]
            pdf_data = {
                "company_name": tmpl["company_name"],
                "industry": tmpl["industry"],
                "company_size": tmpl["company_size"],
                "business_summary": tmpl["business_summary"],
                "pain_points": tmpl["pain_point_analysis"],
                "readiness_scores": tmpl["automation_readiness"],
                "recommendations": tmpl["recommendations"],
                "tech_stack": tmpl["tech_stack"],
                "roi_prediction": tmpl["roi_prediction"],
                "roadmap_plan": tmpl["roadmap_plan"],
            }
            pdf_buffer = generate_pdf_report(pdf_data)
            return StreamingResponse(
                pdf_buffer,
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename=flowarchitect_{session_id}_report.pdf"}
            )
        raise HTTPException(status_code=404, detail="Report analysis not found.")

    pdf_data = {
        "company_name": analysis.company_name,
        "industry": analysis.industry,
        "company_size": analysis.company_size,
        "business_summary": json.loads(analysis.business_summary),
        "pain_points": json.loads(analysis.pain_point_analysis),
        "readiness_scores": json.loads(analysis.automation_readiness),
        "recommendations": json.loads(analysis.recommendations),
        "tech_stack": json.loads(analysis.tech_stack),
        "roi_prediction": json.loads(analysis.roi_prediction),
        "roadmap_plan": json.loads(analysis.roadmap_plan),
    }

    pdf_buffer = generate_pdf_report(pdf_data)
    filename = f"flowarchitect_report_{analysis.company_name.replace(' ', '_')}.pdf"
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
