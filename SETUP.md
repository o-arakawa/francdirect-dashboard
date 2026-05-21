FrancDirect — Meta 広告ダッシュボード セットアップ
⚠️ まず最初に：トークンを再生成してください
スクリーンショットや会話にトークンが表示された場合、
セキュリティのためすぐに新しいトークンを発行してください。
（古いトークンは使わない）

① 短期トークン → 長期トークン（60日）に変換
1. 新しい短期トークンを取得
Meta for Developers → マーケティングAPI → ツール
権限: ads_read + read_insights にチェック → 「トークンを取得」

2. ブラウザで以下の URL を開く
https://graph.facebook.com/v21.0/oauth/access_token?grant_type=fb_exchange_token&client_id=928434486895785&client_secret=【App Secret】&fb_exchange_token=【短期トークン】
App Secret の確認場所:
Meta for Developers → アプリの設定 → ベーシック → 「アプリシークレット」を表示

3. レスポンスから長期トークンを取得
{
  "access_token": "EAABsb...(長い文字列)",
  "token_type": "bearer",
  "expires_in": 5183944
}
この access_token の値を GitHub Secret に登録します。

② GitHub Secrets に登録する値
リポジトリ → Settings → Secrets and variables → Actions → New repository secret

Secret 名	登録する値
META_ACCESS_TOKEN	上で取得した長期トークン
META_AD_ACCOUNT_ID	727273939454651
META_CAMPAIGN_ID	120243061348860707
META_CV_ACTION	lead（myasp/LINE リードの場合）
SHEET_CSV_URL	MyASP/LINE CV を集計した Google Sheets の CSV 公開URL（任意）
GAS_YOUTUBE_URL	YouTube/Google Ads 側の GAS Web App URL（任意）
③ GitHub Pages を有効化
Settings → Pages → Source: Deploy from a branch → Branch: main / root

URL: https://{username}.github.io/{repo}/dashboard.html

④ 動作テスト
Actions タブ → 「Fetch Meta Ads Data — FrancDirect」→「Run workflow」

data.json が更新されれば成功。

GitHub Actions の定期実行は UTC 基準です。現在の設定 0 0,6,12,18 * * * は、日本時間では 9:00 / 15:00 / 21:00 / 3:00 頃に実行されます。

アプリのモードについて
現在「開発モード」になっています。自分のアカウントの広告データは
開発モードでも取得できますが、他のユーザーのデータを取得する場合は
「ライブモード」への切り替えとアプリレビューが必要です。

トークン有効期限について
長期トークンは 60日で失効 します。
失効前に同じ手順で再発行し、GitHub Secret を更新してください。

ファイル構成
.
├── dashboard.html              ← GitHub Pages で公開
├── data.json                   ← Actions が 1日4回更新
├── fetch_meta.py               ← Meta API 取得スクリプト
├── .github/workflows/
│   └── fetch-meta-ads.yml      ← スケジュール設定
└── SETUP.md                    ← このファイル
