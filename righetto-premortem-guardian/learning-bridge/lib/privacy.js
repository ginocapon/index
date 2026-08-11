import crypto from 'node:crypto';

export function hashSession(sessionId, salt = 'linda-lb-v1') {
  if (!sessionId) return null;
  return crypto.createHash('sha256').update(`${salt}:${sessionId}`).digest('hex').slice(0, 24);
}

export function hashMessage(text) {
  if (!text || typeof text !== 'string') return null;
  const norm = text.toLowerCase().trim().replace(/\s+/g, ' ');
  return crypto.createHash('sha256').update(norm).digest('hex').slice(0, 16);
}

export function stripPii(obj) {
  if (!obj || typeof obj !== 'object') return obj;
  const forbidden = ['nome', 'email', 'telefono', 'phone', 'name', 'messaggio', 'note'];
  const out = { ...obj };
  for (const key of forbidden) delete out[key];
  return out;
}
