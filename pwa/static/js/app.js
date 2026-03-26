// D&D Drafter & Researcher — PWA App Logic
const App = {
  apiKey: localStorage.getItem('dnd_api_key') || '',
  currentPage: 'home',

  init() {
    this.bindNav();
    this.loadApiKey();
    this.navigate('home');
    this.registerSW();
  },

  registerSW() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    }
  },

  // ─── Navigation ───
  bindNav() {
    document.querySelectorAll('[data-page]').forEach(el => {
      el.addEventListener('click', e => {
        e.preventDefault();
        this.navigate(el.dataset.page);
      });
    });
  },

  navigate(page) {
    this.currentPage = page;
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.bottom-nav a').forEach(a => a.classList.remove('active'));
    const pageEl = document.getElementById('page-' + page);
    const navEl = document.querySelector(`[data-page="${page}"]`);
    if (pageEl) pageEl.classList.add('active');
    if (navEl) navEl.classList.add('active');
    window.scrollTo(0, 0);
  },

  // ─── API Key ───
  loadApiKey() {
    const input = document.getElementById('api-key-input');
    if (input && this.apiKey) {
      input.value = this.apiKey;
      this.updateKeyStatus(true);
    }
  },

  saveApiKey() {
    const input = document.getElementById('api-key-input');
    this.apiKey = input.value.trim();
    localStorage.setItem('dnd_api_key', this.apiKey);
    this.updateKeyStatus(!!this.apiKey);
    this.toast(this.apiKey ? 'API key saved' : 'API key cleared');
  },

  updateKeyStatus(ok) {
    const status = document.getElementById('key-status');
    if (status) status.textContent = ok ? '✓' : '○';
  },

  // ─── AI: Draft ───
  async draft() {
    if (!this.checkKey()) return;
    const data = {
      api_key: this.apiKey,
      doc_type: document.getElementById('draft-type').value,
      court: document.getElementById('draft-court').value,
      parties: document.getElementById('draft-parties').value,
      facts: document.getElementById('draft-facts').value,
      relief: document.getElementById('draft-relief').value,
      additional: document.getElementById('draft-additional').value,
    };
    if (!data.facts.trim()) return this.toast('Please enter case facts');
    this.showSpinner('draft-spinner', 'Claude is drafting your document...');
    const res = await this.post('/api/draft', data);
    this.hideSpinner('draft-spinner');
    this.showResult('draft-result', res.result);
  },

  // ─── AI: Research ───
  async research() {
    if (!this.checkKey()) return;
    const data = {
      api_key: this.apiKey,
      query: document.getElementById('research-query').value,
      research_type: document.getElementById('research-type').value,
    };
    if (!data.query.trim()) return this.toast('Please enter your question');
    this.showSpinner('research-spinner', 'Researching...');
    const res = await this.post('/api/research', data);
    this.hideSpinner('research-spinner');
    this.showResult('research-result', res.result);
  },

  // ─── AI: Case Analysis ───
  async analyze() {
    if (!this.checkKey()) return;
    const data = {
      api_key: this.apiKey,
      client_side: document.getElementById('analyze-side').value,
      case_type: document.getElementById('analyze-type').value,
      facts: document.getElementById('analyze-facts').value,
      opponent: document.getElementById('analyze-opponent').value,
    };
    if (!data.facts.trim()) return this.toast('Please enter case facts');
    this.showSpinner('analyze-spinner', 'Analyzing case...');
    const res = await this.post('/api/analyze', data);
    this.hideSpinner('analyze-spinner');
    this.showResult('analyze-result', res.result);
  },

  // ─── AI: Review Draft ───
  async reviewDraft() {
    if (!this.checkKey()) return;
    const data = {
      api_key: this.apiKey,
      draft: document.getElementById('review-draft').value,
      doc_type: document.getElementById('review-type').value,
    };
    if (!data.draft.trim()) return this.toast('Please paste your draft');
    this.showSpinner('review-spinner', 'Reviewing draft...');
    const res = await this.post('/api/review', data);
    this.hideSpinner('review-spinner');
    this.showResult('review-result', res.result);
  },

  // ─── Limitation Calculator ───
  async calcLimitation() {
    const key = document.getElementById('lim-article').value;
    const date = document.getElementById('lim-date').value;
    if (!key || !date) return this.toast('Select article and date');
    const parts = date.split('-');
    const ddmmyyyy = `${parts[2]}-${parts[1]}-${parts[0]}`;
    const res = await this.post('/api/limitation', { article_key: key, coa_date: ddmmyyyy });
    const el = document.getElementById('lim-result');
    if (res.error) { el.innerHTML = `<div class="badge badge-danger">${res.error}</div>`; return; }
    const statusClass = { EXPIRED:'danger', CRITICAL:'danger', URGENT:'warning', APPROACHING:'warning', WITHIN_TIME:'success', NO_LIMITATION:'info' }[res.status] || 'info';
    el.innerHTML = `
      <div class="card">
        <div style="text-align:center;margin-bottom:12px"><span class="badge badge-${statusClass}" style="font-size:16px;padding:8px 20px">${res.status}</span></div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;text-align:center">
          <div><div style="font-size:11px;color:var(--text-light)">PERIOD</div><div style="font-size:16px;font-weight:700">${res.limitation_period}</div></div>
          <div><div style="font-size:11px;color:var(--text-light)">EXPIRY</div><div style="font-size:16px;font-weight:700">${res.expiry_date}</div></div>
        </div>
        <div style="margin-top:12px;padding:10px;background:#f0f4ff;border-radius:8px;font-size:13px">${res.urgency}</div>
      </div>`;
  },

  // ─── Court Fee Calculator ───
  async calcFee() {
    const category = document.getElementById('fee-category').value;
    const suitType = document.getElementById('fee-type').value;
    const value = parseFloat(document.getElementById('fee-value').value) || 0;
    const res = await this.post('/api/court-fee', { suit_value: value, suit_type: suitType, fee_category: category });
    const el = document.getElementById('fee-result');
    if (res.error) { el.innerHTML = `<div class="badge badge-danger">${res.error}</div>`; return; }
    el.innerHTML = `
      <div class="card" style="text-align:center">
        <div style="font-size:13px;color:var(--text-light)">COURT FEE</div>
        <div style="font-size:24px;font-weight:800;color:var(--primary);margin:8px 0">${res.court_fee_formatted}</div>
        <div style="font-size:13px;color:var(--text-light)">${res.note || ''}</div>
      </div>`;
  },

  // ─── Amount Converter ───
  async convertAmount() {
    const val = parseFloat(document.getElementById('amount-input').value) || 0;
    const res = await this.post('/api/amount', { amount: val });
    document.getElementById('amount-result').innerHTML = `
      <div class="card" style="text-align:center">
        <div style="font-size:18px;font-weight:700;color:var(--primary);word-break:break-word">${res.formatted}</div>
      </div>`;
  },

  // ─── Jurisdiction ───
  async checkJurisdiction() {
    const data = {
      suit_type: document.getElementById('jur-type').value,
      suit_value: parseFloat(document.getElementById('jur-value').value) || 0,
      location: document.getElementById('jur-location').value || 'Visakhapatnam'
    };
    const res = await this.post('/api/jurisdiction', data);
    const el = document.getElementById('jur-result');
    if (res.error) { el.innerHTML = `<div class="badge badge-danger">${res.error}</div>`; return; }
    let warnings = '';
    if (res.warnings && res.warnings.length) {
      warnings = res.warnings.map(w => `<div style="padding:6px 10px;background:#fef3c7;border-radius:6px;font-size:12px;margin-top:6px">⚠ ${w}</div>`).join('');
    }
    el.innerHTML = `
      <div class="card">
        <div style="font-size:13px;color:var(--text-light)">CORRECT COURT</div>
        <div style="font-size:17px;font-weight:700;color:var(--primary);margin:6px 0">${res.correct_court}</div>
        ${res.designation ? `<div style="font-size:13px">Designation: <strong>${res.designation}</strong></div>` : ''}
        ${res.jurisdiction_type ? `<div style="font-size:13px">Type: ${res.jurisdiction_type}</div>` : ''}
        ${warnings}
      </div>`;
  },

  // ─── Helpers ───
  checkKey() {
    if (!this.apiKey) { this.toast('Enter API key in Settings first'); this.navigate('settings'); return false; }
    return true;
  },

  async post(url, data) {
    try {
      const r = await fetch(url, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(data) });
      return await r.json();
    } catch(e) { return { error: 'Network error: ' + e.message, result: 'ERROR: Network error — check your connection' }; }
  },

  showSpinner(id, text) {
    const el = document.getElementById(id);
    if (el) { el.innerHTML = `<div class="spinner active"></div><div class="spinner-text">${text}</div>`; el.style.display='block'; }
  },
  hideSpinner(id) {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  },

  showResult(id, text) {
    const el = document.getElementById(id);
    if (!el) return;
    // Basic markdown: bold, headers, lists
    let html = text
      .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
      .replace(/^### (.+)$/gm, '<h3>$1</h3>')
      .replace(/^## (.+)$/gm, '<h2>$1</h2>')
      .replace(/^# (.+)$/gm, '<h1>$1</h1>')
      .replace(/^- (.+)$/gm, '• $1')
      .replace(/\n/g, '<br>');
    el.innerHTML = `<div class="result-box">${html}</div>`;
  },

  toast(msg) {
    let t = document.getElementById('toast');
    if (!t) { t = document.createElement('div'); t.id='toast'; t.className='toast'; document.body.appendChild(t); }
    t.textContent = msg; t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 2500);
  },

  copyResult(id) {
    const el = document.getElementById(id);
    if (el) {
      const text = el.innerText || el.textContent;
      navigator.clipboard.writeText(text).then(() => this.toast('Copied!')).catch(() => this.toast('Copy failed'));
    }
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
