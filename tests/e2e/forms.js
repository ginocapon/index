// Definizione condivisa dei moduli lead sotto test (usata da leads.spec e failures.spec).
const { TEST_LEAD } = require('./helpers');

const FORMS = [
  {
    nome: 'servizio-vendita', url: '/servizio-vendita', provenienza: 'form-vendita',
    fill: async (p) => {
      await p.fill('#f-nome', `${TEST_LEAD.nome} ${TEST_LEAD.cognome}`);
      await p.fill('#f-tel', TEST_LEAD.tel);
      await p.fill('#f-email', TEST_LEAD.email);
      await p.check('#f-gdpr');
    },
    submit: 'form[data-rig-lead-form] button[type=submit]',
    ok: 'form[data-rig-lead-form].is-sent',
  },
  {
    nome: 'homepage', url: '/', provenienza: 'homepage',
    fill: async (p) => {
      await p.fill('#cf-nome', TEST_LEAD.nome);
      await p.fill('#cf-cognome', TEST_LEAD.cognome);
      await p.fill('#cf-tel', TEST_LEAD.tel);
      await p.fill('#cf-email', TEST_LEAD.email);
      await p.check('#cf-gdpr');
    },
    submit: '#contattoForm button[type=submit]',
    ok: '#contattoForm.is-sent',
  },
  {
    nome: 'contatti', url: '/contatti', provenienza: 'form-contatti',
    fill: async (p) => {
      await p.fill('#f-nome', TEST_LEAD.nome);
      await p.fill('#f-cog', TEST_LEAD.cognome);
      await p.fill('#f-tel', TEST_LEAD.tel);
      await p.fill('#f-mail', TEST_LEAD.email);
      await p.check('#f-gdpr');
    },
    submit: '#contact-form .fsubmit',
    ok: '#success',
  },
  {
    nome: 'landing-consulenza', url: '/landing-consulenza-immobiliare-gratuita', provenienza: null,
    fill: async (p) => {
      await p.fill('#nome', `${TEST_LEAD.nome} ${TEST_LEAD.cognome}`);
      await p.fill('#tel', TEST_LEAD.tel);
      await p.fill('#email', TEST_LEAD.email);
      await p.check('#gdpr');
    },
    submit: '#consulenza-form .v-submit',
    ok: '#consulenza-ok',
  },
  {
    nome: 'landing-valutazione', url: '/landing-valutazione', provenienza: 'landing-valutazione',
    fill: async (p) => {
      await p.fill('#v-comune', 'Padova centro storico');
      await p.selectOption('#v-tipo', 'Appartamento');
      await p.evaluate(() => goStep(2));
      await p.evaluate(() => goStep(3));
      await p.fill('#v-nome', TEST_LEAD.nome);
      await p.fill('#v-cognome', TEST_LEAD.cognome);
      await p.fill('#v-tel', TEST_LEAD.tel);
      await p.fill('#v-email', TEST_LEAD.email);
      await p.check('#v-gdpr');
    },
    submit: '#leadForm .fc-submit',
    ok: '#leadSuccess',
  },
];

module.exports = { FORMS };
