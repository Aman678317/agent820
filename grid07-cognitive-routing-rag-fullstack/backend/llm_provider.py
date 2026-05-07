import google.generativeai as genai  # pyright: ignore[reportMissingImports]
from langchain_openai import ChatOpenAI  # pyright: ignore[reportMissingImports]
from langchain.schema import HumanMessage, SystemMessage  # pyright: ignore[reportMissingImports]
from config import GEMINI_API_KEY, OPENAI_API_KEY, LLM_PROVIDER

def get_active_provider():
    return LLM_PROVIDER

def generate_ai_response(prompt: str, system_prompt: str = "") -> dict:
    provider = LLM_PROVIDER

    if provider == "auto":
        if GEMINI_API_KEY:
            try:
                return _call_gemini(prompt, system_prompt)
            except Exception as e:
                print(f"Gemini auto failed: {e}. Trying OpenAI...")
                if OPENAI_API_KEY:
                    try:
                        return _call_openai(prompt, system_prompt)
                    except Exception as e2:
                        print(f"OpenAI auto failed: {e2}. Falling back to mock...")
        elif OPENAI_API_KEY:
            try:
                return _call_openai(prompt, system_prompt)
            except Exception as e:
                print(f"OpenAI auto failed: {e}. Falling back to mock...")
        return _mock_response()

    elif provider == "gemini":
        try:
            return _call_gemini(prompt, system_prompt)
        except Exception as e:
            print(f"Gemini failed: {e}. Falling back to mock...")
            return _mock_response()

    elif provider == "openai":
        try:
            return _call_openai(prompt, system_prompt)
        except Exception as e:
            print(f"OpenAI failed: {e}. Falling back to mock...")
            return _mock_response()

    # Default fallback
    return _mock_response()

def _call_gemini(prompt: str, system_prompt: str) -> dict:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt if system_prompt else None)
    response = model.generate_content(prompt)
    return {
        "text": response.text.strip(),
        "provider": "gemini",
        "success": True,
        "fallback": False
    }

def _call_openai(prompt: str, system_prompt: str) -> dict:
    llm = ChatOpenAI(temperature=0.7, openai_api_key=OPENAI_API_KEY, model_name="gpt-4o-mini")
    messages = []
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))
    messages.append(HumanMessage(content=prompt))
    
    res = llm.invoke(messages)
    return {
        "text": res.content.strip(),
        "provider": "openai",
        "success": True,
        "fallback": False
    }

def _mock_response() -> dict:
    return {
        "text": "This is a mock response because real AI providers were unavailable or disabled.",
        "provider": "mock",
        "success": True,
        "fallback": True
    }
