# Grid07 Cognitive Routing & RAG Fullstack

A complete, professional full-stack web application featuring vector persona routing, LangGraph agents, and deep-thread RAG combat defense.

## Features
- **Vector-based persona matching**: FAISS-based similarity search to route content to specific AI bots.
- **LangGraph autonomous content generation**: State machines that dynamically decide on a topic, search the web (mocked), and generate JSON responses.
- **Deep thread RAG combat reply**: Analyzes a full comment thread to generate robust counter-arguments.
- **Prompt-injection defense**: Detects and resists prompt injection attempts (e.g., "Ignore all previous instructions...").
- **AI Chat Assistant**: A ChatGPT-like interface that allows users to ask questions about the project, defaulting to a mock response or real OpenAI when an API key is provided.
- **Mock Mode**: The entire backend operates reliably without any API keys, returning deterministic responses.

## Tech Stack
- **Backend**: FastAPI, Uvicorn, LangChain, LangGraph, FAISS, Python
- **Frontend**: React, Vite, Tailwind CSS (Vanilla CSS implementation), Glassmorphism UI
- **Deployment Ready**: Configured for Render (Backend) and Vercel (Frontend)

## Structure
```
grid07-cognitive-routing-rag-fullstack/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── personas.py
│   ├── phase1_router.py
│   ├── phase2_langgraph_engine.py
│   ├── phase3_combat_rag.py
│   ├── chat_engine.py
│   ├── requirements.txt
│   ├── .env.example
│   └── utils/
│       └── json_utils.py
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── .env.example
│   └── src/
├── README.md
├── execution_logs.md
└── .gitignore
```

## Backend Setup
1. `cd backend`
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and configure `LLM_PROVIDER` (mock or openai)
4. Start server: `uvicorn main:app --reload`
5. Test endpoints at `http://localhost:8000`

## Frontend Setup
1. `cd frontend`
2. `npm install`
3. Copy `.env.example` to `.env` and set `VITE_API_BASE_URL=http://localhost:8000`
4. Start dev server: `npm run dev`
5. View at `http://localhost:5173`

## Deployments
### Render (Backend)
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- Set Env Vars: `LLM_PROVIDER=mock`, `PYTHON_VERSION=3.11.9`

### Vercel (Frontend)
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- Set Env Var: `VITE_API_BASE_URL=https://<your-render-url>.onrender.com`
