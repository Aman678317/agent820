from config import is_mock, OPENAI_API_KEY

def generate_chat_answer(message: str) -> dict:
    project_context = """
    This project is 'grid07-cognitive-routing-rag-fullstack'.
    Features include:
    - Vector persona routing using FAISS
    - LangGraph autonomous content engine for agents
    - RAG combat reply with prompt-injection defense
    - Deployed with Render (backend) and Vercel (frontend)
    """
    
    if is_mock():
        answer = "I am a mock assistant. You asked: " + message + "\n\nThis project features Vector persona routing, LangGraph agents, RAG combat reply, and prompt-injection defense. Let me know if you need specific details."
        return {
            "answer": answer,
            "provider": "mock",
            "success": True
        }
        
    try:
        from langchain_openai import ChatOpenAI
        from langchain.schema import HumanMessage, SystemMessage
        llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY)
        
        messages = [
            SystemMessage(content=f"You are a helpful AI assistant answering questions about the current project.\nContext:\n{project_context}\nExplain clearly and practically."),
            HumanMessage(content=message)
        ]
        
        res = llm.invoke(messages)
        
        return {
            "answer": res.content.strip(),
            "provider": "openai",
            "success": True
        }
    except Exception as e:
        print("Fallback chat answer:", e)
        return {
            "answer": "Error generating answer. Please try again.",
            "provider": "openai (error)",
            "success": False
        }
