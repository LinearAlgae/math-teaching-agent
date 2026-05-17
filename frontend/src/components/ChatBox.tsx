import { useState, useEffect, useRef } from "react";
import { useChat } from "../hooks/useChat";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { LoadingSpinner } from "./LoadingSpinner";
import { ImageUpload } from "./ImageUpload";
import { RoleSelector } from "./RoleSelector";
import { MessageRole } from "../types";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
  reasoning?: string;
  status?: string;
}

interface ChatBoxProps {
  sessionId?: string;
  initialMessages?: ChatMessage[];
  onSessionUpdate?: (session: { id: string; messages: unknown[]; lastActivityAt: string }) => void;
}

export function ChatBox({ sessionId, initialMessages, onSessionUpdate }: ChatBoxProps) {
  const { messages, isLoading, sendMessage } = useChat(initialMessages || []);
  const [input, setInput] = useState("");
  const [images, setImages] = useState<File[]>([]);
  const [role, setRole] = useState<MessageRole>("student");
  const onSessionUpdateRef = useRef(onSessionUpdate);
  useEffect(() => {
    onSessionUpdateRef.current = onSessionUpdate;
  });

  useEffect(() => {
    if (onSessionUpdateRef.current && messages.length > 0) {
      onSessionUpdateRef.current({
        id: sessionId || "new",
        messages: messages as unknown[],
        lastActivityAt: new Date().toISOString(),
      });
    }
  }, [messages, sessionId]);

  const handleSend = async () => {
    if (!input.trim() && !images.length) return;
    const text = input;
    setInput("");
    setImages([]);
    await sendMessage(text, images.length > 0 ? images : undefined, role, sessionId);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-list">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isLoading && <TypingIndicator />}
      </div>
      <div className="input-container">
        <RoleSelector role={role} onRoleChange={setRole} />
        <ImageUpload onImagesChange={setImages} images={images} />
        <div className="input-wrapper">
          <textarea
            className="chat-input"
            placeholder={role === "teacher" ? "输入教学大纲或教案请求…" : "输入数学问题…"}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={1}
          />
        </div>
        <button
          className="send-button"
          onClick={handleSend}
          disabled={isLoading || (!input.trim() && !images.length)}
        >
          {isLoading ? <LoadingSpinner /> : "发送"}
        </button>
      </div>
    </div>
  );
}
