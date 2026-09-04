#!/usr/bin/env python3
"""
把 contact.html 的假表單接上真正的寄信端點。冪等。

## 修的是什麼

原本：

    <form ... onsubmit="alert('感謝您的訊息！此功能即將開放，請透過 Email
                        聯繫我們。'); return false">

使用者填完姓名、電話、信箱、訊息後按送出，會看到一句「感謝您的訊息」，
但**沒有任何地方收到那則訊息**。表單看起來能用，實際是壞的——這比明白
寫「請寄信到 cs@shell.fans」更糟，因為它讓人以為訊息送出了。

改為 POST /api/contact（shellfans-api 的 /contact），寄到 cs@shell.fans，
Reply-To 設為填表人，客服直接回覆該信即可。

## 加 honeypot

一個 CSS 隱藏、標記 tabindex=-1 與 autocomplete=off 的 website 欄位。
真人看不到也 tab 不到；自動填表的爬蟲會填。後端命中時回 200 假成功——
回錯誤等於告訴對方換個方式再試。

不用 CAPTCHA：那要引入第三方腳本與 cookie，對一個每天幾封的表單，
成本高於效益。

## 送出狀態直接寫在按鈕與訊息區，不用 alert

alert 會擋住整個頁面且無法呈現錯誤細節。改為就地顯示，並在成功後清空
表單——沒清空的話使用者容易重複送出。

用法：python3 scripts/fix-contact-form.py [--check]
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'contact.html')
MARKER = 'sf-contact-wired'

OLD_ONSUBMIT = (
    ''' onsubmit="alert('感謝您的訊息！此功能即將開放，請透過 Email 聯繫我們。');'''
    ''' return false;"'''
)

# 隱藏 honeypot。用 position:absolute + left:-9999px 而不是 display:none——
# 部分爬蟲會跳過 display:none 的欄位，但讀得到位移到畫面外的。
HONEYPOT = (
    '<div aria-hidden="true" style="position:absolute;left:-9999px;top:-9999px;'
    'height:0;width:0;overflow:hidden">'
    '<label for="sf-website">請勿填寫此欄</label>'
    '<input type="text" id="sf-website" name="website" tabindex="-1" autocomplete="off">'
    '</div>'
)

SCRIPT = '''<script data-''' + MARKER + '''="1">
(function () {
  'use strict';
  var form = document.getElementById('email-form-2');
  if (!form) return;
  var btn = form.querySelector('input[type="submit"], button[type="submit"]');
  var note = document.createElement('p');
  note.setAttribute('role', 'status');
  note.style.cssText = 'margin-top:14px;font-size:0.95rem;line-height:1.8;display:none';
  form.appendChild(note);

  function say(msg, ok) {
    note.textContent = msg;
    note.style.color = ok ? '#2C9A8A' : '#C2503A';
    note.style.display = 'block';
  }
  function busy(on) {
    if (!btn) return;
    btn.disabled = on;
    if (btn.tagName === 'INPUT') {
      if (on) { btn.dataset.sfLabel = btn.value; btn.value = btn.dataset.wait || '寄送中...'; }
      else if (btn.dataset.sfLabel) { btn.value = btn.dataset.sfLabel; }
    }
  }

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    note.style.display = 'none';
    var fd = new FormData(form);
    var payload = {};
    fd.forEach(function (v, k) { payload[k] = typeof v === 'string' ? v : ''; });
    busy(true);
    fetch('https://shell.fans/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
      credentials: 'omit'
    })
      .then(function (r) { return r.json().then(function (j) { return { ok: r.ok, body: j }; }); })
      .then(function (o) {
        if (o.ok && o.body && o.body.ok) {
          say('已送出，我們會盡快與您聯繫。', true);
          form.reset();
          // 表單送出是真實的商業意圖，值得記錄。AI 推薦歸因會由
          // sf-analytics.js 自動附上，這裡不必重複帶。
          try { window.sfAnalytics && window.sfAnalytics.track('contact_submit', {}); } catch (e) {}
        } else {
          // 後端回的是 RFC 9457 problem+json，detail 已是可直接顯示的中文
          say((o.body && o.body.detail) || '送出失敗，請稍後再試，或直接來信 cs@shell.fans。', false);
        }
      })
      .catch(function () {
        say('連線異常，請稍後再試，或直接來信 cs@shell.fans。', false);
      })
      .finally(function () { busy(false); });
  });
})();
</script>'''


def main():
    check = '--check' in sys.argv
    src = open(PAGE, encoding='utf-8').read()

    if MARKER in src:
        print('待處理 0 頁（已接線）')
        return

    if OLD_ONSUBMIT not in src:
        raise SystemExit(
            'contact.html 找不到預期的 onsubmit alert —— 表單可能已被改動，'
            '請先人工確認再跑本腳本')

    out = src.replace(OLD_ONSUBMIT, '', 1)

    # honeypot 放在表單開頭
    m = re.search(r'(<form id="email-form-2"[^>]*>)', out)
    if not m:
        raise SystemExit('找不到 email-form-2 的開始標籤')
    out = out[:m.end()] + HONEYPOT + out[m.end():]

    # 腳本放在 </body> 之前
    b = out.rfind('</body>')
    if b < 0:
        raise SystemExit('找不到 </body>')
    out = out[:b] + SCRIPT + '\n' + out[b:]

    # 產出即驗證
    if 'alert(' in out.split('<form id="email-form-2"')[1][:600]:
        raise SystemExit('表單仍帶 alert')
    if out.count('name="website"') != 1:
        raise SystemExit('honeypot 數量不是 1')
    if out.count(MARKER) < 1:
        raise SystemExit('冪等標記未寫入')
    for tag in ('form', 'div', 'script'):
        if out.count(f'<{tag}') - out.count(f'</{tag}>') != \
           src.count(f'<{tag}') - src.count(f'</{tag}>'):
            raise SystemExit(f'{tag} 標籤平衡被改變')

    if not check:
        open(PAGE, 'w', encoding='utf-8').write(out)
    print(f'{"待處理" if check else "已處理"} contact.html'
          f'（移除 alert、加 honeypot、接上 /api/contact）')


if __name__ == '__main__':
    main()
