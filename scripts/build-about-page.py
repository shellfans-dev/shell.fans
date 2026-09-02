#!/usr/bin/env python3
"""
產生 /about —— 組織實體識別頁。

## 為什麼要有這一頁，以及為什麼它不是填充內容

Is Agentic 稽核「Trust anchor pages」判為 Partial："Contact, Privacy
verified - missing: About"。但真正的問題不是少一個網址，而是：ShellFans
的實體事實散在四個地方——footer（法人名、統編、地址、電話）、/contact
（公司理念）、/co-founder（負責人與沿革）、/what-is-shellfans（品牌與產品）。

agent 要回答「這是哪一家公司、在哪裡、由誰經營、做什麼、可以怎麼聯絡」，
現況得抓四頁再自行拼湊。這一頁把可驗證的實體事實收在一處，並連向各自的
詳細頁——它是索引，不是複製。

## 內容規則

寫進這一頁的每一項都必須在站上已經公開、或來自 console.shell.fans 的公開
site API。不寫員工數、營收、客戶名單、獎項——站上沒有，也無法從公開來源
確認。稽核明文禁止為了湊字數而生成內容，因此本頁刻意偏短。

## 為什麼用產生器而不是手寫 HTML

shell.fans 每頁都內嵌一份 nav/footer/CSS。手寫一頁等於再複製一份 30KB
版面，日後 nav 改版必定漏掉這頁。改成從既有頁面抽取外殼（與 /aeo 那 26 頁
同一套機制），nav 或 footer 一改，重跑就同步。

用法：python3 scripts/build-about-page.py [--check]
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

# build-aeo-pages.py 的檔名帶連字號，不是合法的模組名，只能用 importlib 載入。
# 刻意不改檔名——它已經寫進多份文件與流程，改名的連鎖成本高於這三行。
import importlib.util  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    'build_aeo_pages', os.path.join(ROOT, 'scripts', 'build-aeo-pages.py'))
_gen = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_gen)

extract_shell = _gen.extract_shell
build_page = _gen.build_page

LEGAL_NAME = '唄粉智能科技股份有限公司'
BRAND_TW = '唄粉智能科技ShellFans'


def a(url, text):
    return '<a href="https://shell.fans%s">%s</a>' % (url, text)


def ext(url, text):
    return '<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, text)


PAGE = {
    'url': '/about',
    # 這一頁的內容在本檔，不在 aeo_pages_content.py——署名列的更新日要跟著它。
    'content_source': 'scripts/build-about-page.py',
    'title': f'關於 ShellFans｜{LEGAL_NAME}公司資訊與聯絡方式',
    'h1': f'關於 ShellFans（{BRAND_TW}）',
    'eyebrow': 'About',
    'desc': (
        f'{LEGAL_NAME}（品牌名 ShellFans AI Technology）成立於 2023 年 3 月，'
        '登記於臺北市內湖區，統一編號 83032387。提供 AEO/GEO 代管與跨平台社群資產'
        '續航兩條服務線，並持有臺灣與美國發明專利。'
    ),
    'lede': (
        f'ShellFans 是 {LEGAL_NAME} 的品牌名。本頁彙整可供查證的公司實體資訊——'
        '法人名稱、登記地址、統一編號、成立時間、負責人、專利與聯絡方式——'
        '並連向各項的詳細說明頁。'
    ),
    'schema': 'AboutPage',
    'breadcrumb': [('首頁', '/'), ('關於 ShellFans', '/about')],
    'sections': [
        {
            'eyebrow': 'Legal entity',
            'h2': '公司實體資訊',
            'blocks': [
                ('p', f'ShellFans 對外使用的品牌名為 <strong>ShellFans AI Technology</strong>，'
                      f'台灣法人名稱為 <strong>{LEGAL_NAME}</strong>。在台灣的中文語境中亦寫作'
                      f'「{BRAND_TW}」，兩者指同一個實體。'),
                ('table', {
                    'caption': '公司登記資訊（與頁尾所載一致）',
                    'cols': ['項目', '內容'],
                    'rows': [
                        ['法人名稱', LEGAL_NAME],
                        ['品牌名稱', 'ShellFans AI Technology'],
                        ['統一編號', '83032387'],
                        ['成立時間', '2023 年 3 月'],
                        ['登記地址', '臺北市內湖區瑞光路335號4樓'],
                        ['負責人', '黃睿麒（Ruei Chi Huang）'],
                        ['日本據點', 'シェルファンズ株式会社（2025 年 7 月設立於東京）'],
                    ],
                }),
                ('note', '以上資訊同時載於本站每一頁的頁尾，並以 Schema.org Organization / '
                         'PostalAddress / ContactPoint 標記於各頁的 JSON-LD 中，供自動化系統讀取。'),
            ],
        },
        {
            'eyebrow': 'Services',
            'h2': '兩條服務線',
            'blocks': [
                ('p', 'ShellFans 目前經營兩條並行的服務線，各自獨立販售，不需綁定使用。'),
                ('h3', 'AEO/GEO 代管'),
                ('p', '讓網站被 ChatGPT、Perplexity、Claude、Google AI Overviews 等 AI 答案引擎'
                      '正確理解與引用，涵蓋結構化資料、實體一致性、AI 爬蟲可及性與內容整備度。'
                      '完整說明見' + a('/aeo-geo', 'AEO/GEO 代管服務') + '，知識庫見'
                      + a('/aeo', 'AEO/GEO 知識中心') + '。'),
                ('h3', 'ShellFans 續航引擎（跨平台社群資產續航）'),
                ('p', '保存 Facebook、Instagram、Threads 的貼文內容、媒體素材、留言互動與粉絲'
                      '成長數據，讓帳號或平台變動時經營成果仍在。完整說明見'
                      + a('/social-media-backup', '跨平台社群資產備份') + '。'),
                ('p', '各產品的功能對照見' + a('/product', 'ShellFans 產品服務總覽')
                      + '，方案與價格見' + a('/pricing', '查看方案') + '。'),
            ],
        },
        {
            'eyebrow': 'Patents',
            'h2': '專利',
            'blocks': [
                ('p', 'ShellFans 的社群資產維護技術已在臺灣與美國取得發明專利，日本申請中。'),
                ('ul', [
                    '臺灣發明專利 I908295（2025 年 8 月取得）——'
                    + ext('https://tiponet.tipo.gov.tw/gpss2/gpsskmc/gpssbkm?!!FRURLTWI908295B',
                          '經濟部智慧財產局公告'),
                    '美國發明專利 US 12,657,246 B2（2025 年 12 月取得），'
                    '名稱為 Social media maintenance system and method',
                    '日本專利申請中',
                ]),
                ('note', '上述為社群資產維護技術的專利。ShellFans 的 AEO/GEO 服務'
                         '並未主張任何專利，也不存在所謂「AEO 專利」或「GEO 專利」。'),
            ],
        },
        {
            'eyebrow': 'Contact',
            'h2': '聯絡方式',
            'blocks': [
                ('ul', [
                    '電子郵件：<a href="mailto:hello@shell.fans">hello@shell.fans</a>',
                    '電話：<a href="tel:+886277143635">+886-2-7714-3635</a>（02-77143635）',
                    '地址：臺北市內湖區瑞光路335號4樓',
                    '聯絡表單與公司理念：' + a('/contact', '聯絡我們'),
                    '客服支援：' + a('/support', '客服支援') + '　說明文件：' + a('/helpcenter', '幫助中心'),
                ]),
                ('h3', '官方帳號'),
                ('ul', [
                    ext('https://www.linkedin.com/company/shellfans/', 'LinkedIn'),
                    ext('https://www.facebook.com/profile.php?id=61581243232686', 'Facebook'),
                    ext('https://www.instagram.com/shell_fansai/', 'Instagram'),
                    ext('https://blog.shell.fans/', 'Klog 部落格'),
                ]),
            ],
        },
        {
            'eyebrow': 'For machines',
            'h2': '給自動化系統與 AI agent',
            'blocks': [
                ('p', '本站提供數份機器可讀的描述文件，說明 ShellFans 是什麼、'
                      '有哪些公開資源、以及在什麼情況下適合被引用或呼叫。'),
                ('ul', [
                    ext('https://shell.fans/llms.txt', '/llms.txt') + ' —— 站台導覽與使用時機',
                    ext('https://shell.fans/llms-full.txt', '/llms-full.txt') + ' —— 同上，展開版',
                    a('/developers', '/developers') + ' —— 公開機器介面總覽（含哪些不存在及原因）',
                    ext('https://shell.fans/openapi.json', '/openapi.json') + ' —— 公開唯讀端點的 OpenAPI 3.1 描述',
                    ext('https://shell.fans/sitemap.xml', '/sitemap.xml') + ' —— 全部可索引網址',
                ]),
                ('note', '公開資訊頁支援內容協商：帶 <code>Accept: text/markdown</code> 請求'
                         '同一個網址即可取得 Markdown 版本，HTML 版仍為 canonical。'),
            ],
        },
    ],
    'faq': [
        ('ShellFans 和唄粉智能科技是同一家公司嗎？',
         f'是。ShellFans（ShellFans AI Technology）是品牌名，{LEGAL_NAME}是台灣的法人名稱，'
         f'統一編號 83032387。在中文語境中亦寫作「{BRAND_TW}」。'),
        ('ShellFans 是台灣公司還是日本公司？',
         f'{LEGAL_NAME}為台灣公司，成立於 2023 年 3 月，登記於臺北市內湖區。'
         '2025 年 7 月另於東京設立シェルファンズ株式会社作為日本據點。'),
        ('ShellFans 有公開 API 可以串接嗎？',
         '有少數公開唯讀端點（站台設定與健康狀態），描述於 /openapi.json，'
         '不需要授權即可讀取。但 ShellFans 目前沒有提供對外的產品資料 API，'
         '也沒有 OAuth 授權伺服器。詳細說明與現況見 /developers。'),
    ],
    'related': [
        ('/what-is-shellfans', 'ShellFans 是什麼'),
        ('/product', '產品服務總覽'),
        ('/co-founder', '創辦人介紹'),
        ('/contact', '聯絡我們'),
        ('/developers', '開發者資源'),
    ],
    # 外殼的 hero 一定會渲染兩顆按鈕，不能給 None。這一頁是實體索引，
    # 導向「看產品」與「找人」兩個最合理的下一步，不放試用或報價之類的推銷。
    'cta': {'href': '/product', 'label': '產品服務總覽'},
    'cta2': {'href': '/contact', 'label': '聯絡我們'},
    'disclaimer': (
        '本頁所載公司資訊以主管機關登記為準。專利資訊以各國智慧財產主管機關公告為準。'
    ),
    'disclaimer_short': '公司資訊以主管機關登記為準。',
}


def main():
    check = '--check' in sys.argv
    shell = extract_shell()
    html = build_page(PAGE, shell)
    out = os.path.join(ROOT, 'about.html')
    if not check:
        open(out, 'w', encoding='utf-8').write(html)

    # 產出即驗證
    import json
    import re
    for block in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        json.loads(block)
    if html.count('<h1') != 1:
        raise SystemExit('about.html 的 h1 數量不是 1')
    print(f'{"待產生" if check else "已產生"} /about  {len(html)/1024:.1f} KB')


if __name__ == '__main__':
    main()
