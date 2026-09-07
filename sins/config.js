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
  video: {
    type: 'none',                          // 'youtube' | 'vimeo' | 'mp4' | 'none'
    src: '',                               // youtube: 動画ID / vimeo: 動画ID / mp4: 動画URL
    poster: 'assets/iron-1600.jpg'         // 再生前に表示する画像（mp4 のみ）
  },
  unlockAt: 0.9,                           // 視聴率がこの値に達したら購入CTAを表示（0.9 = 90%）
  unlockWhenNoVideo: true,                 // 動画が未設定の間は購入CTAを最初から表示する（この状態は端末に保存しない）
  unlockTtlDays: 90,                       // 視聴完了の記憶を保持する日数
  cases: [
    { title: 'ミディアム・うねりの強い髪', before: 'assets/ba4038-before-600.jpg', after: 'assets/ba4038-after-600.jpg', chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ロング・広がりやすい髪',     before: 'assets/ba4032-before-600.jpg', after: 'assets/ba4032-after-600.jpg', chart: '', thickness: '', history: '', recipe: '', reason: '' },
    { title: 'ロング・明るめの髪色',       before: 'assets/ba4040a-before-600.jpg', after: 'assets/ba4040a-after-600.jpg', chart: '', thickness: '', history: '', recipe: '', reason: '' }
  ],
  price: '13,200円（税込）',                // サンプルセットの価格表記。空文字にすると価格の行が非表示になる
  profile: { name: '菅原 寛人', romaji: 'Hiroto Sugawara', role: 'sins cosmetics ／ 現役美容師（sinsia）' },
  testimonials: []                         // 実在の受講者の声のみ。例: { quote: '…', salon: '〇〇（神奈川）', name: '〇〇 様', photo: 'assets/voice-1.jpg' }
};
