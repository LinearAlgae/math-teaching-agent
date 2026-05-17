import { describe, it, expect, vi, afterEach } from "vitest";
import { cleanup, render } from "@testing-library/react";

vi.mock("katex", () => ({
  default: { renderToString: (tex: string) => `<span>${tex}</span>` },
}));

import { LaTeXRenderer } from "../../src/components/LaTeXRenderer";

afterEach(cleanup);

describe("LaTeXRenderer", () => {
  it("renders plain text", () => {
    const { container } = render(<LaTeXRenderer content="Hello world" />);
    expect(container.querySelector(".latex-content")).toBeTruthy();
  });

  it("renders with LaTeX math", () => {
    const { container } = render(<LaTeXRenderer content="E = $mc^2$" />);
    expect(container.querySelector(".latex-content")).toBeTruthy();
  });
});
