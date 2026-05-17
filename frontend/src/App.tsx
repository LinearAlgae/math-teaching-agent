import { useState, useCallback } from "react";
import { ChatBox } from "./components/ChatBox";
import { useSession } from "./hooks/useSession";
import { ConversationSession } from "./types";
import "./styles/theme.css";

export default function App() {
  const { session, isLoading, isExpired, clearSession, saveSession } = useSession();
  const [showExpired, setShowExpired] = useState(false);
  const [sessionKey, setSessionKey] = useState(0);

  const handleNewSession = useCallback(() => {
    clearSession();
    setSessionKey((k) => k + 1);
  }, [clearSession]);

  if (isLoading) {
    return (
      <div className="app-container">
        <div className="messages-list" style={{ alignItems: "center", justifyContent: "center" }}>
          <div className="loading-spinner" />
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="chat-header">
        <h1 className="chat-title">数学教学助手</h1>
        <button className="role-button" onClick={handleNewSession}>
          新对话
        </button>
      </header>
      {isExpired && !showExpired && (
        <div className="session-expired-banner">
          <p>上一会话已过期，请开始新对话。</p>
          <button onClick={() => setShowExpired(true)}>关闭</button>
        </div>
      )}
      <ChatBox
        key={sessionKey}
        sessionId={session?.id}
        initialMessages={session?.messages as { id: string; role: "user" | "assistant"; content: string; reasoning?: string; status?: string }[]}
        onSessionUpdate={(s) => {
          const fullSession: ConversationSession = {
            id: s.id,
            createdAt: session?.createdAt || new Date().toISOString(),
            lastActivityAt: s.lastActivityAt,
            role: session?.role || "student",
            expired: false,
            messages: s.messages as ConversationSession["messages"],
          };
          saveSession(fullSession);
        }}
      />
    </div>
  );
}
