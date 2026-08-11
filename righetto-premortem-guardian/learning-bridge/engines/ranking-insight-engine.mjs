#!/usr/bin/env node
/**
 * C. RANKING INSIGHT ENGINE — insight testuali supportati da dati.
 */

import fs from 'node:fs';
import path from 'node:path';
import { runLearningEngine } from './learning-engine.mjs';

const root = process.cwd();
const outDir = path.join(root, 'data', 'learning-bridge');

function confidence(sampleSize, minObs) {
  if (sampleSize < minObs) return 0;
  return Math.min(0.95, 0.4 + (sampleSize - minObs) / (minObs * 4));
}

export async function runRankingInsightEngine() {
  const report = await runLearningEngine();
  const minObs = report.min_observations;
  const insights = [];

  const { aggregates } = report;
  const searchesWithClicks = [];
  for (const [bucket, count] of Object.entries(aggregates.combinations || {})) {
    if (count < minObs) continue;
    const [tipoOp, zone, tipologia] = bucket.split('|');
    const clicksInBucket = Object.entries(aggregates.clicked_properties || {})
      .reduce((sum, [, n]) => sum + n, 0);
    if (clicksInBucket === 0) continue;

    if (aggregates.feature_frequency?.garage >= minObs) {
      insights.push({
        id: `insight_garage_${bucket}`,
        text:
          `Per ricerche ${tipologia !== 'any' ? `di ${tipologia}` : 'immobiliari'} ` +
          `${zone !== 'any' ? `a ${zone}` : ''} con richiesta di garage, ` +
          `gli utenti mostrano interesse per annunci con garage anche quando la posizione è meno centrale.`,
        sample_size: aggregates.feature_frequency.garage,
        confidence: confidence(aggregates.feature_frequency.garage, minObs),
        period: report.period,
        evidence: {
          garage_requests: aggregates.feature_frequency.garage,
          bucket_searches: count,
          property_clicks: aggregates.clicked_properties
        },
        disclaimer: 'Insight statistico — non modifica prezzi o disponibilità.'
      });
    }

    if (aggregates.feature_frequency?.terrazzo >= minObs) {
      insights.push({
        id: `insight_terrazzo_soft_${bucket}`,
        text:
          'Quando il terrazzo è dichiarato come preferenza soft, ' +
          'immobili senza terrazzo ma con metratura superiore continuano a ricevere click.',
        sample_size: aggregates.feature_frequency.terrazzo,
        confidence: confidence(aggregates.feature_frequency.terrazzo, minObs),
        period: report.period,
        evidence: {
          terrazzo_mentions: aggregates.feature_frequency.terrazzo,
          top_clicked: Object.entries(aggregates.clicked_properties || {})
            .sort((a, b) => b[1] - a[1])
            .slice(0, 5)
        },
        disclaimer: 'Insight statistico — verificare con campione più ampio prima di cambiare ranking.'
      });
    }
  }

  if ((aggregates.zero_result_queries || []).length >= 5) {
    insights.push({
      id: 'insight_zero_results',
      text: 'Alcune combinazioni zona/tipologia terminano spesso senza risultati nel catalogo attuale.',
      sample_size: aggregates.zero_result_queries.length,
      confidence: confidence(aggregates.zero_result_queries.length, 5),
      period: report.period,
      evidence: { samples: aggregates.zero_result_queries.slice(0, 10) },
      disclaimer: 'Opportunità SEO/contenuto — non inventare annunci.'
    });
  }

  const unanswered = (aggregates.unanswered_questions || []).length;
  if (unanswered >= 3) {
    insights.push({
      id: 'insight_unanswered',
      text: 'Domande ricorrenti senza risposta FAQ — candidato per nuova voce FAQ o articolo blog.',
      sample_size: unanswered,
      confidence: confidence(unanswered, 3),
      period: report.period,
      evidence: { unanswered_count: unanswered },
      disclaimer: 'Usare hash messaggio — no testo utente in chiaro.'
    });
  }

  const output = {
    generated_at: new Date().toISOString(),
    ranking_insights: insights,
    seo_opportunities: insights.filter((i) => i.id.includes('zero') || i.id.includes('unanswered')),
    unanswered_questions: aggregates.unanswered_questions || [],
    emerging_preferences: report.emerging_preferences
  };

  fs.writeFileSync(path.join(outDir, 'ranking-insights.json'), JSON.stringify(output, null, 2));
  return output;
}

if (import.meta.url === `file://${process.argv[1]}`) {
  runRankingInsightEngine().then((o) => console.log('Ranking Insights:', o.ranking_insights.length));
}
