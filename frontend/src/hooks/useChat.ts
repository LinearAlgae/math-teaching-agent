import { useState } from "react";

interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  reasoning?: string;
  status?: "streaming" | "complete" | "error";
}

interface UseChatReturn {
  messages: Message[];
  isLoading: boolean;
  sendMessage: (text: string, images?: File[], role?: string, sessionId?: string) => Promise<void>;
  clearMessages: () => void;
}

const STREAM_TIMEOUT_MS = 1800000; // 30 minutes total

export function useChat(initialMessages: Message[] = []): UseChatReturn {
  const [messages, setMessages] = useState<Message[]>(initialMessages);
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async (text: string, images?: File[], role: string = "auto", sessionId?: string) => {
    if (!text.trim() && !images?.length) return;

    const userMsg: Message = {
      id: Date.now().toString(),
      role: "user",
      content: text,
    };
    setMessages((prev) => [...prev, userMsg]);
    setIsLoading(true);

    const assistantMsgId = (Date.now() + 1).toString();
    const assistantMsg: Message = {
      id: assistantMsgId,
      role: "assistant",
      content: "",
      status: "streaming",
    };
    setMessages((prev) => [...prev, assistantMsg]);

    let assistantContent = "";
    let assistantReasoning = "";
    let streamDone = false;
    let currentEvent = "";

    const processStream = async (signal: AbortSignal): Promise<void> => {
      const formData = new FormData();
      formData.append("text", text);
      formData.append("role", role);
      if (sessionId) {
        formData.append("sessionId", sessionId);
      }
      if (images?.length) {
        for (const img of images) {
          formData.append("files", img);
        }
      }

      const response = await fetch("/api/chat", {
        method: "POST",
        body: formData,
        signal,
      });

      if (!response.ok) {
        const text = await response.text().catch(() => "");
        throw new Error(`服务器错误 (${response.status}): ${text.slice(0, 200)}`);
      }
      if (!response.body) throw new Error("No response body");

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = "";

      const updateMessage = () => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  content: assistantContent,
                  reasoning: assistantReasoning,
                  status: "streaming",
                }
              : m
          )
        );
      };

      // eslint-disable-next-line no-constant-condition
      while (true) {
        if (signal.aborted) return;

        const { done, value } = await reader.read();
        if (done) {
          streamDone = true;
          return;
        }

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split("\n");
        buffer = lines.pop() || "";

        for (const line of lines) {
          if (line.startsWith("event: ")) {
            currentEvent = line.slice(7).trim();
          } else if (line.startsWith("data: ")) {
            const data = line.slice(6);
            if (data === "[DONE]") {
              streamDone = true;
              return;
            }
            try {
              const parsed = JSON.parse(data);
              if (currentEvent === "reasoning" && parsed.content) {
                assistantReasoning += parsed.content;
                updateMessage();
              } else if (currentEvent === "token" && parsed.content) {
                assistantContent += parsed.content;
                updateMessage();
              } else if (currentEvent === "complete") {
                assistantContent = parsed.fullContent || assistantContent;
                assistantReasoning = parsed.reasoning || assistantReasoning;
                streamDone = true;
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          content: assistantContent,
                          reasoning: assistantReasoning,
                          status: "complete",
                        }
                      : m
                  )
                );
                return;
              } else if (currentEvent === "error" || parsed.error) {
                setMessages((prev) =>
                  prev.map((m) =>
                    m.id === assistantMsgId
                      ? {
                          ...m,
                          content: parsed.message || assistantContent || "流中断",
                          reasoning: assistantReasoning,
                          status: "error",
                        }
                      : m
                  )
                );
                streamDone = true;
                return;
              }
            } catch {
              // Skip malformed JSON
            }
          }
        }
      }
    };

    const controller = new AbortController();
    const timeoutId = setTimeout(() => {
      controller.abort();
    }, STREAM_TIMEOUT_MS);

    try {
      await processStream(controller.signal);

      if (!streamDone) {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === assistantMsgId && m.status === "streaming"
              ? { ...m, content: assistantContent, reasoning: assistantReasoning, status: "complete" }
              : m
          )
        );
      }
    } catch (error) {
      console.error("Chat stream error:", error);
      const errorMsg =
        assistantContent ||
        ((error as Error).name === "AbortError"
          ? "请求超时"
          : (error as Error).message?.includes("服务器错误")
            ? (error as Error).message
            : "出现了问题，请重试。");

      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantMsgId
            ? { ...m, content: errorMsg, reasoning: assistantReasoning, status: "error" }
            : m
        )
      );
    } finally {
      clearTimeout(timeoutId);
      setIsLoading(false);
    }
  };

  const clearMessages = () => setMessages([]);

  return { messages, isLoading, sendMessage, clearMessages };
}
