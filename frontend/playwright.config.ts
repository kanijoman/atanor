import { defineConfig } from "@playwright/test";

const backendPort = process.env.E2E_BACKEND_PORT ?? "8000";

export default defineConfig({
  testDir: "./e2e",
  timeout: 30_000,
  reporter: "list",
  use: {
    baseURL: "http://127.0.0.1:5174",
    trace: "on-first-retry",
  },
  webServer: [
    {
      command: "pnpm dev --host 127.0.0.1 --port 5174",
      url: "http://127.0.0.1:5174",
      name: "frontend",
      reuseExistingServer: !process.env.CI,
    },
    {
      command: "cd ../backend && uv run python scripts/run_e2e_server.py",
      url: `http://127.0.0.1:${backendPort}/health`,
      name: "backend",
      timeout: 120_000,
      reuseExistingServer: !process.env.CI,
    },
  ],
});
