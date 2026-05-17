# Tasks: Math Teaching Chat Application

**Input**: Design documents from `/specs/001-math-teaching-chat/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Included — the implementation plan defines testing infrastructure (pytest, Vitest, Playwright). Test tasks are organized per user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create backend directory structure (backend/src/models, backend/src/services, backend/src/api, backend/tests/unit, backend/tests/integration)
- [x] T002 [P] Create frontend directory structure (frontend/src/components, frontend/src/hooks, frontend/src/services, frontend/src/styles, frontend/src/types, frontend/tests/components, frontend/tests/hooks)
- [x] T003 Initialize Python backend with uv: create pyproject.toml with FastAPI, httpx, pytesseract, python-multipart dependencies in backend/
- [x] T004 [P] Initialize frontend with Vite + React + TypeScript: create package.json, vite.config.ts, tsconfig.json in frontend/
- [x] T005 [P] Configure backend linting and formatting (ruff) in backend/pyproject.toml
- [x] T006 [P] Configure frontend linting and formatting (ESLint + Prettier) in frontend/package.json
- [x] T007 Create .gitignore for Python + Node.js project at repository root

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Create environment configuration module in backend/src/config.py (LM Studio URL, port, timeout settings, markdown_output path)
- [x] T009 Create FastAPI application entry point in backend/src/main.py with CORS middleware and basic health endpoint
- [x] T010 [P] Create Pydantic data models for UserMessage, ImageAttachment, SystemResponse, ConversationSession in backend/src/models/message.py
- [x] T011 [P] Create session management model and localStorage-compatible serialization in backend/src/models/session.py
- [x] T012 Implement LM Studio API client with streaming support (SSE via async generator) in backend/src/services/llm_client.py
- [x] T013 Implement LLM vision capability detection service (metadata query + capability test) in backend/src/services/vision_detector.py
- [x] T014 Implement OCR fallback service using pytesseract for non-vision models in backend/src/services/ocr_service.py
- [x] T015 Implement NHM pedagogical system prompt construction service in backend/src/services/pedagogy.py (loads constitution principles, builds role-aware prompts)
- [x] T016 Implement markdown_output example loader service in backend/src/services/example_loader.py (parses directory, indexes by subject/grade)
- [x] T017 Implement API route handlers for POST /api/chat (SSE streaming), GET /api/session/{id}, GET /api/health, POST /api/vision/detect in backend/src/api/routes.py
- [x] T018 Implement error handling middleware with user-friendly messages and investigative rhetoric in backend/src/api/middleware.py
- [x] T019 Create TypeScript type definitions matching backend models in frontend/src/types/index.ts
- [x] T020 Implement backend API client (fetch wrapper with SSE support) in frontend/src/services/api.ts
- [x] T021 Create blue/white/gray/black color theme CSS in frontend/src/styles/theme.css

**Checkpoint**: Foundation ready — user story implementation can now begin in parallel

---

## Phase 3: User Story 1 — Student submits math problem and receives guided teaching (Priority: P1)

**Goal**: A student can type or upload a math problem and receive a pedagogically structured, streamed teaching response with LaTeX rendering and conversational continuity.

**Independent Test**: Submit a single math problem (text or image) and verify the response follows NHM teaching principles (metaphors, spatial reasoning, slow-fast-slow rhythm, affective safety).

### Tests for User Story 1

- [x] T022 [P] [US1] Unit test for LLM client streaming in backend/tests/unit/test_llm_client.py
- [x] T023 [P] [US1] Unit test for pedagogy prompt construction in backend/tests/unit/test_pedagogy.py
- [x] T024 [US1] Integration test for POST /api/chat text-only endpoint in backend/tests/integration/test_chat_api.py
- [x] T025 [P] [US1] Unit test for useChat hook state management in frontend/tests/hooks/useChat.test.ts
- [x] T026 [P] [US1] Component test for ChatBox rendering in frontend/tests/components/ChatBox.test.tsx

### Implementation for User Story 1

- [x] T027 [US1] Wire POST /api/chat route to LLM client + pedagogy service for text-only input (FR-001, FR-002, FR-005, FR-006, FR-008, FR-011)
- [x] T028 [US1] Implement SSE streaming response handler in backend/src/api/routes.py with start/token/complete/error events (FR-019)
- [x] T029 [P] [US1] Create ChatBox component with text input box and send button in frontend/src/components/ChatBox.tsx (FR-001, FR-002)
- [x] T030 [P] [US1] Create MessageBubble component with LaTeX rendering via KaTeX in frontend/src/components/MessageBubble.tsx (FR-015, FR-021)
- [x] T031 [P] [US1] Create LaTeXRenderer component with plain-text fallback on parse failure in frontend/src/components/LaTeXRenderer.tsx (FR-021)
- [x] T032 [P] [US1] Create TypingIndicator component for streaming state in frontend/src/components/TypingIndicator.tsx (FR-019)
- [x] T033 [P] [US1] Create LoadingSpinner component for pre-streaming state in frontend/src/components/LoadingSpinner.tsx (FR-020)
- [x] T034 [US1] Implement useChat hook for message state, send/receive logic, and SSE connection in frontend/src/hooks/useChat.ts (FR-009)
- [x] T035 [US1] Implement useStreaming hook for SSE event parsing and incremental content accumulation in frontend/src/hooks/useStreaming.ts (FR-019)
- [x] T036 [US1] Wire App.tsx to render ChatBox with theme, connect to backend API (FR-001)
- [x] T037 [US1] Add conversational context support: pass session history to LLM for follow-up questions in backend/src/api/routes.py (FR-009)

**Checkpoint**: At this point, User Story 1 should be fully functional — student can submit text math problems, receive streamed pedagogically structured responses with LaTeX rendering, and continue the conversation.

---

## Phase 4: User Story 2 — Teacher requests syllabus or teaching methodology guidance (Priority: P2)

**Goal**: A teacher can request a syllabus or teaching plan and receive NHM-aligned structured content with references to markdown_output examples.

**Independent Test**: Submit a teacher-oriented request (e.g., "Create a syllabus for G8 logarithms") and verify the output includes NHM-aligned teaching methodology, references to example materials, and structured lesson plans.

### Tests for User Story 2

- [x] T038 [P] [US2] Unit test for example_loader subject matching in backend/tests/unit/test_example_loader.py
- [x] T042 [P] [US2] Create RoleSelector component (Student/Teacher toggle) in frontend/src/components/RoleSelector.tsx (FR-018)
- [x] T043 [US2] Integrate RoleSelector into ChatBox header; pass role to API requests in frontend/src/components/ChatBox.tsx (FR-017, FR-018)
- [x] T044 [US2] Implement implicit role detection: analyze user input intent in backend/src/services/pedagogy.py when role=auto (FR-017)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently — teachers can request syllabi with NHM methodology references.

---

## Phase 5: User Story 3 — User uploads both text and image for combined context (Priority: P3)

**Goal**: A user can submit combined text + image input and receive a unified teaching response that addresses visual elements referenced in the text.

**Independent Test**: Submit a combined text + image input and verify the response addresses both modalities coherently.

### Tests for User Story 3

- [x] T045 [P] [US3] Unit test for vision_detector service in backend/tests/unit/test_vision_detector.py
- [x] T046 [US3] Integration test for POST /api/chat with multipart/form-data (text + image) in backend/tests/integration/test_chat_api.py
- [x] T047 [P] [US3] Component test for ImageUpload in frontend/tests/components/ImageUpload.test.tsx (create file)

### Implementation for User Story 3

- [x] T048 [P] [US3] Create ImageUpload component with file picker, drag-and-drop, and preview in frontend/src/components/ImageUpload.tsx (FR-003)
- [x] T049 [P] [US3] Implement image-to-base64 encoding and validation (format, size) in frontend/src/services/api.ts (FR-003, FR-004)
- [x] T050 [US3] Enhance POST /api/chat route to accept multipart/form-data with text + images in backend/src/api/routes.py (FR-004)
- [x] T051 [US3] Implement vision-aware image routing: if LLM supports vision, send image directly; if not, trigger OCR fallback in backend/src/services/llm_client.py (FR-013, FR-014)
- [x] T052 [US3] Integrate OCR-extracted text into LLM prompt when vision not available in backend/src/services/ocr_service.py (FR-014)
- [x] T053 [US3] Integrate ImageUpload into ChatBox component; send combined text + image messages via API in frontend/src/components/ChatBox.tsx (FR-004)
- [x] T054 [US3] Handle OCR failure gracefully with user-friendly investigative error message in backend/src/api/middleware.py (FR-016)

**Checkpoint**: All user stories should now be independently functional — combined text + image input with vision/OCR routing.

---

## Phase 6: Session Persistence & Edge Cases

**Purpose**: Conversation persistence, session management, and edge case handling

- [x] T055 [P] Implement useSession hook for localStorage persistence with 30-minute inactivity timeout in frontend/src/hooks/useSession.ts (FR-010)
- [x] T056 Integrate useSession into App.tsx: restore session on page load, handle expiration in frontend/src/App.tsx (FR-010)
- [x] T057 [P] Implement streaming interruption handling: detect connection drop, preserve partial response in frontend/src/hooks/useStreaming.ts
- [x] T058 [P] Implement LaTeX parse failure fallback: display plain-text formatted math when KaTeX fails in frontend/src/components/LaTeXRenderer.tsx (FR-021)
- [x] T059 Add session retrieval endpoint GET /api/session/{sessionId} to backend/src/api/routes.py
- [x] T060 [P] Unit test for useSession hook localStorage logic in frontend/tests/hooks/useSession.test.ts

**Checkpoint**: Session persistence and edge case handling complete.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T061 [P] Write quickstart.md validation: follow quickstart steps end-to-end and document any issues
- [x] T062 [P] Add backend unit tests for config, session model, and middleware in backend/tests/unit/
- [x] T063 Performance optimization: ensure page load under 3 seconds, optimize KaTeX bundle size
- [x] T064 [P] Add Playwright e2e test for full student flow (submit problem → receive response → follow-up) in frontend/tests/e2e/
- [x] T065 [P] Add Playwright e2e test for full teacher flow (request syllabus → receive structured plan)
- [x] T066 Code cleanup: remove unused imports, fix linting warnings across backend and frontend
- [x] T067 Verify constitution compliance: check all 7 principles are reflected in system prompts and UI behavior

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **User Stories (Phase 3–5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Session Persistence (Phase 6)**: Depends on US1 completion (needs chat infrastructure)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) — Builds on shared chat infrastructure from US1
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) — Builds on chat infrastructure; OCR/vision services from Phase 2

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Backend before frontend integration
- Core implementation before edge case handling
- Story complete before moving to next priority

### Parallel Opportunities

- T001–T007 (Setup): T002, T004, T005, T006 can run in parallel
- T008–T021 (Foundational): T010, T011 can run in parallel; T012, T013, T014, T015, T016 can run in parallel
- T022–T037 (US1): T022, T023, T025, T026 can run in parallel; T029, T030, T031, T032, T033 can run in parallel
- T038–T044 (US2): T038, T042 can run in parallel
- T045–T054 (US3): T045, T047, T048, T049 can run in parallel
- T055–T060 (Phase 6): T055, T057, T058, T060 can run in parallel
- T061–T067 (Phase 7): T061, T062, T063, T064, T065, T066, T067 can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Unit test for LLM client streaming in backend/tests/unit/test_llm_client.py"
Task: "Unit test for pedagogy prompt construction in backend/tests/unit/test_pedagogy.py"
Task: "Unit test for useChat hook state management in frontend/tests/hooks/useChat.test.ts"
Task: "Component test for ChatBox rendering in frontend/tests/components/ChatBox.test.tsx"

# Launch all UI components for User Story 1 together:
Task: "Create ChatBox component with text input box and send button in frontend/src/components/ChatBox.tsx"
Task: "Create MessageBubble component with LaTeX rendering via KaTeX in frontend/src/components/MessageBubble.tsx"
Task: "Create LaTeXRenderer component with plain-text fallback in frontend/src/components/LaTeXRenderer.tsx"
Task: "Create TypingIndicator component for streaming state in frontend/src/components/TypingIndicator.tsx"
Task: "Create LoadingSpinner component for pre-streaming state in frontend/src/components/LoadingSpinner.tsx"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently — submit a math problem, verify streamed pedagogical response with LaTeX rendering
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo (teacher support)
4. Add User Story 3 → Test independently → Deploy/Demo (multimodal input)
5. Add Phase 6 (session persistence) → Test independently
6. Add Phase 7 (polish) → Final validation
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- Total tasks: 67
- Parallel opportunities: 28 tasks marked [P]
