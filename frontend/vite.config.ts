import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

/// <reference types="vitest/config" />

export default defineConfig({
  plugins: [react()],
  test: {
    exclude: ["tests/e2e/**", "node_modules/**"],
    environment: "jsdom",
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ["react", "react-dom"],
          katex: ["katex"],
        },
      },
    },
    target: "esnext",
    minify: "terser",
  },
  server: {
    port: 5173,
    hmr: {
      overlay: false,
    },
    watch: {
      ignored: ["**/resource/**", "**/backend/**", "**/*.md"],
    },
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
        timeout: 0,
        proxyTimeout: 0,
        configure: (proxy, _options) => {
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            proxyReq.setTimeout(0);
            req.socket.setTimeout(0);
            req.socket.setNoDelay(true);
          });
          proxy.on("proxyRes", (proxyRes, _req, res) => {
            res.setHeader("Cache-Control", "no-cache");
            res.setHeader("Connection", "keep-alive");
            res.setHeader("X-Accel-Buffering", "no");
            res.setTimeout(0);
            if (
              proxyRes.headers["content-type"] &&
              proxyRes.headers["content-type"].includes("text/event-stream")
            ) {
              res.setHeader("Content-Type", proxyRes.headers["content-type"]);
              res.flushHeaders();
            }
          });
          proxy.on("error", (_err, _req, res) => {
            res.writeHead(500, { "Content-Type": "application/json" });
            res.end(
              JSON.stringify({
                error: { code: "PROXY_ERROR", message: "代理错误" },
              })
            );
          });
        },
      },
    },
  },
});
