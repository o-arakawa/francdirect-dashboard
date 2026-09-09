/* =====================================================================
   ★ 設定はこのファイルだけ書き換えれば OK です（sins 髪質改善ストレート LP）
   ---------------------------------------------------------------------
   ・文字は必ず「半角の ' ' （シングルクォート）」で囲みます
   ・各行の末尾の「,（カンマ）」は消さないでください
   ・保存は UTF-8 のまま（Windows のメモ帳なら「名前を付けて保存」→ 文字コード UTF-8）
   ・書き換えたらブラウザで再読み込み（Ctrl+F5 / Cmd+Shift+R）して確認
   ===================================================================== */
window.SINS_LP_CONFIG = {
  purchaseUrl: 'https://sins.base.shop',   // サンプルセット購入ページ（BASE）。直販サイトに変わったらここを変更
  lineUrl: '',                             // 公式LINEのURL。空なら LINE 導線は表示しない
  contactUrl: '',                          // 集合セミナー等の問い合わせ先（例 'mailto:info@example.com'）。空なら購入ページ内の問い合わせを案内
  // ▼ 動画（YouTube の「限定公開」を推奨）。1本だけなら { … } を1つにする。type は全部同じ種類にそろえる
  videos: [
    { title: '髪質改善ストレート セミナー', note: '薬剤選定・施術の流れ（経営者目線パートあり）', type: 'youtube', src: 'fIy8MAHXpNM' },
    { title: '髪質改善 セミナー',           note: '経営者目線パートあり',                          type: 'youtube', src: 'zxhF30iWFDE' }
  ],
  //   type: 'youtube' → src は動画ID（URL の v= の後ろ、youtu.be/ の後ろ）
  //   type: 'vimeo'   → src は動画ID（数字） / type: 'mp4' → src は動画のURL、poster: 'assets/…' で再生前の画像
  //   動画をいったん外すときは videos: [] にする（購入ボタンが最初から表示されます）
  unlockRule: 'any',                       // 購入案内を出す条件： 'any' = どれか1本を視聴完了 / 'all' = 全部 / 'first' = 1本目
  unlockAt: 0.9,                           // 視聴率がこの値に達したら購入CTAを表示（0.9 = 90%）
  unlockWhenNoVideo: true,                 // 動画が未設定の間は購入CTAを最初から表示する（この状態は端末に保存しない）
  unlockTtlDays: 90,                       // 視聴完了の記憶を保持する日数
  // ▼ 施術例（ビフォーアフター）。before / after は assets 内の画像、ratio は写真の縦横比（幅/高さ）
  //    chart / thickness / history / recipe / reason は事実が確認できたものだけ入れる（空欄は「動画内で解説」と表示）
  cases: [
    { title: 'ミディアム（黒髪）',            before: 'assets/case1-before-800.jpg', after: 'assets/case1-after-800.jpg', ratio: '1/1',      chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ロング（ダークブラウン）',      before: 'assets/case2-before-800.jpg', after: 'assets/case2-after-800.jpg', ratio: '1/1',      chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ミディアムロング（ブラウン）',  before: 'assets/case3-before-800.jpg', after: 'assets/case3-after-800.jpg', ratio: '1048/1560', chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ミディアム（ブラウン）',        before: 'assets/case4-before-800.jpg', after: 'assets/case4-after-800.jpg', ratio: '1/1',      chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ロング（明るめのブラウン）',    before: 'assets/case5-before-800.jpg', after: 'assets/case5-after-800.jpg', ratio: '986/1661', chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ミディアム（ブラウン）',        before: 'assets/case6-before-800.jpg', after: 'assets/case6-after-800.jpg', ratio: '1/1',      chart: '', thickness: '', history: '', recipe: '', reason: '' }
  ],
  price: '13,200円（税込）',                // サンプルセットの価格表記。空文字にすると価格の行が非表示になる
  profile: { name: '菅原 寛人', romaji: 'Hiroto Sugawara', role: 'sins cosmetics ／ 現役美容師（sinsia）' },
  testimonials: []                         // 実在の受講者の声のみ。例: { quote: '…', salon: '〇〇（神奈川）', name: '〇〇 様', photo: 'assets/voice-1.jpg' }
};
