import { describe, it, expect, vi, afterEach } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";

vi.mock("katex", () => ({
  default: { renderToString: (tex: string) => `<span>${tex}</span>` },
}));

import { ChatBox } from "../../src/components/ChatBox";

afterEach(cleanup);

describe("ChatBox", () => {
  it("renders chat container", () => {
    const { container } = render(<ChatBox />);
    expect(container.querySelector(".chat-container")).toBeTruthy();
  });

  it("renders input elements", () => {
    render(<ChatBox />);
    expect(screen.getByPlaceholderText(/输入数学问题…/i)).toBeTruthy();
    expect(screen.getByText("发送")).toBeTruthy();
  });
});
