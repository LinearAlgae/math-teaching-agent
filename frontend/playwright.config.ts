import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  timeout: 120000,
  reporter: "line",
  use: {
    baseURL: "http://localhost:5173",
    trace: "on-first-retry",
    actionTimeout: 60000,
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
  ],
  webServer: [
    {
      command: "bash -c 'cd ../backend && . .venv/bin/activate && python -m uvicorn src.main:app --host 127.0.0.1 --port 8000'",
      url: "http://127.0.0.1:8000/api/health",
      reuseExistingServer: true,
    },
    {
      command: "npm run dev",
      url: "http://localhost:5173",
      reuseExistingServer: true,
    },
  ],
});
