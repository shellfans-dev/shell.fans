/*!
 * ShellFans AEO Chat Widget
 *
 * 嵌入方式：<script src="/js/aeo-chat.js" defer></script>
 *
 * 設計取捨：
 *   - 純原生 JS，無框架依賴 —— shell.fans 是靜態站，不該為了一個 widget
 *     引入建置流程
 *   - 所有訊息以 textContent 寫入，絕不使用 innerHTML —— 訊息內容來自
 *     使用者與客服，是最典型的 XSS 入口
 *   - 3 秒輪詢而非長連線：真人客服的節奏用輪詢足夠，且穿過 CDN 比長連線
 *     穩定（長連線遇 idle timeout 會靜默斷開，最糟的失敗模式是「以為在線上
 *     其實沒收到」）
 *   - 分頁隱藏時停止輪詢，避免背景分頁持續打 API
 */
(function () {
  'use strict';

  var API = 'https://console.shell.fans/api/site/aeo-chat';
  var POLL_MS = 3000;
  var STORE_KEY = 'sf_aeo_chat_open';

  var state = {
    conversationId: null,
    messages: [],
    open: false,
    sending: false,
    timer: null,
    lastCount: 0,
    unread: 0,
  };

  // ---------- 樣式 ----------
  var css = ''
    + '.sfc-btn{position:fixed;right:20px;bottom:20px;width:56px;height:56px;border-radius:50%;'
    + 'background:#E96F5E;color:#fff;border:0;cursor:pointer;box-shadow:0 6px 20px rgba(0,0,0,.18);'
    + 'display:flex;align-items:center;justify-content:center;z-index:2147483000;transition:transform .18s}'
    + '.sfc-btn:hover{transform:translateY(-2px)}'
    + '.sfc-badge{position:absolute;top:-2px;right:-2px;min-width:20px;height:20px;border-radius:10px;'
    + 'background:#111;color:#fff;font-size:11px;line-height:20px;text-align:center;padding:0 5px}'
    + '.sfc-panel{position:fixed;right:20px;bottom:88px;width:360px;max-width:calc(100vw - 32px);'
    + 'height:520px;max-height:calc(100vh - 120px);background:#fff;border-radius:16px;'
    + 'box-shadow:0 16px 48px rgba(0,0,0,.18);display:none;flex-direction:column;overflow:hidden;'
    + 'z-index:2147483000;font-family:inherit}'
    + '.sfc-panel.open{display:flex}'
    + '.sfc-head{padding:16px 18px;background:#101214;color:#fff}'
    + '.sfc-head h3{margin:0;font-size:15px;font-weight:600}'
    + '.sfc-head p{margin:4px 0 0;font-size:12px;opacity:.75;line-height:1.5}'
    + '.sfc-body{flex:1;overflow-y:auto;padding:14px;background:#FAFAF8}'
    + '.sfc-msg{margin-bottom:10px;display:flex}'
    + '.sfc-msg.me{justify-content:flex-end}'
    + '.sfc-bub{max-width:80%;padding:9px 12px;border-radius:14px;font-size:13.5px;line-height:1.6;'
    + 'white-space:pre-wrap;word-break:break-word}'
    + '.sfc-msg.me .sfc-bub{background:#101214;color:#fff}'
    + '.sfc-msg.them .sfc-bub{background:#fff;color:#101214;border:1px solid #E5E7EB}'
    + '.sfc-msg.sys .sfc-bub{background:transparent;color:#9CA3AF;font-size:12px;text-align:center;max-width:100%}'
    + '.sfc-who{font-size:10px;opacity:.6;margin-bottom:2px}'
    + '.sfc-quick{padding:0 14px 10px;background:#FAFAF8;display:flex;flex-wrap:wrap;gap:6px}'
    + '.sfc-quick button{border:1px solid #E5E7EB;background:#fff;border-radius:16px;padding:6px 11px;'
    + 'font-size:12px;cursor:pointer;color:#101214;font-family:inherit}'
    + '.sfc-quick button:hover{border-color:#E96F5E;color:#E96F5E}'
    + '.sfc-foot{border-top:1px solid #E5E7EB;padding:10px;display:flex;gap:8px;background:#fff}'
    + '.sfc-foot textarea{flex:1;resize:none;border:1px solid #E5E7EB;border-radius:10px;padding:8px 10px;'
    + 'font-size:13.5px;font-family:inherit;outline:none;max-height:90px}'
    + '.sfc-foot textarea:focus{border-color:#101214}'
    + '.sfc-foot button{border:0;background:#E96F5E;color:#fff;border-radius:10px;padding:0 16px;'
    + 'font-size:13.5px;cursor:pointer;font-family:inherit}'
    + '.sfc-foot button:disabled{opacity:.45;cursor:default}'
    + '.sfc-err{padding:8px 14px;background:#FEF2F2;color:#991B1B;font-size:12px}'
    + '@media(max-width:480px){.sfc-panel{right:8px;left:8px;width:auto;bottom:78px;height:calc(100vh - 100px)}'
    + '.sfc-btn{right:14px;bottom:14px}}';

  var st = document.createElement('style');
  st.textContent = css;
  document.head.appendChild(st);

  // ---------- DOM ----------
  var btn = document.createElement('button');
  btn.className = 'sfc-btn';
  btn.setAttribute('aria-label', '線上諮詢');
  btn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
    + 'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    + '<path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"/></svg>';

  var badge = document.createElement('span');
  badge.className = 'sfc-badge';
  badge.style.display = 'none';
  btn.appendChild(badge);

  var panel = document.createElement('div');
  panel.className = 'sfc-panel';
  panel.setAttribute('role', 'dialog');
  panel.setAttribute('aria-label', 'ShellFans 線上諮詢');

  var head = document.createElement('div');
  head.className = 'sfc-head';
  var h3 = document.createElement('h3');
  h3.textContent = 'ShellFans 線上諮詢';
  var sub = document.createElement('p');
  sub.textContent = '我們可以協助您了解網站是否適合導入 AEO，以及 90 天成效驗證方案。';
  head.appendChild(h3);
  head.appendChild(sub);

  var body = document.createElement('div');
  body.className = 'sfc-body';

  var errBar = document.createElement('div');
  errBar.className = 'sfc-err';
  errBar.style.display = 'none';

  var quick = document.createElement('div');
  quick.className = 'sfc-quick';

  var foot = document.createElement('div');
  foot.className = 'sfc-foot';
  var ta = document.createElement('textarea');
  ta.rows = 1;
  ta.placeholder = '輸入訊息…';
  var sendBtn = document.createElement('button');
  sendBtn.textContent = '送出';
  foot.appendChild(ta);
  foot.appendChild(sendBtn);

  panel.appendChild(head);
  panel.appendChild(errBar);
  panel.appendChild(body);
  panel.appendChild(quick);
  panel.appendChild(foot);
  document.body.appendChild(btn);
  document.body.appendChild(panel);

  // ---------- 工具 ----------
  function utm() {
    var p = new URLSearchParams(location.search);
    var o = {};
    ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'].forEach(function (k) {
      if (p.get(k)) o[k] = p.get(k);
    });
    return o;
  }

  function showErr(msg) {
    errBar.textContent = msg;
    errBar.style.display = 'block';
    setTimeout(function () { errBar.style.display = 'none'; }, 5000);
  }

  function render() {
    body.textContent = '';
    if (state.messages.length === 0) {
      var hint = document.createElement('div');
      hint.className = 'sfc-msg sys';
      var hb = document.createElement('div');
      hb.className = 'sfc-bub';
      hb.textContent = '您好，請問想了解哪個部分？也可以直接輸入問題。';
      hint.appendChild(hb);
      body.appendChild(hint);
    }
    state.messages.forEach(function (m) {
      var row = document.createElement('div');
      row.className = 'sfc-msg ' + (m.from === 'visitor' ? 'me' : m.from === 'system' ? 'sys' : 'them');
      var bub = document.createElement('div');
      bub.className = 'sfc-bub';
      if (m.from === 'shellfans' && m.name) {
        var who = document.createElement('div');
        who.className = 'sfc-who';
        who.textContent = m.name;          // textContent，不用 innerHTML
        bub.appendChild(who);
      }
      var txt = document.createElement('div');
      txt.textContent = m.content;         // 同上，這是 XSS 的主要入口
      bub.appendChild(txt);
      row.appendChild(bub);
      body.appendChild(row);
    });
    body.scrollTop = body.scrollHeight;
  }

  var QUICKS = [
    { label: '我想了解 AEO', text: '我想了解 AEO 是什麼，對我的網站有什麼幫助？' },
    { label: '我的網站適合嗎', text: '我想知道我的網站適不適合做 AEO。' },
    { label: '3 個月免費工程期', text: '請說明 3 個月免費工程期是怎麼運作的。' },
    { label: '合作方案', text: '我想了解 AEO 的合作方案與費用。' },
    { label: '請顧問聯繫我', text: '請安排顧問與我聯繫，謝謝。' },
  ];

  function renderQuick() {
    quick.textContent = '';
    // 已經開始對話就不再顯示引導按鈕，避免佔用空間
    if (state.messages.length > 0) return;
    QUICKS.forEach(function (q) {
      var b = document.createElement('button');
      b.textContent = q.label;
      b.onclick = function () { send(q.text); };
      quick.appendChild(b);
    });
  }

  function updateBadge() {
    if (state.unread > 0 && !state.open) {
      badge.textContent = String(state.unread);
      badge.style.display = 'block';
    } else {
      badge.style.display = 'none';
    }
  }

  // ---------- API ----------
  function load() {
    return fetch(API, { credentials: 'include' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (j) {
        if (!j || !j.data) return;
        var msgs = j.data.messages || [];
        // 只在訊息變多時才重繪，避免每 3 秒閃一次
        if (msgs.length !== state.lastCount) {
          var incoming = msgs.length - state.lastCount;
          if (!state.open && state.lastCount > 0 && incoming > 0) {
            state.unread += incoming;
          }
          state.lastCount = msgs.length;
          state.messages = msgs;
          render();
          renderQuick();
          updateBadge();
        }
        if (j.data.conversation) state.conversationId = j.data.conversation.id;
      })
      .catch(function () { /* 網路暫時失敗不打擾使用者，下一輪會再試 */ });
  }

  function send(text) {
    var content = (text !== undefined ? text : ta.value).trim();
    if (!content || state.sending) return;
    state.sending = true;
    sendBtn.disabled = true;

    // 樂觀顯示：先畫上去，失敗再移除
    state.messages.push({ from: 'visitor', content: content, name: null });
    render();
    if (text === undefined) ta.value = '';
    renderQuick();

    fetch(API, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        message: content,
        conversation_id: state.conversationId,
        landing_url: location.href,
        utm: utm(),
      }),
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, j: j }; }); })
      .then(function (o) {
        if (!o.ok) {
          state.messages.pop();
          render();
          showErr((o.j && o.j.error && o.j.error.message) || '訊息未送出，請稍後再試');
          return;
        }
        if (o.j.data && o.j.data.conversation) state.conversationId = o.j.data.conversation.id;
        state.lastCount = 0;   // 強制下一輪重新同步
        return load();
      })
      .catch(function () {
        state.messages.pop();
        render();
        showErr('連線異常，請稍後再試');
      })
      .finally(function () {
        state.sending = false;
        sendBtn.disabled = false;
      });
  }

  // ---------- 輪詢 ----------
  function startPoll() {
    stopPoll();
    state.timer = setInterval(function () {
      if (document.hidden) return;   // 背景分頁不打 API
      load();
    }, POLL_MS);
  }
  function stopPoll() {
    if (state.timer) { clearInterval(state.timer); state.timer = null; }
  }

  // ---------- 開關 ----------
  function toggle(force) {
    state.open = force !== undefined ? force : !state.open;
    panel.classList.toggle('open', state.open);
    if (state.open) {
      state.unread = 0;
      updateBadge();
      ta.focus();
      load();
    }
    try { sessionStorage.setItem(STORE_KEY, state.open ? '1' : '0'); } catch (e) { /* 隱私模式 */ }
  }

  btn.onclick = function () { toggle(); };
  sendBtn.onclick = function () { send(); };
  ta.onkeydown = function (e) {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); send(); }
  };
  ta.oninput = function () {
    ta.style.height = 'auto';
    ta.style.height = Math.min(90, ta.scrollHeight) + 'px';
  };
  document.addEventListener('visibilitychange', function () {
    if (!document.hidden) load();
  });

  // ---------- 啟動 ----------
  load().then(function () {
    render();
    renderQuick();
    try {
      if (sessionStorage.getItem(STORE_KEY) === '1') toggle(true);
    } catch (e) { /* ignore */ }
    startPoll();
  });
})();
