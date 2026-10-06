import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    exclude: ["e2e/**", "node_modules/**", "dist/**"],
  },
  server: {
    port: 5174,
    strictPort: true,
    proxy: {
      "/api": `http://127.0.0.1:${process.env.E2E_BACKEND_PORT ?? "8000"}`,
    },
  },
});
