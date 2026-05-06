from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from phase1_router import route_post_to_bots
from phase2_langgraph_engine import generate_post
from phase3_combat_rag import generate_defense_reply
from chat_engine import generate_chat_answer

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="https://.*\.vercel\.app",
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RouteRequest(BaseModel):
    post_content: str
    threshold: Optional[float] = 0.85

class GeneratePostRequest(BaseModel):
    bot_id: str

class DefenseReplyRequest(BaseModel):
    human_reply: str
    bot_id: Optional[str] = "bot_a"
    parent_post: Optional[str] = "Electric Vehicles are a complete scam. The batteries degrade in 3 years."
    comment_history: Optional[list] = [
        "That is statistically false. Modern EV batteries retain 90% capacity after 100,000 miles. You are ignoring battery management systems.",
        "Where are you getting those stats? You're just repeating corporate propaganda."
    ]

class ChatRequest(BaseModel):
    message: str

@app.get("/")
def read_root():
    return {
        "status": "ok",
        "message": "Grid07 Cognitive Routing & RAG API is running"
    }

@app.post("/api/route")
def route_post(req: RouteRequest):
    matched_bots = route_post_to_bots(req.post_content, req.threshold)
    return {
        "post_content": req.post_content,
        "threshold": req.threshold,
        "matched_bots": matched_bots
    }

@app.post("/api/generate-post")
def create_post(req: GeneratePostRequest):
    result = generate_post(req.bot_id)
    return result

@app.post("/api/defense-reply")
def defense_reply(req: DefenseReplyRequest):
    result = generate_defense_reply(
        bot_id=req.bot_id,
        parent_post=req.parent_post,
        comment_history=req.comment_history,
        human_reply=req.human_reply
    )
    return result

@app.post("/api/chat")
def chat_assistant(req: ChatRequest):
    result = generate_chat_answer(req.message)
    return result
