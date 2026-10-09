// Regressione visiva. Baseline = versione APPROVATA (generata con --update-snapshots dopo revisione umana).
// Esecuzione:  npx playwright test -c tests/visual/playwright.visual.config.js
// Aggiorna baseline (solo dopo aver guardato gli screenshot):  ... --update-snapshots
const { defineConfig } = require('@playwright/test');
const path = require('path');
const PORT = Number(process.env.E2E_PORT || 4173);

module.exports = defineConfig({
  testDir: __dirname,
  testMatch: /.*\.visual\.js/,
  timeout: 60000,
  expect: { timeout: 8000, toHaveScreenshot: { maxDiffPixelRatio: 0.015, animations: 'disabled', caret: 'hide' } },
  snapshotPathTemplate: '{testDir}/baseline/{arg}-{projectName}{ext}',
  reporter: [['list']],
  use: { baseURL: `http://localhost:${PORT}`, locale: 'it-IT', timezoneId: 'Europe/Rome', trace: 'off' },
  webServer: {
    command: 'node tests/e2e/static-server.js',
    url: `http://localhost:${PORT}/proprietario-immobile`,
    cwd: path.resolve(__dirname, '..', '..'),
    reuseExistingServer: true,
    timeout: 20000,
  },
  projects: [
    { name: 'desktop-1440', use: { viewport: { width: 1440, height: 900 } } },
    { name: 'laptop-1366', use: { viewport: { width: 1366, height: 768 } } },
    { name: 'tablet-768', use: { viewport: { width: 768, height: 1024 }, hasTouch: true } },
    { name: 'phone-390', use: { viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true } },
    { name: 'phone-360', use: { viewport: { width: 360, height: 800 }, isMobile: true, hasTouch: true } },
  ],
});
