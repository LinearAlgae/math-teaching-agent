# Feature Specification: Math Teaching Chat Application

**Feature Branch**: `001-math-teaching-chat`

**Created**: 2026-05-16

**Status**: Draft

**Input**: User description: "Create a web-based math teaching chat application for students and teachers that accepts text and image input, uses NHM pedagogy as the teaching framework, references markdown_output examples, and integrates with LM Studio local LLM API"

## Clarifications

### Session 2026-05-16

- Q: Should role selection be explicit or implicit? → A: Explicit but optional — role selector available in UI but defaults to implicit
- Q: How should image processing handle vision-capable vs text-only LLMs? → A: Dual-mode — use LLM vision if available, fall back to OCR extraction for text-only models
- Q: How should conversation state persist across page refreshes? → A: Browser local storage with session timeout (30 minutes inactivity)
- Q: Should teaching responses stream progressively or appear as a complete batch? → A: Streaming — responses appear token-by-token with a typing indicator while generating
- Q: How should mathematical notation be rendered in the chat interface? → A: LaTeX rendering (KaTeX/MathJax) with formatted text fallback

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student submits math problem and receives guided teaching (Priority: P1)

A student visits the web application, types or uploads an image of a math problem (e.g., a logarithm equation, geometry question, or algebra problem), and submits it. The system identifies the mathematical subject, applies the NHM pedagogical framework (low-threshold entry, metaphorical mapping, Gan-Jue checks, investigative error handling), and generates a step-by-step teaching response that builds intuition before procedure. The student can continue the conversation to ask follow-up questions or request clarification.

**Why this priority**: This is the core value proposition — a student receiving pedagogically sound math instruction through natural conversation.

**Independent Test**: Can be fully tested by submitting a single math problem (text or image) and verifying the response follows NHM teaching principles (metaphors, spatial reasoning, slow-fast-slow rhythm, affective safety).

**Acceptance Scenarios**:

1. **Given** a student has opened the chat interface, **When** they type a math problem in the text input and press send, **Then** the system responds with a pedagogically structured teaching answer that includes intuitive anchoring, metaphorical explanation, and step-by-step guidance
2. **Given** a student has opened the chat interface, **When** they upload an image of a handwritten or printed math problem and press send, **Then** the system processes the image, identifies the mathematical content, and responds with teaching guidance following NHM principles
3. **Given** a student has received an initial teaching response, **When** they ask a follow-up question or request clarification, **Then** the system continues the conversation contextually, maintaining the pedagogical approach

---

### User Story 2 - Teacher requests syllabus or teaching methodology guidance (Priority: P2)

A teacher visits the application and requests a syllabus, teaching methodology, or instructional ideas for a specific mathematical subject or grade level. The system generates structured teaching content that aligns with the NHM Blueprint, referencing relevant examples from the `markdown_output` repository (e.g., 国中学员手册, 教材, 数学科教师共备手册). The output includes lesson structure suggestions, metaphorical mappings, and pacing recommendations following the slow-fast-slow rhythm.

**Why this priority**: Teachers are the second primary user group; enabling them to generate teaching materials expands the application's value beyond individual student tutoring.

**Independent Test**: Can be fully tested by submitting a teacher-oriented request (e.g., "Create a syllabus for G8 logarithms") and verifying the output includes NHM-aligned teaching methodology, references to example materials, and structured lesson plans.

**Acceptance Scenarios**:

1. **Given** a teacher has opened the chat interface, **When** they request a syllabus or teaching plan for a specific math topic, **Then** the system generates a structured teaching document that references NHM pedagogical strategies and relevant examples from the markdown_output repository
2. **Given** a teacher is reviewing generated teaching content, **When** they ask for alternative teaching approaches, **Then** the system provides analogous pedagogical strategies drawn from similar subjects in the example repository

---

### User Story 3 - User uploads both text and image for combined context (Priority: P3)

A user (student or teacher) provides both a text description and an accompanying image to give richer context. For example, a student uploads a photo of a geometry diagram and adds text like "I don't understand how to find the area of the shaded region." The system processes both inputs together and provides a unified teaching response that addresses the specific visual elements referenced in the text.

**Why this priority**: Multimodal input enhances accuracy and relevance but is an enhancement over the core single-input flows.

**Independent Test**: Can be fully tested by submitting a combined text + image input and verifying the response addresses both modalities coherently.

**Acceptance Scenarios**:

1. **Given** a user has opened the chat interface, **When** they upload an image and add a text question about it, **Then** the system processes both inputs together and generates a teaching response that references specific visual elements from the image in context of the text question

---

### Edge Cases

