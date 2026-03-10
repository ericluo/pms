import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  timeout: 60000,
  retries: 1,
  projects: [
    {
      name: 'Edge',
      use: {
        ...devices['Desktop Edge'],
        channel: 'msedge',
        baseURL: 'http://localhost:3000',
      },
    },
  ],
  use: {
    baseURL: 'http://localhost:3001',
    screenshot: 'only-on-failure',
  },
});
