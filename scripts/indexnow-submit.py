#!/usr/bin/env python3
"""
IndexNow 推送 —— 內容變動後主動通知搜尋引擎。

## 為什麼要做這個

Bing、Yandex、Seznam 支援 IndexNow 協定：網站可以主動告知「這些網址有變動」，
不必等爬蟲自己回來。對 AEO 特別有意義的是 **Microsoft Copilot 走 Bing 的索引** ——
被 Bing 收錄的速度，直接影響 Copilot 何時能引用你。

Google 不支援 IndexNow，仍靠 sitemap 與自然抓取。

## 金鑰

`/{key}.txt` 必須公開可讀且內容就是那把金鑰本身 —— 這是 IndexNow 驗證網站
所有權的方式。因此這把金鑰**本來就是公開的**，放進版控是正確的，不是外洩。

## 用法

    python3 scripts/indexnow-submit.py              # 推送 AEO 叢集 + 首頁
    python3 scripts/indexnow-submit.py --all        # 推送 sitemap 全部
    python3 scripts/indexnow-submit.py --dry-run    # 只顯示會推送什麼

## 注意

IndexNow 是「內容有變動」的通知，不是「請重新索引全站」的請求。
每次改動後推送相關網址即可；無意義地反覆推送整站只會降低訊號價值。
"""

import glob
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = 'shell.fans'
ENDPOINT = 'https://api.indexnow.org/indexnow'


def find_key():
    """金鑰檔是站根目錄下的 32 位十六進位 .txt，內容與檔名相同。"""
    for path in glob.glob(os.path.join(ROOT, '*.txt')):
        name = os.path.basename(path)[:-4]
        if not re.fullmatch(r'[0-9a-f]{32}', name):
            continue
        with open(path, encoding='utf-8') as f:
            if f.read().strip() == name:
                return name
    raise SystemExit(
        '找不到 IndexNow 金鑰檔。建立方式：\n'
        "  KEY=$(python3 -c 'import secrets;print(secrets.token_hex(16))')\n"
        '  echo "$KEY" > "$KEY.txt"\n'
        '  sudo install -m 664 "$KEY.txt" "/var/www/shell.fans/$KEY.txt"',
    )


def sitemap_urls():
    with open(os.path.join(ROOT, 'sitemap.xml'), encoding='utf-8') as f:
        return re.findall(r'<loc>(.*?)</loc>', f.read())


def main():
    dry = '--dry-run' in sys.argv
    everything = '--all' in sys.argv

    key = find_key()
    urls = sitemap_urls()
    if not everything:
        urls = [u for u in urls
                if '/aeo' in u or u == f'https://{HOST}/' or u.endswith('/what-is-shellfans')]

    payload = {
        'host': HOST,
        'key': key,
        'keyLocation': f'https://{HOST}/{key}.txt',
        'urlList': urls,
    }

    print(f'金鑰 /{key}.txt　·　推送 {len(urls)} 條 URL')
    for u in urls[:8]:
        print('  ', u)
    if len(urls) > 8:
        print(f'   ...（其餘 {len(urls) - 8} 條）')

    if dry:
        print('\n--dry-run，未送出')
        return

    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode('utf-8'),
        headers={'Content-Type': 'application/json; charset=utf-8'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        # 200 = 已接受並處理；202 = 已接受，金鑰驗證中
        print(f'\nHTTP {res.status} —— {"已接受" if res.status in (200, 202) else "未預期的回應"}')


if __name__ == '__main__':
    main()
