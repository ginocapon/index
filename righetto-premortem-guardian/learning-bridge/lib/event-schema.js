/**
 * Schema eventi normalizzati — LINDA Learning Bridge
 * Nessun dato personale nei payload di learning.
 */

export const EVENT_TYPES = Object.freeze([
  'search_started',
  'property_results_shown',
  'property_clicked',
  'property_ignored',
  'property_saved',
  'visit_requested',
  'lead_created',
  'search_no_result',
  'question_unanswered',
  'user_correction',
  'conversation_abandoned',
  'conversation_completed',
  'stima_completed',
  'faq_matched'
]);

export function normalizeEvent(raw) {
  const type = String(raw.event_type || raw.type || '').trim();
  if (!EVENT_TYPES.includes(type)) return null;

  const payload = raw.payload && typeof raw.payload === 'object' ? raw.payload : {};
  const criteria = payload.criteria && typeof payload.criteria === 'object' ? payload.criteria : {};

  return {
    event_type: type,
    session_id: raw.session_id || null,
    search_id: raw.search_id || payload.search_id || null,
    page_path: raw.page_path || payload.page_path || null,
    source: raw.source || payload.source || 'linda_chatbot',
    payload: {
      criteria: sanitizeCriteria(criteria),
      property_ids: Array.isArray(payload.property_ids) ? payload.property_ids.slice(0, 20) : [],
      property_id: payload.property_id || null,
      property_slug: payload.property_slug || null,
      position: typeof payload.position === 'number' ? payload.position : null,
      result_count: typeof payload.result_count === 'number' ? payload.result_count : null,
      intent: payload.intent || null,
      faq_key: payload.faq_key || null,
      user_message_hash: payload.user_message_hash || null,
      ranking_version: payload.ranking_version || 'baseline_v1',
      meta: payload.meta && typeof payload.meta === 'object' ? payload.meta : {}
    }
  };
}

export function sanitizeCriteria(criteria) {
  const out = {};
  const allowed = [
    'tipo_operazione', 'zona', 'comune', 'tipologia', 'budget_min', 'budget_max',
    'camere', 'garage', 'giardino', 'terrazzo', 'mq_min', 'mq_max', 'hard_constraints',
    'soft_preferences'
  ];
  for (const key of allowed) {
    if (criteria[key] !== undefined && criteria[key] !== null && criteria[key] !== '') {
      out[key] = criteria[key];
    }
  }
  return out;
}
