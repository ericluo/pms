import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  testIgnore: ['**/frontend/**', '**/*.unit.ts', '**/*.test.ts'],
  timeout: 60000,
  retries: 1,
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: 'http://localhost:3000',
      },
    },
    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        baseURL: 'http://localhost:3000',
      },
    },
    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        baseURL: 'http://localhost:3000',
      },
    },
    {
      name: 'Edge',
      use: {
        ...devices['Desktop Chrome'],
        baseURL: 'http://localhost:3000',
      },
    },
    {
      name: 'Tabbit',
      use: {
        launchOptions: {
          executablePath: 'C:\\Users\\Administrator\\AppData\\Local\\Tabbit Browser\\Application\\Tabbit Browser.exe',
        },
        baseURL: 'http://localhost:3000',
      },
    },
  ],
  use: {
    baseURL: 'http://localhost:3000',
    screenshot: 'only-on-failure',
  },
});
