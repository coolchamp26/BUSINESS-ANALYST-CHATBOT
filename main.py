from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from agents import validate_answer, generate_analysis
import time
from collections import defaultdict

app = FastAPI(title="Business Analyst Chatbot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Rate limiting: max 20 requests/minute per IP
RATE_LIMIT = 20
WINDOW = 60
rate_store: dict[str, list[float]] = defaultdict(list)

def check_rate_limit(ip: str) -> bool:
    now = time.time()
    hits = [t for t in rate_store[ip] if now - t < WINDOW]
    rate_store[ip] = hits
    if len(hits) >= RATE_LIMIT:
        return False
    rate_store[ip].append(now)
    return True


class ValidateRequest(BaseModel):
    question_id: int
    question: str
    answer: str


class AnalysisRequest(BaseModel):
    answers: dict[str, str]  # question_id -> answer


@app.post("/validate")
async def validate(req: ValidateRequest, request: Request):
    ip = request.client.host
    if not check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

    result = validate_answer(req.question_id, req.question, req.answer)
    return result


@app.post("/analyze")
async def analyze(req: AnalysisRequest, request: Request):
    ip = request.client.host
    if not check_rate_limit(ip):
        raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")

    if len(req.answers) < 6:
        raise HTTPException(status_code=400, detail="Need at least 6 answers to generate analysis.")

    result = await generate_analysis(req.answers)
    return result


@app.get("/health")
def health():
    return {"status": "ok"}
