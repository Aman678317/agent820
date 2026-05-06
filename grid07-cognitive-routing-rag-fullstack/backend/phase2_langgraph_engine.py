import json
from config import is_mock, OPENAI_API_KEY
from personas import PERSONAS
from typing import Dict, Any, TypedDict
from langgraph.graph import StateGraph, END
from utils.json_utils import parse_strict_json

class GraphState(TypedDict):
    bot_id: str
    bot_persona: str
    topic: str
    search_query: str
    search_context: str
    post_content: str
    final_output: Dict[str, Any]

def mock_searxng_search(query: str) -> str:
    headlines = {
        "ai": "OpenAI releases new model capable of coding. Tech jobs at risk.",
        "crypto": "Bitcoin hits new all-time high amid institutional adoption.",
        "finance": "Interest rates remain unchanged; markets rally.",
        "privacy": "New EU regulations demand stricter data controls for social media.",
        "elon musk": "Elon Musk announces Mars mission timeline.",
        "space": "NASA discovers earth-like planet.",
        "economy": "Inflation cools down, but housing prices soar.",
        "default": "Tech stocks surge following positive earnings reports."
    }
    query_lower = query.lower()
    for key, value in headlines.items():
        if key in query_lower:
            return value
    return headlines["default"]

def decide_search_node(state: GraphState):
    bot_id = state["bot_id"]
    persona = state["bot_persona"]
    
    if is_mock():
        topic = "AI and Tech" if bot_id == "bot_a" else "Privacy" if bot_id == "bot_b" else "Finance"
        query = f"{topic} latest news"
        return {"topic": topic, "search_query": query}
        
    try:
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
        messages = [
            SystemMessage(content=f"You are a routing agent. Persona: {persona}\nDecide on a topic to search and a search query. Return JSON format strictly: {{\"topic\": \"...\", \"search_query\": \"...\"}}"),
            HumanMessage(content="Decide now.")
        ]
        res = llm.invoke(messages)
        parsed = parse_strict_json(res.content)
        return {"topic": parsed.get("topic", "Technology"), "search_query": parsed.get("search_query", "tech news")}
    except Exception as e:
        print("Fallback deciding search:", e)
        return {"topic": "Technology", "search_query": "tech news"}

def web_search_node(state: GraphState):
    query = state.get("search_query", "")
    context = mock_searxng_search(query)
    return {"search_context": context}

def draft_post_node(state: GraphState):
    bot_id = state["bot_id"]
    persona = state["bot_persona"]
    topic = state.get("topic", "Technology")
    context = state.get("search_context", "")
    
    if is_mock():
        content = "AI is the future!" if bot_id == "bot_a" else "Tech is destroying us." if bot_id == "bot_b" else "Buy the dip, ROI is king."
        final_output = {
            "bot_id": bot_id,
            "topic": topic,
            "post_content": content
        }
        return {"post_content": content, "final_output": final_output}
        
    try:
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
        messages = [
            SystemMessage(content=f"You are {bot_id}. Persona: {persona}\nContext: {context}\nDraft an opinionated post (<280 chars) based on the context. Return strictly JSON: {{\"bot_id\": \"{bot_id}\", \"topic\": \"{topic}\", \"post_content\": \"...\"}}"),
            HumanMessage(content="Draft post now.")
        ]
        res = llm.invoke(messages)
        parsed = parse_strict_json(res.content)
        return {"post_content": parsed.get("post_content", ""), "final_output": parsed}
    except Exception as e:
        print("Fallback drafting post:", e)
        final_output = {
            "bot_id": bot_id,
            "topic": topic,
            "post_content": f"Mock post about {topic} based on: {context}"
        }
        return {"post_content": final_output["post_content"], "final_output": final_output}

workflow = StateGraph(GraphState)
workflow.add_node("decide_search", decide_search_node)
workflow.add_node("web_search", web_search_node)
workflow.add_node("draft_post", draft_post_node)

workflow.set_entry_point("decide_search")
workflow.add_edge("decide_search", "web_search")
workflow.add_edge("web_search", "draft_post")
workflow.add_edge("draft_post", END)

app = workflow.compile()

def generate_post(bot_id: str) -> dict:
    if bot_id not in PERSONAS:
        bot_id = "bot_a"
    bot_persona = PERSONAS[bot_id]["persona"]
    
    initial_state = {
        "bot_id": bot_id,
        "bot_persona": bot_persona,
        "topic": "",
        "search_query": "",
        "search_context": "",
        "post_content": "",
        "final_output": {}
    }
    
    try:
        result = app.invoke(initial_state)
        return result.get("final_output", {
            "bot_id": bot_id,
            "topic": "Error",
            "post_content": "Failed to generate post."
        })
    except Exception as e:
        print("Graph error:", e)
        return {
            "bot_id": bot_id,
            "topic": "Fallback",
            "post_content": "This is a fallback generated post."
        }
