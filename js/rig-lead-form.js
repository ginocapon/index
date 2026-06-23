/**
 * Righetto — invio lead unificato (landing, blog, servizi, homepage)
 * GDPR: consenso obbligatorio a/b + marketing facoltativo c/d/e
 */
(function (global) {
  var SB_URL = 'https://qwkwkemuabfwvwuqrxlu.supabase.co';
  var SB_ANON =
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF3a3drZW11YWJmd3Z3dXFyeGx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzE1OTk5NjEsImV4cCI6MjA4NzE3NTk2MX0.JxEYiWVPEOiwjZtbWAZRlMUdKXcupjw7filvrERCiqc';
  var TEL = '049.8843484';

  function val(sel) {
    if (!sel) return '';
    var el = typeof sel === 'string' ? document.querySelector(sel) : sel;
    return el && el.value ? String(el.value).trim() : '';
  }

  function checked(sel) {
    var el = typeof sel === 'string' ? document.querySelector(sel) : sel;
    return el ? !!el.checked : false;
  }

  function resolveField(form, spec) {
    if (!spec) return null;
    if (Array.isArray(spec)) {
      var parts = spec.map(function (s) {
        return val(form.querySelector(s));
      }).filter(Boolean);
      return { value: parts.join(' ') };
    }
    var el = form.querySelector(spec);
    return el;
  }

  function parseFields(form) {
    var raw = form.getAttribute('data-fields');
    if (raw) {
      try {
        var cfg = JSON.parse(raw);
        return {
          nome: resolveField(form, cfg.nome),
          cognome: resolveField(form, cfg.cognome),
          tel: resolveField(form, cfg.tel),
          email: resolveField(form, cfg.email),
          msg: resolveField(form, cfg.msg),
          gdpr: resolveField(form, cfg.gdpr),
          gdprMarketing: resolveField(form, cfg.gdprMarketing)
        };
      } catch (e) {}
    }
    return {
      nome: form.querySelector('#bl-nome, #f-nome, #cf-nome, #nome, [name="nome"]'),
      cognome: form.querySelector('#cf-cognome, #f-cog, [name="cognome"]'),
      tel: form.querySelector('#bl-tel, #f-tel, #cf-tel, #tel, [name="telefono"]'),
      email: form.querySelector('#bl-email, #f-email, #f-mail, #cf-email, #email, [name="email"]'),
      msg: form.querySelector('#bl-msg, #f-msg, #f-note, #cf-msg, #msg, [name="messaggio"]'),
      gdpr: form.querySelector(
        '#bl-gdpr, #f-gdpr, #gdpr, [name="gdpr"], input[id*="bl-gdpr"][required], input[id*="gdpr"][required]'
      ),
      gdprMarketing: form.querySelector('.rig-gdpr-marketing, #f-gdpr-marketing, [name="gdpr_marketing"]')
    };
  }

  function buildMessaggio(form, fields, baseMsg) {
    var parts = [];
    if (baseMsg) parts.push(baseMsg);
    var extra = form.getAttribute('data-extra-labels');
    if (extra) {
      try {
        var map = JSON.parse(extra);
        Object.keys(map).forEach(function (sel) {
          var v = val(form.querySelector(sel));
          if (v) parts.push(map[sel] + ': ' + v);
        });
      } catch (e) {}
    }
    if (fields.gdprMarketing && checked(fields.gdprMarketing)) {
      parts.push('Consenso marketing (c/d/e): SI');
    }
    return parts.join(' | ') || baseMsg || '';
  }

  async function submitLead(form) {
    var fields = parseFields(form);
    var nome = fields.nome && fields.nome.value != null ? fields.nome.value : val(fields.nome);
    var cognome = val(fields.cognome);
    var nomeCompleto = cognome ? nome + ' ' + cognome : nome;
    var tel = val(fields.tel);
    var email = val(fields.email);
    var msg = val(fields.msg);
    var provenienza = form.getAttribute('data-provenienza') || 'form-sito';
    var prefix = form.getAttribute('data-msg-prefix') || '';
    var marketingOk = fields.gdprMarketing ? checked(fields.gdprMarketing) : false;

    if (!nomeCompleto || !tel) {
      alert('Inserisci nome e telefono');
      return false;
    }
    if (fields.gdpr && !checked(fields.gdpr)) {
      alert('Accetta l\'informativa privacy (finalità contrattuali e di legge) per procedere');
      return false;
    }

    var btn = form.querySelector('[type="submit"], .fsub, .v-submit, .btn-send, .fc-submit');
    var btnText = btn ? btn.textContent : '';
    if (btn) {
      btn.disabled = true;
      btn.textContent = 'Invio in corso...';
    }

    var messaggioDb = buildMessaggio(form, fields, (prefix ? prefix + ' ' : '') + msg);
    var pagina = form.getAttribute('data-pagina') || provenienza;

    var bodyParts = ['<b>Nome:</b> ' + nomeCompleto, '<b>Telefono:</b> ' + tel];
    if (email) bodyParts.push('<b>Email:</b> ' + email);
    if (messaggioDb) bodyParts.push('<b>Messaggio:</b><br>' + messaggioDb.replace(/\n/g, '<br>'));
    bodyParts.push('<b>Pagina:</b> ' + pagina);
    if (marketingOk) bodyParts.push('<b>Consenso marketing (c/d/e):</b> Sì');

    var emailOk = false;
    try {
      if (typeof SERVIZI_CONFIG !== 'undefined') {
        emailOk = await SERVIZI_CONFIG.sendNotifica({
          subject: 'Nuovo contatto dal sito: ' + nomeCompleto,
          html_body: bodyParts.join('<br>'),
          reply_to: email || undefined
        });
      }
    } catch (e) {
      emailOk = false;
    }

    var supaOk = false;
    try {
      var sb = global.supabase && global.supabase.createClient(SB_URL, SB_ANON);
      if (sb) {
        await sb.from('richieste').insert([
          {
            nome: nomeCompleto,
            email: email || null,
            telefono: tel,
            messaggio: messaggioDb || null,
            provenienza: provenienza,
            newsletter: marketingOk,
            letto: false
          }
        ]);
        supaOk = true;
      }
    } catch (e) {
      supaOk = false;
    }

    if (btn) {
      btn.disabled = false;
      btn.textContent = btnText || 'Invia richiesta';
    }

    if (emailOk || supaOk) {
      form.classList.add('is-sent');
      var ok = form.querySelector('.rig-lead-success');
      if (ok) ok.style.display = 'block';
      var okP = ok && ok.querySelector('p');
      if (okP && !emailOk) {
        okP.textContent = 'Richiesta registrata. Se non ricevi notizie, chiama il ' + TEL + '.';
      }
      return true;
    }
    alert('Errore nell\'invio. Chiama il ' + TEL + ' o scrivi a info@righettoimmobiliare.it');
    return false;
  }

  function bindForm(form) {
    if (form.dataset.rigBound === '1') return;
    form.dataset.rigBound = '1';
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      submitLead(form);
    });
  }

  function init() {
    document.querySelectorAll('form[data-rig-lead-form]').forEach(bindForm);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  global.rigSubmitLead = submitLead;
})();
