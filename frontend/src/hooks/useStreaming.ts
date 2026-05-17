import { useState, useCallback, useRef } from "react";

interface UseStreamingReturn {
  content: string;
  isStreaming: boolean;
  hasError: boolean;
  errorMessage: string;
  processChunk: (chunk: string) => void;
  handleStreamError: (error: unknown) => void;
  reset: () => void;
  startStreaming: () => void;
  completeStreaming: () => void;
}

export function useStreaming(): UseStreamingReturn {
  const [content, setContent] = useState("");
  const [isStreaming, setIsStreaming] = useState(false);
  const [hasError, setHasError] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const savedContent = useRef("");

  const startStreaming = useCallback(() => {
    setIsStreaming(true);
    setHasError(false);
    setErrorMessage("");
    savedContent.current = "";
    setContent("");
  }, []);

  const completeStreaming = useCallback(() => {
    savedContent.current = content;
    setIsStreaming(false);
  }, [content]);

  const processChunk = useCallback((chunk: string) => {
    const lines = chunk.split("\n");
    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = line.slice(6);
        if (data === "[DONE]") {
          savedContent.current = content;
          setIsStreaming(false);
          return;
        }
        try {
          const parsed = JSON.parse(data);
          if (parsed.content) {
            savedContent.current += parsed.content;
            setContent((prev) => prev + parsed.content);
          }
          if (parsed.fullContent || parsed.complete) {
            savedContent.current = parsed.fullContent || savedContent.current;
            setIsStreaming(false);
          }
          if (parsed.error) {
            setHasError(true);
            setErrorMessage(parsed.message || "流中断");
            setIsStreaming(false);
          }
        } catch {
          // Skip malformed SSE data
        }
      }
    }
  }, [content]);

  const handleStreamError = useCallback((error: unknown) => {
    setIsStreaming(false);
    setHasError(true);
    const partialContent = savedContent.current;
    if (error instanceof Error) {
      if (error.message.includes("fetch") || error.message.includes("network")) {
        setErrorMessage("连接已断开，请重试。");
      } else if (error.name === "AbortError") {
        setErrorMessage("响应被中断，已保留部分内容。");
      } else {
        setErrorMessage("响应被中断，已保留部分内容。");
      }
    } else {
      setErrorMessage("响应被中断，已保留部分内容。");
    }
    if (partialContent) {
      setContent(partialContent);
    }
  }, []);

  const reset = useCallback(() => {
    setContent("");
    setIsStreaming(false);
    setHasError(false);
    setErrorMessage("");
    savedContent.current = "";
  }, []);

  return { content, isStreaming, hasError, errorMessage, processChunk, handleStreamError, reset, startStreaming, completeStreaming };
}
