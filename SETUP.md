# FrancDirect — Meta 広告ダッシュボード セットアップ

---

## ⚠️ まず最初に：トークンを再生成してください

スクリーンショットや会話にトークンが表示された場合、
セキュリティのため**すぐに新しいトークンを発行**してください。
（古いトークンは使わない）

---

## ① 短期トークン → 長期トークン（60日）に変換

### 1. 新しい短期トークンを取得

Meta for Developers → マーケティングAPI → ツール  
権限: `ads_read` + `read_insights` にチェック → 「トークンを取得」

### 2. ブラウザで以下の URL を開く

```
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=928434486895785&client_secret=【App Secret】&fb_exchange_token=【短期トークン】
```

**App Secret の確認場所:**  
Meta for Developers → アプリの設定 → ベーシック → 「アプリシークレット」を表示

### 3. レスポンスから長期トークンを取得

```json
{
  "access_token": "EAABsb...(長い文字列)",
  "token_type": "bearer",
  "expires_in": 5183944
}
```

この `access_token` の値を GitHub Secret に登録します。

---

## ② GitHub Secrets に登録する値

リポジトリ → Settings → Secrets and variables → Actions → New repository secret

| Secret 名 | 登録する値 |
|---|---|
| `META_ACCESS_TOKEN` | 上で取得した長期トークン |
| `META_AD_ACCOUNT_ID` | `727273939454651` |
| `META_CAMPAIGN_ID` | `120243061348860707` |
| `META_CV_ACTION` | `lead`（myasp/LINE リードの場合） |
| `SHEET_CSV_URL` | MyASP/LINE CV を集計した Google Sheets の CSV 公開URL（任意） |
| `GAS_YOUTUBE_URL` | YouTube/Google Ads 側の GAS Web App URL（任意） |

---

## ③ GitHub Pages を有効化

Settings → Pages → Source: `Deploy from a branch` → Branch: `main` / root

URL: `https://{username}.github.io/{repo}/dashboard.html`

---

## ④ 動作テスト

Actions タブ → 「Fetch Meta Ads Data — FrancDirect」→「Run workflow」

`data.json` が更新されれば成功。

GitHub Actions の定期実行は UTC 基準です。現在の設定 `0 0,6,12,18 * * *` は、日本時間では 9:00 / 15:00 / 21:00 / 3:00 頃に実行されます。

---

## ⑤ ダッシュボード更新時に反映するファイル

通常の画面更新で GitHub に反映するのは以下です。

| ファイル | 用途 |
|---|---|
| `dashboard.html` | GitHub Pages で表示する本体画面 |
| `goals.json` | 目標CPA / CPM / CPC / CTR / CV数 / 計測乖離率 |
| `fetch_meta.py` | Meta API と GAS から `data.json` を作る取得スクリプト |
| `github.gs` | GAS 側コードの控え。Apps Script の `github.gs` と同じ内容にする |

`francdirect-dashboard-latest-YYYYMMDD.zip` は作業用の予備です。GitHub にはアップしなくてOKです。

---

## ⑥ PMO / マーケティング推進部ダッシュボード

`dashboard.html` には、広告数値を見るだけでなく、改善アクションまで落とし込むための
PMO ブロックを追加しています。

組織設計:

```
PMO
└─ マーケティング推進部
    ├─ ①戦略設計チーム
    ├─ ②広告運用チーム
    ├─ ③広告CR制作チーム
    ├─ ④LP制作・改善チーム
    └─ ⑤数値分析・レポートチーム
```

表示される内容:

- 目標との差分
- PMO判断
- 勝ち訴求 / 負け訴求
- 広告運用チームへの指示
- 広告CR制作チームへの制作指示
- LP制作・改善チームへの改善指示
- 数値分析・レポートチームへの確認項目

目標値を変える場合は `goals.json` を編集します。

例:

```json
{
  "daily": {
    "mail": 10,
    "cpa": 1500,
    "cpm": 1600,
    "cpc": 45,
    "ctr": 3.5,
    "purchase": 1,
    "cv_gap_rate": 0.25
  }
}
```

`cv_gap_rate` は、Meta 管理画面CVとスプレッドシートN列（メルマガ登録者）の許容乖離率です。

---

## アプリのモードについて

現在「開発モード」になっています。自分のアカウントの広告データは
開発モードでも取得できますが、他のユーザーのデータを取得する場合は
「ライブモード」への切り替えとアプリレビューが必要です。

---

## トークン有効期限について

長期トークンは **60日で失効** します。  
失効前に同じ手順で再発行し、GitHub Secret を更新してください。

---

## ファイル構成

```
.
├── dashboard.html              ← GitHub Pages で公開
├── goals.json                  ← 目標数値
├── data.json                   ← Actions が 1日4回更新
├── fetch_meta.py               ← Meta API 取得スクリプト
├── github.gs                   ← GAS 側コードの控え
├── .github/workflows/
│   └── fetch-meta-ads.yml      ← スケジュール設定
└── SETUP.md                    ← このファイル
```