- What happens when the uploaded image is unclear, blurry, or contains no recognizable mathematical content?
- How does the system handle cases where OCR fallback produces inaccurate or incomplete math content extraction?
- How does the system handle mathematical subjects not covered in the `markdown_output` examples? (Should extrapolate using analogous NHM pedagogical patterns)
- What happens when the LM Studio API is unavailable or returns an error?
- How does the system handle very long conversation threads without losing pedagogical context?
- What happens when a user returns to the application after their session has expired?
- What happens when a user submits input in a language other than the expected teaching language (Traditional Chinese / English)?
- What happens when the streaming response is interrupted (network drop, page navigation) mid-generation?
- What happens when the LaTeX rendering engine fails to load or cannot parse a mathematical expression?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a web-based chat interface accessible via standard web browsers
- **FR-002**: System MUST accept text input through a chat text box
- **FR-003**: System MUST accept image uploads through a dedicated upload button
- **FR-004**: System MUST accept combined text + image input in a single message
- **FR-005**: System MUST identify the mathematical subject or concept from user input (text, image, or both)
- **FR-006**: System MUST apply the NHM pedagogical framework (as defined in "YouTube Math Pedagogy Instructional Blueprint.md") when generating teaching responses
- **FR-007**: System MUST reference relevant examples from the `markdown_output` directory when generating teaching content for known subjects
- **FR-008**: System MUST generate step-by-step teaching responses that include intuitive anchoring, metaphorical mapping, and procedural guidance following the slow-fast-slow rhythm
- **FR-009**: System MUST support conversational context — maintaining teaching continuity across multiple exchanges within a session
- **FR-010**: System MUST persist active conversations in browser local storage and restore them on page refresh, with sessions expiring after 30 minutes of inactivity
- **FR-011**: System MUST integrate with a local LLM API for generating teaching responses
- **FR-012**: System MUST generate different response types based on user intent: step-by-step solutions, syllabi, teaching methods, concept elaboration
- **FR-013**: System MUST detect whether the loaded LLM supports vision input and route images accordingly
- **FR-014**: System MUST fall back to OCR-based text extraction when the LLM does not support vision, sending extracted math content as text to the LLM
- **FR-015**: System MUST display conversation history in a scrollable chat format with clear visual distinction between user messages and system responses
- **FR-016**: System MUST provide user-friendly error messages when the LLM API is unavailable or returns errors
- **FR-017**: System MUST serve both student and teacher user roles without requiring authentication; role is inferred from input content by default
- **FR-018**: System MUST provide an optional role selector (Student/Teacher toggle) in the chat interface; when explicitly set, it overrides implicit role detection
- **FR-019**: System MUST stream teaching responses progressively, displaying content as it is generated with a typing indicator during generation
- **FR-020**: System MUST display a loading indicator between user message submission and the start of the first streamed response
- **FR-021**: System MUST render mathematical notation using LaTeX syntax with a formatted plain-text fallback when rendering fails

### Key Entities

- **Conversation Session**: A continuous interaction between a user and the system, containing a sequence of messages (user inputs and system responses)
- **User Message**: Input from the user, containing text content, optional image attachments, and metadata (timestamp, message type)
- **System Response**: Teaching output generated by the system, containing pedagogically structured content (intuition building, metaphorical explanation, step-by-step guidance, Gan-Jue checks)
- **Mathematical Subject**: The identified topic or concept from user input (e.g., logarithms, geometry, calculus), used to select appropriate pedagogical strategies and reference examples
- **Pedagogical Context**: The accumulated teaching state within a conversation, including the current subject, teaching phase (slow foundation / fast derivation / slow reflection), and student "feeling" state

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Streaming of teaching responses begins within 1 minute of submission; complete pedagogically structured response finishes within 5 minutes under normal operating conditions
- **SC-002**: 90% of teaching responses include at least one metaphorical mapping or intuitive anchor as defined in the NHM Blueprint
- **SC-003**: Users can successfully complete a follow-up question exchange within an active conversation session without losing context
- **SC-004**: Image upload and processing succeeds for clear, legible math problems in 95% of attempts
- **SC-005**: The chat interface loads and is ready for interaction within 3 seconds on a standard broadband connection
- **SC-006**: Users rate teaching response quality as "helpful" or better in 80% of interactions (measured via optional feedback mechanism)

## Assumptions

- LM Studio is running locally at `http://127.0.0.1:1234` and the `/api/v1/chat` endpoint is available when the application is in use
- The `markdown_output` directory and "YouTube Math Pedagogy Instructional Blueprint.md" are accessible to the application at runtime
- The LLM model loaded in LM Studio has sufficient mathematical reasoning capability to identify subjects and generate teaching content
- The LLM model may or may not support vision input; the system must handle both cases
- An OCR engine is available locally for fallback image-to-text extraction when the LLM lacks vision capability
- Users have a modern web browser with JavaScript enabled
- Image uploads are in common formats (PNG, JPEG, WebP) and under 10MB in size
- The application runs on a local or LAN network; external internet access is not required beyond the initial page load
- Teaching content is generated in Traditional Chinese and/or English, matching the language of the user's input
- The LLM outputs mathematical expressions in LaTeX format for proper rendering
- No user authentication or account system is required for the initial version — the application is open-access
