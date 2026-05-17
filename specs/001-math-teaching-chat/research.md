# Research: Math Teaching Chat Application

**Date**: 2026-05-16
**Feature**: 001-math-teaching-chat

## Decision: Backend Framework Selection

**Chosen**: FastAPI (Python)

**Rationale**: FastAPI provides native async support for streaming LLM responses, automatic OpenAPI schema generation, and integrates cleanly with the uv dependency management mandated by the constitution. Python is the natural choice given the project's Python-first development workflow and the need to process markdown teaching materials.

**Alternatives considered**:
- Express.js (Node.js): Good for streaming but would require separate Python tooling for OCR/markdown processing
- Flask: Simpler but lacks native async streaming support
- Go: Faster but heavier development overhead for this scope

## Decision: Frontend Framework Selection

**Chosen**: React + Vite + TypeScript

**Rationale**: React has the richest ecosystem for chat UI components, KaTeX integration libraries, and state management for streaming responses. Vite provides fast development hot-reload and optimized production builds. TypeScript ensures type safety across the message/session data models.

**Alternatives considered**:
- Vue 3: Comparable but smaller ecosystem for KaTeX streaming integration
- Svelte: Smaller bundle but fewer mature chat component libraries
- Vanilla JS + HTMX: Simpler but insufficient for complex streaming + LaTeX rendering

## Decision: Streaming Protocol

**Chosen**: Server-Sent Events (SSE) via FastAPI's StreamingResponse

**Rationale**: SSE provides unidirectional streaming from server to client, which matches the chat response pattern perfectly. It's simpler than WebSockets (no connection management overhead) and has native browser support. FastAPI's `StreamingResponse` integrates directly with async generators for LLM token streaming.

**Alternatives considered**:
- WebSockets: Bidirectional but overkill for response-only streaming
- HTTP chunked transfer: Works but SSE provides reconnection and event semantics
- Polling: Simpler but higher latency and server load

## Decision: OCR Engine for Vision Fallback

**Chosen**: Tesseract.js (client-side) with server-side Tesseract as fallback

**Rationale**: Tesseract.js runs in the browser, eliminating server-side OCR dependencies for the common case. For complex math notation that Tesseract.js struggles with, the backend can use pytesseract. This dual approach matches the constitution's "low-threshold entry" principle by keeping the default path lightweight.

**Alternatives considered**:
- Server-side Tesseract only: Adds server dependency but more accurate for math
- Mathpix API: Best accuracy but requires external API key (violates local-only constraint)
- PaddleOCR: Good for Chinese text but heavier deployment footprint

## Decision: LaTeX Rendering Library

**Chosen**: KaTeX (not MathJax)

**Rationale**: KaTeX is significantly faster than MathJax for rendering, which matters for streaming responses where formulas appear incrementally. KaTeX's synchronous rendering model prevents layout shifts during streaming. MathJax is more comprehensive but slower and uses async rendering that conflicts with streaming UX.

**Alternatives considered**:
- MathJax: More complete LaTeX support but 3-5x slower rendering
- Mathlive: Interactive editing but overkill for read-only rendering

## Decision: Conversation Storage

**Chosen**: Browser localStorage with 30-minute inactivity timeout

**Rationale**: Matches the spec clarification exactly. No server-side storage needed for v1, keeping the architecture simple. localStorage is synchronous, simple to implement, and persists across page refreshes. The 30-minute timeout is implemented via timestamp comparison on session restore.

**Alternatives considered**:
- IndexedDB: More capacity but unnecessary for text-based chat history
- Server-side sessions: Requires database infrastructure not needed for local deployment
- sessionStorage: Lost on tab close, violating the page-restore requirement

## Decision: LLM Vision Capability Detection

**Chosen**: Query LM Studio's model metadata endpoint + capability test

**Rationale**: LM Studio exposes model information that includes vision capability flags. As a fallback, send a small test image prompt and check if the model accepts it. This dual approach handles both explicit metadata and implicit capability detection.

**Alternatives considered**:
- Hardcoded model list: Fragile when users change models
- Always assume no vision: Wastes capability when vision model is loaded
- Always assume vision: Fails silently with text-only models

## Decision: Pedagogical System Prompt Construction

**Chosen**: Dynamic prompt assembly from constitution principles + loaded examples

**Rationale**: The system prompt is constructed at request time by combining: (1) core NHM principles from the constitution, (2) relevant examples from markdown_output directory matched to the identified math subject, (3) role context (student vs teacher), and (4) conversation history. This ensures every response is pedagogically grounded without hardcoding prompts.

**Alternatives considered**:
- Static system prompt: Cannot adapt to different math subjects or roles
- Fine-tuned model: Requires training data and infrastructure beyond scope
- Prompt templates only: Loses the rich example-based grounding from markdown_output
