// Test e2e Righetto. Esecuzione: npm run test:e2e
// Nessuna richiesta reale: Supabase, email e analytics sono simulati in helpers.js.
const { defineConfig } = require('@playwright/test');

const PORT = Number(process.env.E2E_PORT || 4173);

module.exports = defineConfig({
  testDir: __dirname,
  testMatch: /.*\.spec\.js/,
  timeout: 45000,
  expect: { timeout: 8000 },
  retries: 0,
  reporter: [['list']],
  use: { baseURL: `http://localhost:${PORT}`, locale: 'it-IT', trace: 'off' },
  webServer: {
    command: 'node tests/e2e/static-server.js',
    url: `http://localhost:${PORT}/proprietario-immobile`,
    cwd: require('path').resolve(__dirname, '..', '..'),
    reuseExistingServer: true,
    timeout: 20000,
  },
  projects: [
    { name: 'mobile', use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true, deviceScaleFactor: 2 } },
    { name: 'desktop', use: { viewport: { width: 1440, height: 900 } } },
  ],
});
