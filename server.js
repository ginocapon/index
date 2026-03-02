const express = require('express');
const compression = require('compression');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 8080;

// Gzip/Brotli compression — riduce HTML, CSS, JS, JSON del 60-80%
app.use(compression());

// Asset statici con cache differenziata
app.use(express.static(path.join(__dirname), {
  setHeaders(res, filePath) {
    const ext = path.extname(filePath).toLowerCase();

    // Font, immagini, WebP — cache lunga (1 anno, immutable)
    if (['.woff2','.woff','.webp','.jpg','.jpeg','.png','.svg','.ico'].includes(ext)) {
      res.setHeader('Cache-Control', 'public, max-age=31536000, immutable');
      return;
    }

    // CSS e JS — cache media (1 settimana)
    if (['.css','.js'].includes(ext)) {
      res.setHeader('Cache-Control', 'public, max-age=604800, stale-while-revalidate=86400');
      return;
    }

    // HTML — sempre fresco (rivalidazione)
    if (ext === '.html' || ext === '') {
      res.setHeader('Cache-Control', 'public, max-age=0, must-revalidate');
    }
  }
}));

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
