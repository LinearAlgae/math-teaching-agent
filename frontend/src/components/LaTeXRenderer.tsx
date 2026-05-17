import { useEffect, useRef, useState } from "react";
import { marked } from "marked";
import katex from "katex";

interface LaTeXRendererProps {
  content: string;
}

interface ParseResult {
  html: string;
  hasErrors: boolean;
  failedExpressions: string[];
}

function renderLatexWithFallback(text: string): ParseResult {
  const failedExpressions: string[] = [];
  let hasErrors = false;

  const rendered = text.replace(/(\$\$[\s\S]*?\$\$)|(\$[^$]+\$)/g, (_match, blockMath, inlineMath) => {
    const tex = blockMath ? blockMath.slice(2, -2) : inlineMath.slice(1, -1);
    const isBlock = !!blockMath;
    try {
      return katex.renderToString(tex, {
        throwOnError: true,
        displayMode: isBlock,
        output: "html",
        strict: false,
      });
    } catch (err) {
      hasErrors = true;
      failedExpressions.push(tex);
      return `<span class="latex-fallback" title="LaTeX解析错误：${tex}">${tex}</span>`;
    }
  });

  return { html: rendered, hasErrors, failedExpressions };
}

export function LaTeXRenderer({ content }: LaTeXRendererProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [hasParseErrors, setHasParseErrors] = useState(false);

  useEffect(() => {
    if (!containerRef.current) return;

    const placeholderMap = new Map<string, string>();
    let placeholderIdx = 0;

    const extractLatex = (text: string): string => {
      return text.replace(/(\$\$[\s\S]*?\$\$)|(\$[^$]+\$)/g, (match) => {
        const key = `LATEX_PLACEHOLDER_${placeholderIdx++}_`;
        placeholderMap.set(key, match);
        return key;
      });
    };

    const textWithoutLatex = extractLatex(content);
    const markdownHtml = marked.parse(textWithoutLatex, { async: false }) as string;

    const withLatex = markdownHtml.replace(/LATEX_PLACEHOLDER_\d+_/g, (match) => {
      const original = placeholderMap.get(match);
      if (!original) return match;
      const result = renderLatexWithFallback(original);
      if (result.hasErrors) setHasParseErrors(true);
      return result.html;
    });

    containerRef.current.innerHTML = withLatex;
  }, [content]);

  return (
    <div className="latex-content">
      <div ref={containerRef} />
      {hasParseErrors && (
        <div className="latex-parse-warning">
          部分公式无法渲染，已显示为纯文本。
        </div>
      )}
    </div>
  );
}
