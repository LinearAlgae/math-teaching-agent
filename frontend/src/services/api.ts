import { MessageRole } from "../types";

const API_BASE = "/api";
const MAX_IMAGE_SIZE = 10 * 1024 * 1024; // 10MB
const ACCEPTED_MIME_TYPES = ["image/png", "image/jpeg", "image/webp"];

export interface ImageValidationResult {
  valid: boolean;
  error?: string;
}

export function validateImage(file: File): ImageValidationResult {
  if (!ACCEPTED_MIME_TYPES.includes(file.type)) {
    return { valid: false, error: `不支持的格式：${file.type}。请使用PNG、JPG或WebP格式。` };
  }
  if (file.size > MAX_IMAGE_SIZE) {
    return { valid: false, error: `文件过大：${(file.size / (1024 * 1024)).toFixed(1)}MB（最大10MB）` };
  }
  return { valid: true };
}

export async function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => {
      const result = reader.result as string;
      const base64 = result.split(",")[1];
      resolve(base64);
    };
    reader.onerror = reject;
    reader.readAsDataURL(file);
  });
}

export async function sendChatMessage(
  text: string,
  role: MessageRole = "auto",
  sessionId?: string,
  images?: File[]
): Promise<ReadableStreamDefaultReader<Uint8Array>> {
  const formData = new FormData();
  formData.append("text", text);
  formData.append("role", role);
  if (sessionId) {
    formData.append("sessionId", sessionId);
  }
  if (images) {
    for (const img of images) {
      const validation = validateImage(img);
      if (!validation.valid) {
        throw new Error(validation.error);
      }
      formData.append("files", img);
    }
  }

  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.error?.message || "发送消息失败");
  }

  if (!response.body) {
    throw new Error("无响应内容");
  }

  return response.body.getReader();
}

export async function fetchSession(sessionId: string) {
  const response = await fetch(`${API_BASE}/session/${sessionId}`);
  if (!response.ok) {
    throw new Error("会话未找到");
  }
  return response.json();
}

export async function checkVisionSupport() {
  const response = await fetch(`${API_BASE}/vision/detect`);
  return response.json();
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`);
  return response.json();
}
