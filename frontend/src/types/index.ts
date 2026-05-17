export type MessageRole = "student" | "teacher" | "auto";

export interface ImageAttachment {
  id: string;
  filename: string;
  mimeType: string;
  sizeBytes: number;
  data: string;
  extractedText?: string;
}

export interface UserMessage {
  id: string;
  timestamp: string;
  text: string;
  images: ImageAttachment[];
  role: MessageRole;
}

export type ResponseStatus = "streaming" | "complete" | "error";

export type PedagogyPhase = "slow-foundation" | "fast-derivation" | "slow-reflection";

export interface SystemResponse {
  id: string;
  timestamp: string;
  completedAt?: string;
  content: string;
  status: ResponseStatus;
  errorMessage?: string;
  pedagogyPhase?: PedagogyPhase;
}

export type ChatMessage = UserMessage | SystemResponse;

export interface ConversationSession {
  id: string;
  createdAt: string;
  lastActivityAt: string;
  role: MessageRole;
  expired: boolean;
  subject?: string;
  messages: ChatMessage[];
}