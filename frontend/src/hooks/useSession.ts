import { useState, useEffect, useCallback } from "react";
import { ConversationSession } from "../types";

const STORAGE_KEY = "math-teaching-session";
const SESSION_TIMEOUT_MS = 30 * 60 * 1000; // 30 minutes

interface UseSessionReturn {
  session: ConversationSession | null;
  isLoading: boolean;
  saveSession: (session: ConversationSession) => void;
  clearSession: () => void;
  isExpired: boolean;
}

export function useSession(): UseSessionReturn {
  const [session, setSession] = useState<ConversationSession | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isExpired, setIsExpired] = useState(false);

  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored);
        const lastActivity = new Date(parsed.lastActivityAt).getTime();
        const now = Date.now();
        if (now - lastActivity > SESSION_TIMEOUT_MS) {
          setIsExpired(true);
          localStorage.removeItem(STORAGE_KEY);
        } else {
          setSession(parsed);
        }
      }
    } catch (e) {
      console.error("Failed to load session:", e);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const saveSession = useCallback((newSession: ConversationSession) => {
    const updated = {
      ...newSession,
      lastActivityAt: new Date().toISOString(),
    };
    setSession(updated);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
  }, []);

  const clearSession = useCallback(() => {
    setSession(null);
    setIsExpired(false);
    localStorage.removeItem(STORAGE_KEY);
  }, []);

  return { session, isLoading, saveSession, clearSession, isExpired };
}