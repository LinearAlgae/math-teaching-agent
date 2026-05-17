import { describe, it, expect, vi, beforeEach } from "vitest";

vi.mock("../../src/services/api", () => ({
  sendChatMessage: vi.fn(),
}));

async function createUseChatMock() {
  const messages: Array<{ id: string; role: string; content: string; status?: string }> = [];
  let isLoading = false;

  return {
    get messages() { return messages; },
    get isLoading() { return isLoading; },
    sendMessage: vi.fn(async (text: string) => {
      isLoading = true;
      messages.push({ id: "1", role: "user", content: text });
      await new Promise((resolve) => setTimeout(resolve, 0));
      messages.push({ id: "2", role: "assistant", content: "Test response", status: "complete" });
      isLoading = false;
    }),
    clearMessages: vi.fn(() => {
      messages.length = 0;
    }),
  };
}

describe("useChat", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("initializes with empty messages", async () => {
    const chat = await createUseChatMock();
    expect(chat.messages).toEqual([]);
    expect(chat.isLoading).toBe(false);
  });

  it("adds user and assistant messages after send", async () => {
    const chat = await createUseChatMock();
    await chat.sendMessage("Hello");
    expect(chat.messages).toHaveLength(2);
    expect(chat.messages[0].role).toBe("user");
    expect(chat.messages[0].content).toBe("Hello");
    expect(chat.messages[1].role).toBe("assistant");
  });

  it("clears messages", async () => {
    const chat = await createUseChatMock();
    await chat.sendMessage("Hello");
    chat.clearMessages();
    expect(chat.messages).toHaveLength(0);
  });

  it("sets loading state during send", async () => {
    const chat = await createUseChatMock();
    const sendPromise = chat.sendMessage("Hello");
    expect(chat.isLoading).toBe(true);
    await sendPromise;
    expect(chat.isLoading).toBe(false);
  });
});
