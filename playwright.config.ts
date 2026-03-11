import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.ts',
  timeout: 60000,
  retries: 1,
  projects: [
    {
      name: 'Chromium',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: 'http://localhost:3000',
      },
    },
  ],
  use: {
    baseURL: 'http://localhost:3001',
    screenshot: 'only-on-failure',
  },
});
