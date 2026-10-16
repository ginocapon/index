/**
 * Lead scoring acquisizione proprietari — admin Richieste
 * Allineato a supabase/functions/score-lead-righetto + data/lead-scoring-rules.json
 */
(function (global) {
  const HOT = 70;
  const WARM = 40;

  let rulesCache = null;

  async function loadLeadScoringRules() {
    if (rulesCache) return rulesCache;
    try {
      const res = await fetch('/data/lead-scoring-rules.json?v=2');
      if (res.ok) rulesCache = await res.json();
    } catch (_) {
      rulesCache = null;
    }
    return rulesCache;
  }

  function scoreLeadRow(row) {
    const nome = String(row.nome ?? '');
    const tel = String(row.telefono ?? '').trim();
    const msg = String(row.messaggio ?? '');
    const prov = String(row.provenienza ?? '');
    const blob = `${msg} ${prov} ${row.tipo_immobile ?? ''} ${row.zona ?? ''}`.toLowerCase();

    let score = 15;
    if (tel.length >= 8) score += 10;
    if (/landing-valutazione|servizio-valutazioni|valutazione/.test(prov)) score += 20;
    if (/vend|incarico|mandato|valut/.test(blob)) score += 25;
    if (/urgent|subito|asap|3 mesi|tre mesi|6 mesi/.test(blob)) score += 15;
    if (/300\.?000|350\.?000|400\.?000|500\.?000|ville|centro storico|pregio/.test(blob)) score += 20;
    if (/non si vende|invendut|annuncio fermo|già in vendita|gia in vendita/.test(blob)) score += 15;
    if (/solo curios|tra qualche anno|non ho fretta/.test(blob)) score -= 10;
    if (!tel && row.email) score -= 5;

    score = Math.max(0, Math.min(100, score));
    const temperature = score >= HOT ? 'hot' : score >= WARM ? 'warm' : 'cold';

    let owner_path = null;
    if (/non si vende|invendut|già in vendita|annuncio fermo/.test(blob)) owner_path = 'F';
    else if (/quanto vale|valutazione|stima/.test(blob)) owner_path = 'A';
    else if (/pens.*vendere|voglio vendere/.test(blob)) owner_path = 'B';
    else if (/non so se|indecis/.test(blob)) owner_path = 'L';
    else if (/eredit|succession/.test(blob)) owner_path = 'H';
    else if (/ristruttur|lavori/.test(blob)) owner_path = 'J';

    return { score, temperature, owner_path, nome };
  }

  function effectiveLeadMeta(row) {
    const dbScore = row.lead_score != null && row.lead_score !== '' ? Number(row.lead_score) : null;
    const computed = scoreLeadRow(row);
    const score = dbScore != null && !Number.isNaN(dbScore) ? dbScore : computed.score;
    let temperature = row.lead_temperature || computed.temperature;
    if (dbScore != null && !row.lead_temperature) {
      temperature = score >= HOT ? 'hot' : score >= WARM ? 'warm' : 'cold';
    }
    const owner_path = row.owner_path || computed.owner_path;
    return { score, temperature, owner_path, computed_only: dbScore == null };
  }

  function temperatureLabel(temp) {
    if (temp === 'hot') return 'HOT';
    if (temp === 'warm') return 'WARM';
    return 'COLD';
  }

  function temperatureBadgeHtml(meta) {
    const t = meta.temperature;
    const cls = t === 'hot' ? 'lead-badge-hot' : t === 'warm' ? 'lead-badge-warm' : 'lead-badge-cold';
    const hint = meta.computed_only ? ' · stima' : '';
    const path = meta.owner_path ? ` · ${meta.owner_path}` : '';
    return `<span class="lead-score-badge ${cls}">${temperatureLabel(t)} ${meta.score}${path}${hint}</span>`;
  }

  function messaggioWithScorePrefix(messaggio, score) {
    const msg = String(messaggio ?? '').trim();
    const prefix = `[score:${score}]`;
    if (/^\[score:\d+\]/.test(msg)) {
      return msg.replace(/^\[score:\d+\]\s*/, `${prefix} `);
    }
    return msg ? `${prefix} ${msg}` : prefix;
  }

  function renderScoringGuide(rules) {
    if (!rules || !rules.signals) {
      return '<p style="font-size:0.85rem;color:var(--caffe)">Regole in <code>data/lead-scoring-rules.json</code></p>';
    }
    const th = rules.thresholds || {};
    const rows = rules.signals
      .map((s) => `<tr><td>${s.label}</td><td style="text-align:right;font-weight:600">${s.points > 0 ? '+' : ''}${s.points}</td></tr>`)
      .join('');
    return (
      `<details class="lead-scoring-guide" style="margin-bottom:16px">
        <summary style="cursor:pointer;font-weight:600;font-size:0.9rem">Guida lead scoring (0–100) · webhook <code>score-lead-righetto</code></summary>
        <p style="font-size:0.82rem;margin:10px 0 8px">HOT ≥${th.hot?.min ?? HOT} · WARM ${th.warm?.min ?? WARM}–${(th.warm?.max ?? HOT - 1)} · COLD &lt;${WARM}. Compila anche <code>data/acquisition-kpi-template.json</code> ogni venerdì.</p>
        <table class="lead-scoring-table"><thead><tr><th>Segnale</th><th>Punti</th></tr></thead><tbody>${rows}</tbody></table>
      </details>`
    );
  }

  function renderKpiReminder() {
    return `<div class="lead-kpi-reminder" style="background:var(--oro2);border-radius:8px;padding:12px 14px;margin-bottom:16px;font-size:0.85rem">
      <strong>KPI acquisizione (venerdì):</strong> aggiorna <code>data/acquisition-kpi-template.json</code> con lead HOT/WARM, sopralluoghi e mandati della settimana. Edge function Telegram su lead HOT se deployata.
    </div>`;
  }

  global.RighettoLeadScoring = {
    loadLeadScoringRules,
    scoreLeadRow,
    effectiveLeadMeta,
    temperatureBadgeHtml,
    messaggioWithScorePrefix,
    renderScoringGuide,
    renderKpiReminder,
    HOT,
    WARM,
  };
})(typeof window !== 'undefined' ? window : globalThis);
