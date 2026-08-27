# MCP Gap Analysis

**日期**：2026-08-26（2026-08-27 補查證）
**觸發**：Is Agentic 稽核（shell.fans，51/100）
**結論**：**不實作 `/.well-known/mcp`**。ShellFans 沒有 MCP server，稽核的判定是誤判。

---

## 稽核怎麼說

| 項目 | 層級 | 結果 | 稽核原文 |
|---|---|---|---|
| MCP server / manifest | Recommended | Partial | "First-party MCP server published; missing live handshake" |

任務說明據此要求：「Inspect the existing MCP implementation and package
`@shell-mcp/core`. Do not create a duplicate MCP architecture.」

## 查證結果：沒有這個東西

| 查什麼 | 怎麼查 | 結果 |
|---|---|---|
| `@shell-mcp/core` 套件（本機） | `grep -rl '@shell-mcp' ~/work ~/workspace`（排除 node_modules） | 找不到 |
| `@shell-mcp/core` 套件（npm） | `curl registry.npmjs.org/@shell-mcp%2Fcore` | **存在，但不是 ShellFans 的**（見下節） |
| MCP server 實作 | 六個程式庫搜尋 `modelcontextprotocol`／`McpServer`／`StreamableHTTP`（saas_womm、shellfans-agent、backend、continuity-api、gateway、business-api） | 全部無 |
| 站上內容提及 MCP | 全站 `*.html`／`*.txt`／`*.md` 搜尋 `MCP`／`Model Context Protocol` | 0 處 |
| 線上內容提及 MCP | `curl` 首頁、`/llms.txt`、`/llms-full.txt`、`/what-is-shellfans`、`/aeo` | 各 0 次 |
| `/.well-known/mcp` | `curl` | 稽核當下為 302（soft-404 導首頁），現為 404 |

本機的六個程式庫完全沒有 MCP server 實作，站上也零處提及。至於 npm 上那個同名套件，見下節。

## 2026-08-27 補查：該套件確實存在，但屬於別人

上一版寫「npm 上不存在」是錯的，重新查證後更正。`@shell-mcp/core` 在 npm
上確實存在，但**與 ShellFans 無關**：

```
name:         @shell-mcp/core
description:  Core session management, safety guardrails, and audit logging
              for shell-mcp
maintainers:  hypotext
repository:   github.com/psdlabs/shell-mcp
keywords:     mcp, shell, terminal, session, pty, cli
created:      2026-03-31
license:      MIT
```

那是 **psdlabs** 發布的、用於 shell/terminal/PTY session 的 MCP server。
ShellFans（唄粉智能科技股份有限公司）從未發布、貢獻或使用該套件，
兩者唯一的共同點是名稱裡都有 "shell"。

掃描器把它判為 ShellFans 的 first-party MCP server，是對品牌名做了
子字串比對。

### 這讓「照著實作」變成危險而不只是錯誤

先前的結論是「不能發布指向不存在服務的 manifest」。查證之後結論更強：

在 `/.well-known/mcp` 指向 `@shell-mcp/core`，等於以 ShellFans 的名義
把 agent 導向一個**可以在主機上開 shell session 的第三方工具**。任何
信任 shell.fans 網域而據此連線的 agent，會取得一組 ShellFans 從未提供、
也無法為其安全性負責的能力。

這不是分數問題，是把別人的遠端執行工具掛上自家品牌背書。

## 誤判可能的來源

**1. 舊的 soft-404 行為。**
稽核執行時，shell.fans 對任何未知路徑都回 302 導向首頁。掃描器若探測
`/.well-known/mcp`、`/mcp`、`/sse`，拿到的是 302 → 200（首頁 HTML）。
若判定邏輯是「非 404 即視為存在」，就會得出「已發布但沒有握手」的結論——
這正好對應 "published; missing live handshake" 的措辭。

access log 支持這個推測：`/mcp`（28 次）、`/mcp/`（20 次）、`/api/mcp`（20 次）、
`/sse`（27 次）都有被探測，全部回 302。

**2. 名稱混淆。**
ShellFans 的 Dify 工作流中有名為 `shellfans_mcp`、`shellfans_threads_mcp`、
`shellfans_mcp_v4` 的工具供應者。那些是 ShellFans **消費**外部 MCP 工具
（xpoz.ai、Apify）的設定，是 client 端，不對外提供服務，也不在公開網域上。

無論來源為何，結論一樣：**沒有 first-party MCP server 可供發現。**

## 為什麼不順手蓋一個

**1. 發現文件不能指向不存在的服務。**
`/.well-known/mcp` 的用途是告訴 client「MCP endpoint 在哪、支援什麼傳輸方式」。
沒有 endpoint 就發布 manifest，等於製造一個 100% 會失敗的握手。
對 agent 而言，這比 404 更糟——404 是明確的「沒有」，
壞掉的 manifest 是「有，但你連不上」，會導致重試與錯誤歸因。

任務說明本身也要求「Verify the endpoint with an actual MCP client or
protocol-level test」。沒有 server 就無從驗證，這一項本質上無法達成。

**2. 沒有可暴露的工具。**
MCP server 的價值在於暴露工具（tools）與資源（resources）給 agent 呼叫。
ShellFans 目前沒有任何面向第三方的可呼叫能力：
沒有公開寫入 API，唯一的運算型端點（ShellFans Chat）每次呼叫都會實際
產生語言模型與外部資料來源的成本，且僅有每日 2 次的匿名額度。
把它包成 MCP tool 等於開放一個「每次呼叫都花錢、且無法計費」的介面。

**3. 認證缺口。**
任何有意義的 ShellFans MCP server 都需要辨識呼叫者（配額、計費、資料範圍）。
而 ShellFans 目前沒有面向機器的授權機制——見
[oauth-gap-analysis.md](./oauth-gap-analysis.md)。MCP 的授權規範建立在
OAuth 2.1 之上；在授權模型確立之前做 MCP，順序是反的。

## 若未來要做，先決條件的順序

1. **先有可暴露的能力。** 一個 MCP server 只有在「有工具可以呼叫」時才有意義。
   最可能的第一批候選是唯讀的：AEO/GEO 掃描結果查詢、備份工作狀態查詢。
2. **再有機器授權。** OAuth 2.1 + PKCE，含 scope 與後端強制檢查。
3. **然後才是傳輸層。** Streamable HTTP（現行建議），
   `/.well-known/mcp` 描述 endpoint 與能力。
4. **最後是驗證。** 用真實 MCP client 做完整握手測試，
   不是只確認 manifest 回 200。

跳過 1、2 直接做 3，得到的是一個沒有東西可呼叫、也不知道呼叫者是誰的端點。

## 現況如何對外說明

`/developers` 明文寫出：

> ShellFans 目前沒有發布 Model Context Protocol server，也沒有
> `/.well-known/mcp` 描述檔。內部產品在某些工作流中**使用** MCP 工具，
> 但那是消費端，不對外提供服務。

`/llms.txt` 的 "What an agent can and cannot do programmatically" 段落同樣載明。

改成真 404 之後（2026-08-26 已上線），`/.well-known/mcp`、`/mcp`、`/sse` 都會明確回 404，
掃描器不會再從 302 推論出「已發布」——這本身就修正了誤判的成因。

## 對分數的影響

此項目前是 Partial（部分得分），基於誤判。改成真 404 後，
**重新掃描很可能會降為 Failed**，因為誤判的依據消失了。

這是預期中的、正確的變化：ShellFans 確實沒有 MCP server，
分數應該反映事實。用一個壞掉的 manifest 維持虛假的部分得分，
會讓真正嘗試連線的 agent 付出代價。
