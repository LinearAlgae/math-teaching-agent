# API Contract: Chat Endpoints

**Date**: 2026-05-16
**Feature**: 001-math-teaching-chat

## POST /api/chat

Send a message (text, image, or both) and receive a streamed teaching response.

### Request

**Content-Type**: `multipart/form-data` (for image support) or `application/json` (text-only)

**Body** (multipart/form-data):

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| text | string | No | User's text input (required if no images) |
| images | file[] | No | Uploaded image files (PNG, JPEG, WebP, max 10MB each) |
| role | string | No | "student", "teacher", or "auto" (default: "auto") |
| sessionId | string | No | Existing session ID to continue conversation |

**Body** (application/json, text-only):

```json
{
  "text": "How do I solve log_2(8)?",
  "role": "student",
  "sessionId": "optional-existing-session-id"
}
```

### Response

**Content-Type**: `text/event-stream` (SSE)

**Stream events**:

```
event: start
data: {"sessionId": "uuid", "responseId": "uuid", "subject": "logarithms"}

event: token
data: {"content": "Let's start by thinking about what a logarithm means..."}

event: token
data: {"content": "Imagine you have a number line..."}

event: complete
data: {"responseId": "uuid", "fullContent": "...", "pedagogyPhase": "slow-reflection"}

event: error
data: {"message": "LM Studio API unavailable", "code": "LLM_UNAVAILABLE"}
```

### Error Responses

| Status Code | Error Code | Description |
|-------------|------------|-------------|
| 400 | INVALID_INPUT | No text or images provided |
| 400 | IMAGE_TOO_LARGE | Image exceeds 10MB limit |
| 400 | UNSUPPORTED_FORMAT | Image format not PNG/JPEG/WebP |
| 413 | PAYLOAD_TOO_LARGE | Total payload exceeds server limit |
| 502 | LLM_UNAVAILABLE | LM Studio API not responding |
| 500 | INTERNAL_ERROR | Unexpected server error |

## GET /api/session/{sessionId}

Retrieve an existing conversation session.

### Response

**Content-Type**: `application/json`

```json
{
  "id": "uuid",
  "createdAt": "2026-05-16T10:30:00Z",
  "lastActivityAt": "2026-05-16T10:45:00Z",
  "role": "student",
  "expired": false,
  "subject": "logarithms",
  "messages": [
    {
      "type": "user",
      "id": "uuid",
      "timestamp": "2026-05-16T10:30:00Z",
      "text": "How do I solve log_2(8)?",
      "images": []
    },
    {
      "type": "system",
      "id": "uuid",
      "timestamp": "2026-05-16T10:30:05Z",
      "completedAt": "2026-05-16T10:30:30Z",
      "content": "...",
      "status": "complete"
    }
  ]
}
```

## GET /api/health

Check backend health and LLM connectivity.

### Response

**Content-Type**: `application/json`

```json
{
  "status": "healthy",
  "llmConnected": true,
  "llmModel": "llama-3-8b-instruct",
  "llmVisionSupported": false,
  "timestamp": "2026-05-16T10:00:00Z"
}
```

## POST /api/vision/detect

Detect whether the currently loaded LLM model supports vision input.

### Response

**Content-Type**: `application/json`

```json
{
  "visionSupported": true,
  "detectionMethod": "metadata",
  "modelName": "llava-1.5-7b"
}
```
