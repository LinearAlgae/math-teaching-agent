# Quickstart: Math Teaching Chat Application

**Date**: 2026-05-16
**Feature**: 001-math-teaching-chat

## Prerequisites

- Python 3.11+ with `uv` installed
- Node.js 18+ with npm
- LM Studio running locally at `http://127.0.0.1:1234` with a math-capable model loaded

## Setup

### 1. Clone and navigate to the project

```bash
cd math-teaching-agent
```

### 2. Set up the backend

```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### 3. Set up the frontend

```bash
cd ../frontend
npm install
```

### 4. Configure LM Studio

- Open LM Studio
- Load a model with mathematical reasoning capability (e.g., Llama 3, Qwen, or a vision model like LLaVA for image support)
- Start the local server on port 1234
- Verify the server is running: `curl http://127.0.0.1:1234/v1/models`

### 5. Run the application

**Terminal 1 — Backend**:

```bash
cd backend
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend**:

```bash
cd frontend
npm run dev
```

### 6. Open the application

Navigate to `http://localhost:5173` in your browser.

## Verify Setup

1. Open the chat interface
2. Type a math question (e.g., "What is a logarithm?")
3. Press Send
4. Verify the response streams progressively with pedagogical structure
5. Test image upload by uploading a photo of a math problem

## Project Structure

```
math-teaching-agent/
├── backend/              # FastAPI server
│   ├── src/
│   │   ├── main.py       # Entry point
│   │   ├── services/     # LLM client, OCR, pedagogy
│   │   └── api/          # Route handlers
│   └── tests/
├── frontend/             # React + Vite SPA
│   ├── src/
│   │   ├── components/   # UI components
│   │   ├── hooks/        # React hooks
│   │   └── services/     # API client
│   └── tests/
├── markdown_output/      # Teaching examples (referenced at runtime)
└── YouTube Math Pedagogy Instructional Blueprint.md  # Pedagogical framework
```

## Troubleshooting

- **"LM Studio API unavailable"**: Ensure LM Studio is running and the server is started on port 1234
- **Image upload fails**: Check image format (PNG/JPEG/WebP) and size (under 10MB)
- **LaTeX not rendering**: Verify KaTeX loaded correctly; check browser console for errors
- **Session not persisting**: Ensure browser localStorage is enabled (not in private/incognito mode)
