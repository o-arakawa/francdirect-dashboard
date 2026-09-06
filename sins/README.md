# sins cosmetics — 髪質改善ストレート LP

美容師向け「sins式 髪質改善ストレート」のランディングページです。
ChatGPT広告 → LP → LP内のセミナー動画 → 視聴後にサンプルセット購入ページへ、という **LP内完結** の導線で設計しています。

- 公開URL（main にマージ後）: `https://o-arakawa.github.io/francdirect-dashboard/sins/`
- 本体: `sins/index.html`（CSS / JS も同一ファイルに内包）
- 画像: `sins/assets/`（WebP + JPEG、複数サイズ）

## 差し替え・設定は `index.html` 冒頭の `SINS_LP_CONFIG` だけ

```js
window.SINS_LP_CONFIG = {
  purchaseUrl: 'https://sins.base.shop',   // サンプルセットの購入ページ（BASE → 直販サイトに変わったらここだけ変更）
  lineUrl: '',                             // 相談用の公式LINE URL。空なら LINE 導線は非表示
  contactUrl: '',                          // 集合セミナー等の問い合わせ先（mailto: や フォームURL）。空なら非表示
  video: { type: 'none', src: '', poster: 'assets/…' },  // 下記参照
  unlockAt: 0.9,                           // 動画をここまで視聴したら購入CTAを表示（0.9 = 90%）
  unlockWhenNoVideo: true,                 // 動画未設定のあいだは購入CTAを最初から表示する
  cases: [ … ],                            // 症例カード（写真＋判断項目）。空欄は「動画内で解説」と表示
  testimonials: [ … ],                     // 実在の受講者の声のみ。空のあいだはセクション非表示
};
```

### 動画の設定（ギガファイル便で届いたら）

| type | src に入れる値 | 補足 |
|---|---|---|
| `youtube` | 動画ID（例 `dQw4w9WgXcQ`） | **推奨**。YouTube に「限定公開」でアップロードし、URL の `v=` 以降を入れる |
| `vimeo` | 動画ID（数字） | Vimeo にアップロードした場合 |
| `mp4` | mp4 の URL | 直接ホスティングする場合。GitHub Pages は 100MB 制限があるため、25分の動画はリポジトリに入れず外部ストレージのURLを指定する |
| `none` | 空 | 準備中プレースホルダーを表示 |

視聴率が `unlockAt` に達するか最後まで再生されると、購入セクション（`#purchase-gate`）とページ下部・固定バーの購入ボタンが表示されます。解放状態は `localStorage` に90日間記憶され、再訪時は最初から表示されます。動画には「2倍速で見る（約12分）」ボタンがあります。

### 症例カード（`cases`）

```js
{ title: 'しっかりした癖・ミディアム', before: 'assets/ba4038-before-600.jpg', after: 'assets/ba4038-after-600.jpg',
  chart: 'C', thickness: '普通', history: 'カラー2回', recipe: 'T7 → 顔周り 4.5', reason: '…' }
```

`chart / thickness / history / recipe / reason` は事実が確認できたものだけ入れてください。空欄は「動画内で解説」と表示されます。

### 受講者の声（`testimonials`）

```js
{ quote: '薬剤選定の基準がスタッフ間で揃った', salon: '〇〇（神奈川）', name: '〇〇 様', photo: 'assets/voice-1.jpg' }
```

実在の受講者から許可を得たものだけを入れてください。1件以上入ると自動でセクションが表示されます。

## 表記ルール

- 「縮毛矯正」ではなく **「髪質改善ストレート」** に統一（見出し・CTA・本文）
- 店舗名は「sinsia（シンシア）」、商品・サービス名は「sins」
- 「日本一」「No.1」などの最上級表現は使わない（広告審査対策）

## ローカル確認

```bash
cd sins && python3 -m http.server 8080
# → http://localhost:8080/
```

## 未着の素材（届き次第差し替え）

- セミナー動画（約24〜25分）
- プロ撮影の単体写真 3 枚（`20250213_sins0636 / 9101 / 9056`）は 10MB 超で取得できなかったため未使用。長辺 2400px 程度に縮小したものをいただければヒーロー等に差し替え可能
- 講師プロフィール（美容師歴・得意分野）の確定文言
- 実在の受講者の声
