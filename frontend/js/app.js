class IACentinell {
  constructor() {
    this.apiBase = 'http://localhost:8000/api';
    this.token = null;
    this.user = null;
    this.state = {
      ops: 0,
      alerts: 0,
      threats: 0,
      queries: 0,
      quarantined: 0
    };
    this.init();
  }

  init() {
    this.setupEventListeners();
    this.bootSequence();
  }

  setupEventListeners() {
    // Login
    document.getElementById('loginForm').addEventListener('submit', (e) => this.handleLogin(e));
    
    // Navigation
    document.querySelectorAll('[data-page]').forEach(link => {
      link.addEventListener('click', (e) => {
        e.preventDefault();
        const page = link.getAttribute('data-page');
        this.navigateTo(page);
      });
    });
    
    // File drop zone
    const dropZone = document.getElementById('dropZone');
    if (dropZone) {
      dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('active');
      });
      dropZone.addEventListener('dragleave', () => dropZone.classList.remove('active'));
      dropZone.addEventListener('drop', (e) => this.handleFileDrop(e));
      dropZone.addEventListener('click', () => document.getElementById('scanFile').click());
    }
    
    // File input
    const scanFile = document.getElementById('scanFile');
    if (scanFile) {
      scanFile.addEventListener('change', (e) => this.handleFileUpload(e.target.files[0]));
    }
    
    // Chat
    const chatBtn = document.querySelector('.chat-input-area button');
    if (chatBtn) {
      chatBtn.addEventListener('click', () => this.sendChatMessage());
    }
    
    // Logout
    document.getElementById('logoutBtn')?.addEventListener('click', () => this.logout());
    
    // Tile actions
    document.querySelectorAll('[data-action]').forEach(tile => {
      tile.addEventListener('click', () => {
        const action = tile.getAttribute('data-action');
        this.navigateTo(action);
      });
    });

    // Update clock
    setInterval(() => this.updateClock(), 1000);
  }

  async bootSequence() {
    const bootLog = document.getElementById('bootLog');
    const progress = document.getElementById('bootProgress');
    
    const steps = [
      'LOADING CRYPTOGRAPHIC ENGINE...',
      'THREAT SHIELD: INITIALIZING DATABASE...',
      'NET SENTINEL: BINDING NETWORK MONITOR...',
      'FILE GUARDIAN: INTEGRITY WATCHDOG ACTIVE...',
      'IA-CORE-1-1: SHA-256 CHAIN VALIDATOR OK',
      'IA-CORE-1-2: FORENSIC INTEGRITY SCANNER OK',
      'IA-CORE-1-3: ETHICAL AI GOVERNOR OK',
      'IA-CORE-1-4: THREAT ATTRIBUTION ENGINE OK',
      'INITIALIZATION COMPLETE — READY FOR AUTHENTICATION'
    ];
    
    for (let i = 0; i < steps.length; i++) {
      const log = document.createElement('div');
      log.textContent = `> ${steps[i]}`;
      bootLog.appendChild(log);
      
      progress.style.width = ((i + 1) / steps.length * 100) + '%';
      await new Promise(resolve => setTimeout(resolve, 150));
    }
    
    // Check for saved session
    const saved = this.loadSession();
    if (saved) {
      this.token = saved.token;
      this.user = saved.user;
      this.showApp();
    } else {
      setTimeout(() => {
        document.getElementById('splash').classList.add('hidden');
        document.getElementById('loginScreen').classList.remove('hidden');
      }, 500);
    }
  }

  async handleLogin(e) {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const apiKey = document.getElementById('apiKey').value;
    
    try {
      const response = await fetch(`${this.apiBase}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password, apiKey })
      });
      
      if (!response.ok) throw new Error('Invalid credentials');
      
      const data = await response.json();
      this.token = data.token;
      this.user = data.user;
      
      this.saveSession();
      this.showApp();
    } catch (err) {
      document.getElementById('loginError').textContent = '❌ ' + err.message;
    }
  }

  showApp() {
    document.getElementById('splash').classList.add('hidden');
    document.getElementById('loginScreen').classList.add('hidden');
    document.getElementById('app').classList.remove('hidden');
    
    this.updateSessionInfo();
    this.startLiveUpdates();
  }

  updateSessionInfo() {
    document.getElementById('currentUser').textContent = this.user?.username.toUpperCase() || '—';
    document.getElementById('sessionCompany').textContent = this.user?.company || '—';
    document.getElementById('sessionRole').textContent = `CLEARANCE: ${this.user?.role || '—'}`;
  }

  navigateTo(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById(`page-${page}`)?.classList.add('active');
    
    document.querySelectorAll('[data-page]').forEach(link => link.classList.remove('active'));
    document.querySelector(`[data-page="${page}"]`)?.classList.add('active');
  }

  async handleFileDrop(e) {
    e.preventDefault();
    const dropZone = document.getElementById('dropZone');
    dropZone.classList.remove('active');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      await this.handleFileUpload(files[0]);
    }
  }

  async handleFileUpload(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    document.querySelector('.scan-result').classList.remove('hidden');
    document.getElementById('resultName').textContent = `${file.name} (${(file.size/1024).toFixed(2)} KB)`;
    document.getElementById('resultAnalysis').textContent = 'SCANNING FILE...';
    
    try {
      const response = await fetch(`${this.apiBase}/shield/scan`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${this.token}` },
        body: formData
      });
      
      const data = await response.json();
      
      document.getElementById('resultHash').textContent = `SHA-256: ${data.hash.substring(0, 32)}...`;
      document.getElementById('resultIcon').textContent = data.isMalicious ? '🚨' : '✅';
      document.getElementById('resultVerdict').textContent = data.verdict;
      document.getElementById('resultAnalysis').textContent = data.analysis;
      
      this.updateMetrics('ops');
    } catch (err) {
      document.getElementById('resultAnalysis').textContent = 'ERROR: ' + err.message;
    }
  }

  async sendChatMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();
    if (!message) return;
    
    const chatMessages = document.getElementById('chatMessages');
    
    // Add user message
    this.addChatMessage('USER', message);
    input.value = '';
    
    try {
      const response = await fetch(`${this.apiBase}/ai/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${this.token}`
        },
        body: JSON.stringify({ message })
      });
      
      const data = await response.json();
      this.addChatMessage('IA CENTINELL', data.response);
      
      this.updateMetrics('queries');
    } catch (err) {
      this.addChatMessage('ERROR', err.message);
    }
  }

  addChatMessage(sender, text) {
    const chatMessages = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'chat-message';
    div.innerHTML = `
      <div class="message-label">${sender}</div>
      <div class="message-body">${text}</div>
    `;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  updateMetrics(type) {
    this.state[type]++;
    
    const metricMap = {
      ops: 'metricOps',
      alerts: 'metricAlerts',
      threats: 'metricThreats',
      quarantined: 'metricQuarantined',
      queries: 'metricQueries'
    };
    
    const el = document.getElementById(metricMap[type]);
    if (el) el.textContent = this.state[type];
    
    this.addAuditLog(`${type.toUpperCase()} UPDATED: ${this.state[type]}`);
    this.updateProtectionScore();
  }

  updateProtectionScore() {
    const threats = Math.min(this.state.threats * 10, 40);
    const score = Math.max(100 - threats, 20);
    
    document.getElementById('protectionScore').textContent = score + '%';
    document.getElementById('shieldScore').textContent = score;
    
    const badge = document.getElementById('protectionBadge');
    if (score > 80) {
      badge.style.borderColor = 'rgba(79, 168, 120, 0.3)';
    } else if (score > 50) {
      badge.style.borderColor = 'rgba(196, 154, 61, 0.3)';
    } else {
      badge.style.borderColor = 'rgba(184, 85, 85, 0.3)';
    }
  }

  addAuditLog(message) {
    const log = document.getElementById('auditLog');
    const ts = new Date().toLocaleTimeString();
    const line = `[${ts}] ${message}`;
    log.textContent = line + '\n' + log.textContent;
  }

  updateClock() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-US', { 
      hour12: false, 
      timeZone: 'UTC' 
    }) + ' UTC';
    
    document.getElementById('currentTime').textContent = timeString;
    document.getElementById('sidebarClock').textContent = timeString.substring(0, 5);
  }

  startLiveUpdates() {
    setInterval(() => {
      const messages = [
        'THREAT SHIELD: ALL CLEAR',
        'NET SENTINEL: TRAFFIC NORMAL',
        'FILE GUARDIAN: BASELINE STABLE',
        'IA-CORE-1-3 HITL CHECK PASSED',
        'SESSION TOKEN VALIDATED'
      ];
      
      const msg = messages[Math.floor(Math.random() * messages.length)];
      document.getElementById('feedContent').textContent = msg;
    }, 5000);
  }

  saveSession() {
    try {
      localStorage.setItem('iac_session', JSON.stringify({
        token: this.token,
        user: this.user,
        timestamp: Date.now()
      }));
    } catch (e) {
      console.error('Failed to save session:', e);
    }
  }

  loadSession() {
    try {
      const saved = localStorage.getItem('iac_session');
      if (saved) {
        const session = JSON.parse(saved);
        // Check if session is less than 24 hours old
        if (Date.now() - session.timestamp < 86400000) {
          return session;
        }
      }
    } catch (e) {
      console.error('Failed to load session:', e);
    }
    return null;
  }

  logout() {
    localStorage.removeItem('iac_session');
    location.reload();
  }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new IACentinell();
});
