import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { renderHook, act } from "@testing-library/react";
import { useSession } from "../../src/hooks/useSession";

const STORAGE_KEY = "math-teaching-session";
const SESSION_TIMEOUT_MS = 30 * 60 * 1000;

const mockSession = {
  id: "test-session-123",
  createdAt: new Date().toISOString(),
  lastActivityAt: new Date().toISOString(),
  role: "student" as const,
  expired: false,
  messages: [],
};

describe("useSession", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it("returns null when no session stored", () => {
    const { result } = renderHook(() => useSession());
    expect(result.current.session).toBeNull();
    expect(result.current.isLoading).toBe(false);
  });

  it("loads session from localStorage", () => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(mockSession));
    const { result } = renderHook(() => useSession());
    expect(result.current.session).not.toBeNull();
    expect(result.current.session?.id).toBe("test-session-123");
  });

  it("detects expired session", () => {
    const expiredSession = {
      ...mockSession,
      lastActivityAt: new Date(Date.now() - SESSION_TIMEOUT_MS - 1000).toISOString(),
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(expiredSession));
    const { result } = renderHook(() => useSession());
    expect(result.current.isExpired).toBe(true);
    expect(result.current.session).toBeNull();
  });

  it("saves session to localStorage", () => {
    const { result } = renderHook(() => useSession());
    act(() => {
      result.current.saveSession(mockSession);
    });
    const stored = localStorage.getItem(STORAGE_KEY);
    expect(stored).not.toBeNull();
    const parsed = JSON.parse(stored!);
    expect(parsed.id).toBe("test-session-123");
  });

  it("updates lastActivityAt on save", () => {
    const { result } = renderHook(() => useSession());
    const beforeSave = Date.now();
    act(() => {
      result.current.saveSession(mockSession);
    });
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY)!);
    expect(new Date(stored.lastActivityAt).getTime()).toBeGreaterThanOrEqual(beforeSave);
  });

  it("clears session and removes from localStorage", () => {
    const { result } = renderHook(() => useSession());
    act(() => {
      result.current.saveSession(mockSession);
    });
    act(() => {
      result.current.clearSession();
    });
    expect(result.current.session).toBeNull();
    expect(result.current.isExpired).toBe(false);
    expect(localStorage.getItem(STORAGE_KEY)).toBeNull();
  });

  it("handles corrupted localStorage data gracefully", () => {
    localStorage.setItem(STORAGE_KEY, "not-valid-json");
    const { result } = renderHook(() => useSession());
    expect(result.current.session).toBeNull();
    expect(result.current.isLoading).toBe(false);
  });

  it("handles empty localStorage", () => {
    localStorage.removeItem(STORAGE_KEY);
    const { result } = renderHook(() => useSession());
    expect(result.current.session).toBeNull();
    expect(result.current.isExpired).toBe(false);
  });
});
