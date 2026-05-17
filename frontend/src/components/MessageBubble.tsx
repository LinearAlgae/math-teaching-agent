import { useState } from "react";
import { LaTeXRenderer } from "./LaTeXRenderer";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  reasoning?: string;
  status?: "streaming" | "complete" | "error";
}

interface MessageBubbleProps {
  message: Message;
}

export function MessageBubble({ message }: MessageBubbleProps) {
  const [showReasoning, setShowReasoning] = useState(false);

  return (
    <div className={`message ${message.role}`}>
      <div className="message-content">
        {message.role === "assistant" && message.reasoning && (
          <div className="reasoning-section">
            <button
              className="reasoning-toggle"
              onClick={() => setShowReasoning(!showReasoning)}
            >
              <span className={`reasoning-arrow ${showReasoning ? "expanded" : ""}`}>&#9654;</span>
              <span>思考过程</span>
              <span className="reasoning-badge">AI</span>
            </button>
            {showReasoning && (
              <div className="reasoning-content">
                <LaTeXRenderer content={message.reasoning} />
              </div>
            )}
          </div>
        )}
        <LaTeXRenderer content={message.content} />
      </div>
    </div>
  );
}