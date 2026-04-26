#!/usr/bin/env node
/**
 * One Donate Server - Gộp donate từ Zypage, Wescan, YouTube vào 1 queue
 * Chạy: node server.js
 * Overlay: mở donate-overlay.html trong OBS Browser Source
 */

const http = require('http');
const url = require('url');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 3847;
const OVERLAY_PATH = path.join(__dirname, 'donate-overlay.html');
const CSS3_PATH = path.join(__dirname, '..', 'css3.css');
const queue = [];
const clients = new Set();

// Chuẩn hóa donate từ mọi nguồn về format thống nhất
function normalizeDonate(raw, platform) {
  return {
    donorName: raw.donorName || raw.name || raw.donor_name || raw.username || 'Ẩn danh',
    amount: parseFloat(raw.amount || raw.money || raw.value || 0) || 0,
    message: raw.message || raw.comment || raw.text || '',
    currency: raw.currency || '₫',
    platform: platform,
    avatar: raw.avatar || raw.image || raw.photo
  };
}

// Parser cho từng nền tảng - chỉnh sửa theo API thực tế của từng nền tảng
function parseZypage(body) {
  try {
    const data = typeof body === 'string' ? JSON.parse(body) : body;
    return normalizeDonate({
      donorName: data.user?.name || data.donorName || data.from,
      amount: data.amount ?? data.money ?? data.value,
      message: data.message || data.content || data.comment
    }, 'zypage');
  } catch (e) {
    return null;
  }
}

function parseWescan(body) {
  try {
    const data = typeof body === 'string' ? JSON.parse(body) : body;
    return normalizeDonate({
      donorName: data.user?.name || data.donorName || data.sender,
      amount: data.amount ?? data.money ?? data.value,
      message: data.message || data.content || data.note
    }, 'wescan');
  } catch (e) {
    return null;
  }
}

function parseYoutube(body) {
  try {
    const data = typeof body === 'string' ? JSON.parse(body) : body;
    return normalizeDonate({
      donorName: data.author?.name || data.donorName || data.user,
      amount: data.amount ?? data.money ?? data.microAmount / 1000000,
      message: data.message || data.text || data.snippet
    }, 'youtube');
  } catch (e) {
    return null;
  }
}

function addDonate(donate) {
  if (!donate || !donate.donorName) return false;
  queue.push(donate);
  broadcast(JSON.stringify(donate));
  console.log(`[+] ${donate.platform}: ${donate.donorName} - ${donate.amount} ${donate.currency}`);
  return true;
}

function broadcast(data) {
  clients.forEach((res) => {
    try {
      res.write(`data: ${data}\n\n`);
    } catch (e) {}
  });
}

const server = http.createServer((req, res) => {
  const parsed = url.parse(req.url, true);
  const path = parsed.pathname;
  const method = req.method;

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // SSE stream cho overlay
  if (path === '/stream') {
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive'
    });
    clients.add(res);
    req.on('close', () => clients.delete(res));
    return;
  }

  // Webhook: Zypage
  if (path === '/webhook/zypage' && method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      const donate = parseZypage(body);
      if (donate) addDonate(donate);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: !!donate }));
    });
    return;
  }

  // Webhook: Wescan
  if (path === '/webhook/wescan' && method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      const donate = parseWescan(body);
      if (donate) addDonate(donate);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: !!donate }));
    });
    return;
  }

  // Webhook: YouTube (hoặc dùng bridge từ extension/tool khác)
  if (path === '/webhook/youtube' && method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      const donate = parseYoutube(body);
      if (donate) addDonate(donate);
      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({ ok: !!donate }));
    });
    return;
  }

  // API thủ công: POST /donate (để test hoặc tích hợp custom)
  if (path === '/donate' && method === 'POST') {
    let body = '';
    req.on('data', (chunk) => { body += chunk; });
    req.on('end', () => {
      try {
        const data = JSON.parse(body);
        const donate = normalizeDonate(data, data.platform || 'youtube');
        addDonate(donate);
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: true }));
      } catch (e) {
        res.writeHead(400, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ ok: false, error: e.message }));
      }
    });
    return;
  }

  // Overlay (OBS Browser Source có thể dùng URL này)
  if (path === '/overlay') {
    try {
      const html = fs.readFileSync(OVERLAY_PATH, 'utf8')
        .replace('http://localhost:3847', `http://localhost:${PORT}`)
        .replace(/href="\.\.\/css3\.css"/, `href="http://localhost:${PORT}/css3.css"`);
      res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
      res.end(html);
    } catch (e) {
      res.writeHead(500);
      res.end('Overlay not found');
    }
    return;
  }

  // CSS3 (overlay dùng khi load qua /overlay)
  if (path === '/css3.css') {
    try {
      const css = fs.readFileSync(CSS3_PATH, 'utf8');
      res.writeHead(200, { 'Content-Type': 'text/css' });
      res.end(css);
    } catch (e) {
      res.writeHead(404);
      res.end('Not found');
    }
    return;
  }

  // Trang test
  if (path === '/' || path === '/test') {
    res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
    res.end(`
<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>One Donate - Test</title></head>
<body style="font-family:sans-serif;padding:20px;background:#1a1a1a;color:#fff">
<h1>One Donate Server</h1>
<p>Server đang chạy. Webhook endpoints:</p>
<ul>
  <li>POST /webhook/zypage</li>
  <li>POST /webhook/wescan</li>
  <li>POST /webhook/youtube</li>
  <li>POST /donate (body: {"donorName","amount","message","platform"})</li>
</ul>
<p>Overlay: <a href="/overlay" style="color:#4fc3f7">/overlay</a> | URL cho OBS: <code>http://localhost:${PORT}/overlay</code></p>
<hr>
<button onclick="testDonate('zypage')">Test Zypage</button>
<button onclick="testDonate('wescan')">Test Wescan</button>
<button onclick="testDonate('youtube')">Test YouTube</button>
<script>
function testDonate(platform) {
  fetch('/donate', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({
      donorName: 'Người test ' + platform,
      amount: Math.floor(Math.random()*500+50)*1000,
      message: 'Donate test từ ' + platform + '!',
      platform: platform
    })
  }).then(r=>r.json()).then(console.log);
}
</script>
</body></html>
    `);
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  console.log(`One Donate Server: http://localhost:${PORT}`);
  console.log('Overlay: one-donate/donate-overlay.html');
  console.log('Webhooks: /webhook/zypage, /webhook/wescan, /webhook/youtube');
});
