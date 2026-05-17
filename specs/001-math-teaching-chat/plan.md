# Implementation Plan: Math Teaching Chat Application

**Branch**: `001-math-teaching-chat` | **Date**: 2026-05-16 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-math-teaching-chat/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Build a web-based chat application that connects to a local LM Studio LLM API to provide NHM-pedagogy-driven math teaching for students and teachers. The application accepts text and image input, streams teaching responses progressively, renders mathematical notation via LaTeX, and persists conversations in browser local storage. The backend serves as a thin orchestration layer that manages LLM API calls, OCR fallback for non-vision models, and pedagogical context injection. The frontend is a single-page chat interface with a blue/white/gray/black color palette, image upload capability, and optional role selector.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend)

**Primary Dependencies**: FastAPI (backend API), Vite + React (frontend), KaTeX (LaTeX rendering), Tesseract.js or server-side Tesseract (OCR fallback), uv (Python dependency management)

**Storage**: Browser localStorage (conversation persistence); no server-side database for v1

**Testing**: pytest (backend), Vitest + React Testing Library (frontend), Playwright (e2e)

**Target Platform**: Linux/macOS/Windows local development server; modern web browsers (Chrome, Firefox, Safari, Edge)

**Project Type**: Web application (frontend SPA + lightweight backend API server)

**Performance Goals**: Streaming response begins within 1 minute; complete response within 5 minutes; page load under 3 seconds

**Constraints**: Local-only deployment (LM Studio at 127.0.0.1:1234); no external internet required after initial page load; image uploads under 10MB; session timeout 30 minutes

**Scale/Scope**: Single-user local deployment; no concurrent user support required for v1

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Cognitive-First Pedagogy
- **Pass**: System prompts embed Gan-Jue checks, affective safety language, and germane-load optimization in all LLM system instructions.

### Principle II: Low-Threshold Entry & Intuitive Scaffolding
- **Pass**: LLM system prompt mandates starting with intuitive anchors before symbolic notation; strategic neglect applied in prompt engineering.

### Principle III: Metaphorical Mapping & Spatial Logic
- **Pass**: System prompt includes NHM metaphor catalog; LaTeX rendering supports spatial visualization of formulas.

### Principle IV: Investigative Error Handling & Affective Safety
- **Pass**: Error messages use investigative rhetoric; LLM instructed to frame mistakes as mysteries, not failures.

### Principle V: Slow-Fast-Slow Instructional Rhythm
- **Pass**: LLM system prompt structures responses into three phases; streaming UI naturally supports this rhythm.

### Principle VI: Longitudinal Concept Continuity (G1–G12)
- **Pass**: System prompt references grade-level continuity; markdown_output examples span multiple grade levels.

### Principle VII: Python Development with uv Virtual Environments
- **Pass**: All Python setup uses `uv venv`; documented in quickstart.md and project scripts.

### Pedagogical Content Constraints
- **Pass**: Blueprint file and markdown_output directory referenced in system prompt construction; fallback to analogous patterns documented.

### Quality Gates
- **Pass**: Gan-Jue test embedded in LLM evaluation; uv venv enforced; metaphorical scaffolding in all teaching outputs; investigative rhetoric in error handling.

**Gate Result**: ALL PASS — proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/001-math-teaching-chat/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
backend/
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment and LM Studio configuration
│   ├── models/
│   │   ├── message.py       # User message and system response schemas
│   │   └── session.py       # Conversation session management
│   ├── services/
│   │   ├── llm_client.py    # LM Studio API client with streaming support
│   │   ├── vision_detector.py # Detect LLM vision capability
│   │   ├── ocr_service.py   # OCR fallback for non-vision models
│   │   ├── pedagogy.py      # NHM system prompt construction
│   │   └── example_loader.py # Load markdown_output examples
│   └── api/
│       ├── routes.py        # Chat endpoints (text, image, combined)
│       └── middleware.py    # Error handling, CORS
└── tests/
    ├── unit/
    │   ├── test_llm_client.py
    │   ├── test_vision_detector.py
    │   ├── test_ocr_service.py
    │   └── test_pedagogy.py
    ├── integration/
    │   └── test_chat_api.py
    └── conftest.py

frontend/
├── package.json
├── vite.config.ts
├── index.html
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── components/
│   │   ├── ChatBox.tsx          # Main chat interface
│   │   ├── MessageBubble.tsx    # Individual message display
│   │   ├── ImageUpload.tsx      # Image upload button + preview
│   │   ├── RoleSelector.tsx     # Student/Teacher toggle
│   │   ├── LaTeXRenderer.tsx    # KaTeX rendering component
│   │   ├── TypingIndicator.tsx  # Streaming typing indicator
│   │   └── LoadingSpinner.tsx   # Loading state between submissions
│   ├── hooks/
│   │   ├── useChat.ts           # Chat state management
│   │   ├── useSession.ts        # localStorage session persistence
│   │   └── useStreaming.ts      # SSE/streaming response handling
│   ├── services/
│   │   └── api.ts               # Backend API client
│   ├── styles/
│   │   └── theme.css            # Blue/white/gray/black color palette
│   └── types/
│       └── index.ts             # TypeScript type definitions
└── tests/
    ├── components/
    │   ├── ChatBox.test.tsx
    │   └── LaTeXRenderer.test.tsx
    └── hooks/
        └── useSession.test.ts

docker-compose.yml              # Optional: local dev with backend + frontend
```

**Structure Decision**: Web application with separate backend (FastAPI) and frontend (React + Vite) directories. Backend handles LLM orchestration, OCR, and pedagogy prompt construction. Frontend provides the chat UI with streaming, LaTeX rendering, and localStorage persistence.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No constitution violations detected. All principles satisfied by design.
