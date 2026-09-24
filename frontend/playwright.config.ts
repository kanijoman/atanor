import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:5173",
    trace: "on-first-retry",
  },
  webServer: [
    {
      command: "pnpm dev --host 127.0.0.1 --port 5173",
      url: "http://127.0.0.1:5173",
      name: "frontend",
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "cd ../backend && uv run python scripts/run_e2e_server.py",
      url: "http://127.0.0.1:8000/health",
      name: "backend",
      timeout: 120_000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});
