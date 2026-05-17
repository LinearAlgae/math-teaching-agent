# Math Teaching Agent

A web-based chat application that connects to a local LM Studio LLM API to provide NHM-pedagogy-driven math teaching for students and teachers. Accepts text and image input, streams teaching responses progressively, renders mathematical notation via LaTeX, and persists conversations in browser local storage.

## Prerequisites

- Python 3.11+ with [uv](https://docs.astral.sh/uv/) installed
- Node.js 18+ with npm
- [LM Studio](https://lmstudio.ai/) running locally at `http://127.0.0.1:1234` with a math-capable model loaded

## Setup

### 1. Backend

```bash
cd backend
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv pip install -e .
```

### 2. Frontend

```bash
cd frontend
npm install
```

### 3. Configure LM Studio

- Open LM Studio, load a model with mathematical reasoning (e.g., Llama 3, Qwen, or LLaVA for vision)
- Start the local server on port 1234
- Verify: `curl http://127.0.0.1:1234/v1/models`

## Running the App

### Quick start (recommended)

```bash
./start.sh
```

This single command kills any existing processes, checks LM Studio, then launches both the backend (port 8000) and frontend (port 5173). Open http://localhost:5173 in your browser.

### Manual start

**Terminal 1 — Backend**:

```bash
cd backend
source .venv/bin/activate
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend**:

```bash
cd frontend
npm run dev
```

Open `http://localhost:5173` in your browser.

## Running Tests

### Backend (pytest)

```bash
cd backend
source .venv/bin/activate
uv run python -m pytest tests/
```

### Frontend (Vitest)

```bash
cd frontend
npx vitest run
```

### E2E (Playwright)

Start both servers, then:

```bash
cd frontend
npx playwright test
```

## Project Structure

```
math-teaching-agent/
├── backend/                  # FastAPI server
│   ├── src/
│   │   ├── main.py           # Entry point
│   │   ├── config.py         # LM Studio configuration
│   │   ├── models/           # Pydantic schemas
│   │   ├── services/         # LLM client, OCR, pedagogy, vision detection
│   │   └── api/              # Route handlers, middleware
│   └── tests/
├── frontend/                 # React + Vite + TypeScript SPA
│   ├── src/
│   │   ├── components/       # ChatBox, MessageBubble, ImageUpload, etc.
│   │   ├── hooks/            # useChat, useSession, useStreaming
│   │   └── services/         # API client
│   └── tests/
├── markdown_output/          # Teaching examples (referenced at runtime)
└── YouTube Math Pedagogy Instructional Blueprint.md
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, httpx, pytesseract |
| Frontend | TypeScript, React 18, Vite 8 |
| Math Rendering | KaTeX |
| Testing | pytest, Vitest, Playwright |
| Linting | ruff (backend), ESLint + Prettier (frontend) |

## Troubleshooting

- **"LM Studio API unavailable"**: Ensure LM Studio is running and the server is started on port 1234
- **Image upload fails**: Check format (PNG/JPEG/WebP) and size (under 10MB)
- **LaTeX not rendering**: Verify KaTeX loaded correctly; check browser console
- **Session not persisting**: Ensure browser localStorage is enabled
