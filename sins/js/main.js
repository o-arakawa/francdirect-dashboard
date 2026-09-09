/* ==========================================================================
   sins 髪質改善ストレート LP — 動作（動画ゲート・スライダー・FAQなど）。通常は編集不要です
   ========================================================================== */
(function () {
  'use strict';
  var CFG = window.SINS_LP_CONFIG || {};
  var doc = document, body = doc.body;
  var $ = function (s, r) { return (r || doc).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || doc).querySelectorAll(s)); };
  var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var VLIST = (CFG.videos && CFG.videos.length) ? CFG.videos : (CFG.video ? [CFG.video] : []);
  var LS_KEY = 'sins_lp_unlocked_v1:' + VLIST.map(function (v) { return ((v && v.type) || 'none') + ':' + ((v && v.src) || ''); }).join('|');   // 動画ごとに記憶（動画公開前の解放は保存しない）
  var TTL_MS = (CFG.unlockTtlDays || 90) * 864e5;

  /* ---------- 1. Scroll reveal ---------- */
  var io = null;
  if ('IntersectionObserver' in window && !reduceMotion) {
    io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  }
  function observeReveals() {
    $$('[data-reveal]:not([data-observed])').forEach(function (el) {
      el.setAttribute('data-observed', '');
      if (io) io.observe(el); else el.classList.add('is-in');
    });
  }
  observeReveals();

  /* ---------- 2. Header + sticky CTA bar ---------- */
  var header = $('#site-header'), bar = $('#sticky-bar'), hero = $('#hero'), heroCta = $('#hero .btn-row');
  function onScroll() {
    var y = window.scrollY || doc.documentElement.scrollTop;
    if (header) header.classList.toggle('is-scrolled', y > 24);
    if (bar && hero) {
      var limit = heroCta ? (heroCta.getBoundingClientRect().top + y + heroCta.offsetHeight - window.innerHeight + 40) : hero.offsetHeight * 0.6;
      bar.classList.toggle('is-visible', y > Math.max(limit, 120));
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  if ('IntersectionObserver' in window) {
    if (heroCta && header) new IntersectionObserver(function (es) { header.classList.toggle('hero-cta-visible', es[0].isIntersecting); }, { threshold: 0.4 }).observe(heroCta);
    var stageEl = $('#video-stage');
    if (stageEl && bar) new IntersectionObserver(function (es) { bar.classList.toggle('is-suppressed', es[0].isIntersecting); }, { threshold: 0.35 }).observe(stageEl);
  }

  /* ---------- 3. Before / After sliders (static ones) ---------- */
  $$('.ba').forEach(function (ba) { initBA(ba); });

  /* ---------- 4. Cases (施術例) from config ---------- */
  var casesRoot = $('#cases-grid');
  if (casesRoot && CFG.cases && CFG.cases.length) {
    var FIELD_LABELS = { chart: '癖毛チャート', thickness: '髪の太さ', history: 'カラー履歴', recipe: '使用レシピ', reason: '選定理由' };
    casesRoot.innerHTML = CFG.cases.map(function (c, i) {
      var n = ('0' + (i + 1)).slice(-2);
      var rows = Object.keys(FIELD_LABELS).map(function (k) {
        var v = String(c[k] == null ? '' : c[k]).trim();
        return '<div class="case__row' + (v ? '' : ' is-empty') + '"><dt>' + FIELD_LABELS[k] + '</dt><dd>' + (v ? esc(v) : '<span>動画内で解説</span>') + '</dd></div>';
      }).join('');
      return '<article class="case" data-reveal>' +
        '<div class="ba" role="group" style="aspect-ratio:' + esc(c.ratio || '1/1') + '" aria-label="施術例' + n + ' ビフォーアフター比較">' +
          pic(c.after, '施術例' + n + ' 施術後') +
          '<div class="ba__after" style="--pos:50%">' + pic(c.before, '施術例' + n + ' 施術前') + '</div>' +
          '<span class="ba__label ba__label--before" aria-hidden="true">Before</span><span class="ba__label ba__label--after" aria-hidden="true">After</span>' +
          '<div class="ba__handle" aria-hidden="true"><span></span></div><span class="ba__hint" aria-hidden="true">◂ ドラッグして比較 ▸</span>' +
          '<input class="ba__range" type="range" min="0" max="100" value="50" aria-label="ビフォーアフターの比較位置">' +
        '</div>' +
        '<div class="case__body"><p class="case__num">CASE ' + n + '</p>' + (c.title ? '<h3 class="case__title">' + esc(c.title) + '</h3>' : '') +
        '<dl class="case__dl">' + rows + '</dl></div></article>';
    }).join('');
    // re-init sliders for injected cases
    $$('.ba', casesRoot).forEach(initBA);
    observeReveals();
  }
  function initBA(ba) {
    var range = $('.ba__range', ba), afterWrap = $('.ba__after', ba), handle = $('.ba__handle', ba);
    function set(v) { v = Math.max(0, Math.min(100, v)); afterWrap.style.setProperty('--pos', v + '%'); handle.style.left = v + '%'; range.value = v; }
    range.addEventListener('input', function () { set(parseFloat(range.value)); }); // range が全面を覆い、ドラッグ／タップ／キーボードを一手に受ける
    set(50);
  }
  function esc(s) { return String(s).replace(/[&<>"']/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  // 'assets/xxx-600.jpg' のような命名なら 480/800 の webp/jpg 候補を生成、それ以外はそのまま表示
  function pic(src, alt) {
    var m = /^(.*)-(\d+)\.(jpe?g|webp)$/i.exec(String(src));
    if (!m) return '<img class="ba__img" src="' + esc(src) + '" alt="' + esc(alt) + '" loading="lazy" decoding="async" width="636" height="1280">';
    var b = esc(m[1]), sizes = '(min-width: 760px) 33vw, 100vw';
    return '<picture><source type="image/webp" srcset="' + b + '-480.webp 480w, ' + b + '-800.webp 800w" sizes="' + sizes + '">' +
      '<img class="ba__img" src="' + b + '-800.jpg" srcset="' + b + '-480.jpg 480w, ' + b + '-800.jpg 800w" sizes="' + sizes + '" alt="' + esc(alt) + '" loading="lazy" decoding="async" width="800" height="1610"></picture>';
  }

  /* ---------- 5. Testimonials (only real ones; hidden until provided) ---------- */
  var tRoot = $('#testimonials');
  if (tRoot) {
    var list = (CFG.testimonials || []).filter(function (t) { return t && t.quote; });
    if (list.length) {
      tRoot.hidden = false;
      $('#testimonials-grid').innerHTML = list.map(function (t) {
        return '<figure class="voice" data-reveal>' +
          (t.photo ? '<img class="voice__photo" src="' + esc(t.photo) + '" alt="" loading="lazy" decoding="async" width="96" height="96">' : '') +
          '<blockquote class="voice__quote">' + esc(t.quote) + '</blockquote>' +
          '<figcaption class="voice__meta">' + esc(t.salon || '') + (t.name ? '<span>' + esc(t.name) + '</span>' : '') + '</figcaption></figure>';
      }).join('');
      observeReveals();
    }
  }


  /* ---------- 5b. Config wiring (URLs / price / profile) ---------- */
  var purchaseUrl = CFG.purchaseUrl || 'https://sins.base.shop';
  $$('[data-purchase]').forEach(function (a) { a.href = purchaseUrl; });
  if (CFG.lineUrl) { $$('[data-line]').forEach(function (a) { a.href = CFG.lineUrl; a.hidden = false; a.style.display = ''; }); }
  if (typeof CFG.price === 'string') {
    if (CFG.price.trim()) { $$('[data-price]').forEach(function (el) { el.textContent = CFG.price; }); }
    else { $$('[data-price-row]').forEach(function (el) { el.hidden = true; }); $$('[data-price]').forEach(function (el) { el.textContent = '価格は購入ページでご確認ください'; }); }
  }
  if (CFG.profile) { Object.keys(CFG.profile).forEach(function (k) { $$('[data-profile="' + k + '"]').forEach(function (el) { if (CFG.profile[k]) el.textContent = CFG.profile[k]; }); }); }
  if (CFG.contactUrl) {
    $$('[data-contact]').forEach(function (a) { a.href = CFG.contactUrl; a.hidden = false; if (/^mailto:/.test(CFG.contactUrl)) { a.removeAttribute('target'); } });
    $$('[data-contact-text]').forEach(function (s) { var a = doc.createElement('a'); a.href = CFG.contactUrl; a.textContent = 'お問い合わせ'; a.style.textDecoration = 'underline'; a.style.textUnderlineOffset = '3px'; if (!/^mailto:/.test(CFG.contactUrl)) { a.target = '_blank'; a.rel = 'noopener'; } s.replaceWith(a); });
  } else if (CFG.lineUrl) {
    $$('[data-contact-text]').forEach(function (s) { var a = doc.createElement('a'); a.href = CFG.lineUrl; a.textContent = '公式LINE'; a.target = '_blank'; a.rel = 'noopener'; a.style.textDecoration = 'underline'; a.style.textUnderlineOffset = '3px'; s.replaceWith(a); });
  }

  /* ---------- 6. 動画 ＋ 購入ゲート（動画は複数本に対応。config.js の videos を参照） ---------- */
  var RAW_VIDEOS = (CFG.videos && CFG.videos.length) ? CFG.videos : (CFG.video ? [CFG.video] : []);
  var videos = RAW_VIDEOS.filter(function (v) { return v && v.type && v.type !== 'none' && v.src; });
  var unlockRule = CFG.unlockRule || 'any';          // 'any' = どれか1本 / 'all' = 全部 / 'first' = 1本目
  var threshold = typeof CFG.unlockAt === 'number' ? CFG.unlockAt : 0.9;
  var unlocked = false;
  var stage = $('#video-stage'), progressEl = $('#video-progress'), progressTxt = $('#video-progress-text');
  var speedBtn = $('#speed-btn');
  var cur = 0, poll = null, player = null, playerKind = '';
  // 動画ごとの視聴状態：実際に再生した区間（約5秒）のユニーク数で視聴率を判定（シークで飛ばした区間は数えない）
  var st = videos.map(function () { return { duration: 0, buckets: {}, count: 0, done: false, restored: false }; });
  function S() { return st[cur]; }
  function bucketSec(d) { return d ? Math.max(1, Math.min(5, d / 40)) : 5; }
  function totalBuckets(d) { return Math.max(1, Math.ceil(d / bucketSec(d))); }
  function ratioOf(s) { return s.duration ? Math.min(1, s.count / totalBuckets(s.duration)) : 0; }

  var ringFg = $('#ring-fg'), ringTxt = $('#ring-text'), lastAnnounced = -1;
  function paintProgress(ratio) {
    ratio = Math.max(0, Math.min(1, ratio || 0));
    var pct = Math.round(ratio * 100);
    if (progressEl) { progressEl.style.width = (ratio * 100) + '%'; var pb = progressEl.parentNode; if (pb) pb.setAttribute('aria-valuenow', pct); }
    if (progressTxt) progressTxt.textContent = pct + '%';
    if (ringFg) ringFg.style.strokeDashoffset = String(1 - ratio);
    if (ringTxt) ringTxt.textContent = pct + '%';
    var step = Math.floor(pct / 10) * 10;
    if (step !== lastAnnounced && step > 0) { lastAnnounced = step; var live = $('#gate-live'); if (live) live.textContent = '視聴 ' + step + '% です'; }
  }
  function markTime(t) {
    var s = S(); if (!s || !(t >= 0)) return;
    var b = Math.floor(t / bucketSec(s.duration));
    if (!s.buckets[b]) { s.buckets[b] = 1; s.count++; if (s.duration) saveProgress(); }
    if (s.duration) { var r = ratioOf(s); paintProgress(r); if (r >= threshold && !s.done) { s.done = true; saveProgress(); markTabDone(); evalUnlock('progress'); } }
  }
  function markEnded() { var s = S(); if (!s) return; paintProgress(1); if (!s.done) { s.done = true; saveProgress(); markTabDone(); } evalUnlock('ended'); }
  function evalUnlock(reason) {
    var dones = st.map(function (s) { return s.done; });
    var ok = unlockRule === 'all' ? dones.length > 0 && dones.every(Boolean) : unlockRule === 'first' ? !!dones[0] : dones.some(Boolean);
    if (ok) unlock(reason);
  }
  var PROG_KEY = 'sins_video_progress_v2:';
  function progKey(i) { var v = videos[i]; return PROG_KEY + (v.type || '') + ':' + (v.src || ''); }
  function saveProgress() { try { var s = S(); localStorage.setItem(progKey(cur), JSON.stringify({ d: s.duration, b: Object.keys(s.buckets).map(Number), done: !!s.done })); } catch (e) {} }
  function restoreProgress() {
    var s = S(); if (!s || s.restored || !s.duration) return; s.restored = true;
    try {
      var saved = JSON.parse(localStorage.getItem(progKey(cur)) || 'null');
      if (saved && saved.d && Math.abs(saved.d - s.duration) < 2 && saved.b && saved.b.length) {
        saved.b.forEach(function (b) { if (!s.buckets[b]) { s.buckets[b] = 1; s.count++; } });
        if (saved.done) s.done = true;
        paintProgress(s.done ? 1 : ratioOf(s)); if (s.done) markTabDone(); evalUnlock('remembered');
      }
    } catch (e) {}
  }
  function restoreAllDone() { // 他の動画の「視聴済み」印だけ先に復元（タブの✓表示用）
    st.forEach(function (s, i) { try { var saved = JSON.parse(localStorage.getItem(progKey(i)) || 'null'); if (saved && saved.done) { s.done = true; } } catch (e) {} });
    markTabDone();
  }

  function unlock(reason) {
    if (unlocked) return;
    unlocked = true;
    body.classList.add('is-unlocked');
    if (reason === 'progress' || reason === 'ended' || reason === 'self-report') { try { localStorage.setItem(LS_KEY, JSON.stringify({ t: Date.now(), r: reason })); } catch (e) {} }
    var gate = $('#purchase-gate');
    if (gate) { gate.classList.add('is-open'); $$('a, button', gate).forEach(function (el) { el.removeAttribute('tabindex'); }); }
    $$('[data-locked]').forEach(function (el) { el.hidden = true; });
    $$('[data-unlocked]').forEach(function (el) { el.hidden = false; });
    if (bar) bar.classList.add('is-unlocked');
    if (reason === 'progress' || reason === 'ended' || reason === 'self-report') {
      var note = $('#unlock-note'); if (note) { note.hidden = false; }
      var live = $('#gate-live'); if (live) live.textContent = 'サンプルセットのご案内を表示しました';
      if (gate && reason !== 'progress') { // 再生中（90%到達）はフォーカスを奪わず、終了時だけ案内へ移動
        gate.setAttribute('tabindex', '-1');
        setTimeout(function () { gate.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' }); try { gate.focus({ preventScroll: true }); } catch (e) {} }, 600);
      }
    }
  }

  // 前回の視聴完了を記憶していれば最初から解放
  try {
    var saved = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
    if (saved && saved.t && (Date.now() - saved.t) < TTL_MS) unlock('remembered');
  } catch (e) {}

  function loadScript(src, cb) {
    var s = doc.createElement('script'); s.src = src; s.async = true; s.onload = cb; s.onerror = function () { showFallback(); }; doc.head.appendChild(s);
  }
  function videoUrl(v) {
    v = v || videos[cur] || {};
    if (v.type === 'youtube') return 'https://www.youtube.com/watch?v=' + encodeURIComponent(String(v.src).trim());
    if (v.type === 'vimeo') return 'https://vimeo.com/' + encodeURIComponent(String(v.src).trim());
    return v.src || '#';
  }
  function showFallback() {
    // プレイヤーが読み込めない場合：外部リンクで視聴してもらい、視聴後に自己申告で解放（無音の自動解放はしない）
    if (showFallback.done) return; showFallback.done = true;
    var tools = $('.video-tools'); if (tools) tools.hidden = true;
    var fb = $('#video-fallback'), fl = $('#video-fallback-link'), fd = $('#video-fallback-done');
    if (fl) fl.href = videoUrl();
    if (fb) fb.hidden = false;
    if (fd) fd.addEventListener('click', function () { unlock('self-report'); });
  }

  /* --- タブ（動画が2本以上のとき） --- */
  var tabs = [];
  function buildTabs() {
    if (videos.length < 2 || !stage) return;
    var wrap = doc.createElement('div'); wrap.className = 'video-tabs'; wrap.setAttribute('role', 'tablist'); wrap.setAttribute('aria-label', '動画を選ぶ');
    videos.forEach(function (v, i) {
      var b = doc.createElement('button'); b.type = 'button'; b.className = 'video-tab' + (i === 0 ? ' is-active' : ''); b.setAttribute('role', 'tab'); b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
      b.innerHTML = '<b>' + (i + 1) + '</b><span><span class="video-tab__t">' + esc(v.title || ('動画 ' + (i + 1))) + '</span>' + (v.note ? '<small>' + esc(v.note) + '</small>' : '') + '</span><i class="video-tab__done" aria-label="視聴済み">✓</i>';
      b.addEventListener('click', function () { select(i); });
      wrap.appendChild(b); tabs.push(b);
    });
    stage.parentNode.insertBefore(wrap, stage);
    var badge = $('.video-head .badge'); if (badge) badge.textContent = '無料・登録不要・動画' + videos.length + '本';
    var rn = $('#gate-rule-note'); if (rn) rn.textContent = unlockRule === 'all' ? ' 動画は' + videos.length + '本あります。すべて最後までご覧いただくとご案内が表示されます。' : unlockRule === 'first' ? ' 1本目の動画を最後までご覧いただくとご案内が表示されます。' : ' 動画は' + videos.length + '本あります。どちらか1本を最後までご覧いただくとご案内が表示されます。';
  }
  function markTabDone() { tabs.forEach(function (b, i) { b.classList.toggle('is-done', !!st[i].done); }); }
  function select(i) {
    if (i === cur || !videos[i]) return;
    if (poll) { clearInterval(poll); poll = null; }
    cur = i; lastAnnounced = -1;
    tabs.forEach(function (b, j) { b.classList.toggle('is-active', j === i); b.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
    paintProgress(S().done ? 1 : ratioOf(S()));
    var v = videos[i], id = String(v.src).trim();
    if (playerKind === 'youtube' && player && player.cueVideoById) player.cueVideoById(id);
    else if (playerKind === 'vimeo' && player && player.loadVideo) player.loadVideo(id).catch(function () {});
    else if (playerKind === 'mp4' && player) { player.pause(); player.src = v.src; if (v.poster) player.setAttribute('poster', v.poster); else player.removeAttribute('poster'); player.load(); }
    var fl = $('#video-fallback-link'); if (fl) fl.href = videoUrl(v);
  }

  /* --- プレイヤー --- */
  function onDuration(d) { var s = S(); if (d && !s.duration) { s.duration = d; restoreProgress(); } }

  function initMp4() {
    var v0 = videos[0];
    var v = doc.createElement('video');
    v.setAttribute('controls', ''); v.setAttribute('playsinline', ''); v.setAttribute('preload', 'metadata');
    if (v0.poster) v.setAttribute('poster', v0.poster);
    v.className = 'video__el'; v.src = v0.src;
    stage.innerHTML = ''; stage.appendChild(v); player = v; playerKind = 'mp4';
    v.addEventListener('loadedmetadata', function () { onDuration(v.duration || 0); });
    v.addEventListener('timeupdate', function () { if (!v.paused) markTime(v.currentTime); });
    v.addEventListener('ended', markEnded);
    v.addEventListener('error', showFallback);
    if (speedBtn) speedBtn.addEventListener('click', function () {
      var fast = v.playbackRate < 1.9; v.playbackRate = fast ? 2 : 1; speedBtn.setAttribute('aria-pressed', fast ? 'true' : 'false');
      if (v.paused) { var pr = v.play(); if (pr && typeof pr.catch === 'function') pr.catch(function () {}); }
    });
  }

  function initYouTube() {
    var holder = doc.createElement('div'); holder.id = 'yt-player'; stage.innerHTML = ''; stage.appendChild(holder);
    window.onYouTubeIframeAPIReady = function () {
      player = new YT.Player('yt-player', {
        videoId: String(videos[0].src).trim(),
        host: 'https://www.youtube-nocookie.com',
        playerVars: { rel: 0, modestbranding: 1, playsinline: 1, origin: location.origin },
        events: {
          onReady: function () { playerKind = 'youtube'; onDuration(player.getDuration() || 0); },
          onStateChange: function (e) {
            if (e.data === YT.PlayerState.PLAYING) {
              onDuration(player.getDuration() || 0);
              if (!poll) poll = setInterval(function () { markTime(player.getCurrentTime()); }, 1000);
            } else if (poll && e.data !== YT.PlayerState.BUFFERING) { clearInterval(poll); poll = null; }
            if (e.data === YT.PlayerState.ENDED) markEnded();
          },
          onError: showFallback
        }
      });
      playerKind = 'youtube';
      if (speedBtn) speedBtn.addEventListener('click', function () {
        var fast = player.getPlaybackRate() < 1.9; player.setPlaybackRate(fast ? 2 : 1);
        speedBtn.setAttribute('aria-pressed', fast ? 'true' : 'false');
        if (player.getPlayerState() !== YT.PlayerState.PLAYING) player.playVideo();
      });
    };
    loadScript('https://www.youtube.com/iframe_api');
  }

  function initVimeo() {
    var iframe = doc.createElement('iframe');
    iframe.src = 'https://player.vimeo.com/video/' + encodeURIComponent(String(videos[0].src).trim()) + '?dnt=1&title=0&byline=0&portrait=0&playsinline=1';
    iframe.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture'); iframe.setAttribute('allowfullscreen', ''); iframe.title = 'オンラインセミナー動画';
    iframe.className = 'video__el'; stage.innerHTML = ''; stage.appendChild(iframe);
    loadScript('https://player.vimeo.com/api/player.js', function () {
      player = new Vimeo.Player(iframe); playerKind = 'vimeo';
      player.on('timeupdate', function (d) { if (d.duration) onDuration(d.duration); markTime(d.seconds); });
      player.on('ended', markEnded);
      player.on('error', showFallback);
      if (speedBtn) speedBtn.addEventListener('click', function () {
        player.getPlaybackRate().then(function (r) {
          var fast = r < 1.9; return player.setPlaybackRate(fast ? 2 : 1).then(function () {
            speedBtn.setAttribute('aria-pressed', fast ? 'true' : 'false');
            var pp = player.play(); if (pp && typeof pp.catch === 'function') pp.catch(function () {});
          });
        }).catch(function () {});
      });
    });
  }

  if (stage) {
    if (videos.length) {
      buildTabs(); restoreAllDone();
      var kind = videos[0].type; // 複数本ある場合は1本目の種類（youtube / vimeo / mp4）で統一してください
      if (kind === 'mp4') initMp4(); else if (kind === 'youtube') initYouTube(); else if (kind === 'vimeo') initVimeo();
      evalUnlock('remembered');
    } else {
      // 動画が未設定 → プレースホルダー表示。購入CTAは最初から表示（設定で変更可。この解放は保存しない）
      body.classList.add('no-video');
      if (speedBtn) speedBtn.hidden = true;
      var th = $('.gate__open .thanks'); if (th) th.textContent = '動画公開前のご案内';
      var hs = $('#hero .btn__sub'); if (hs) hs.textContent = '登録不要・動画は近日公開';
      if (CFG.unlockWhenNoVideo !== false) unlock('no-video');
    }
  }

  /* ---------- 6b. 「後で見る」URLコピー ---------- */
  var laterBtn = $('#later-btn');
  if (laterBtn) laterBtn.addEventListener('click', function () {
    var url = location.origin + location.pathname + '#seminar';
    var done = function () { laterBtn.textContent = 'URLをコピーしました'; setTimeout(function () { laterBtn.textContent = '後で見る（URLをコピー）'; }, 2400); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(url).then(done).catch(function () { window.prompt('このURLをコピーしてください', url); });
    else window.prompt('このURLをコピーしてください', url);
  });

  /* ---------- 7. Smooth anchor scroll with header offset (fallback for old browsers) ---------- */
  $$('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (ev) {
      var id = a.getAttribute('href').slice(1); if (!id) return;
      var t = doc.getElementById(id); if (!t) return;
      ev.preventDefault();
      var top = t.getBoundingClientRect().top + window.scrollY - (header ? header.offsetHeight : 0) + 1;
      window.scrollTo({ top: top, behavior: reduceMotion ? 'auto' : 'smooth' });
      history.replaceState(null, '', '#' + id);
      if (!/^(a|button|input|select|textarea)$/i.test(t.tagName) && t.tabIndex < 0) t.setAttribute('tabindex', '-1');
      try { t.focus({ preventScroll: true }); } catch (e) {}
    });
  });

  /* ---------- 7b. a11y: list semantics (list-style:none) and new-tab notices ---------- */
  $$('ul,ol').forEach(function (l) { if (!l.getAttribute('role')) l.setAttribute('role', 'list'); });
  $$('a[target="_blank"]').forEach(function (a) { if (!a.querySelector('.sr-only') && !/新しいタブ/.test(a.textContent)) { var s = doc.createElement('span'); s.className = 'sr-only'; s.textContent = '（新しいタブで開きます）'; a.appendChild(s); } });

  /* ---------- 7c. FAQ の構造化データ（index.html の FAQ 本文から自動生成。FAQ を編集しても二重管理不要） ---------- */
  try {
    var faqs = $$('.faq details').map(function (d) {
      var q = $('summary span', d), a = $('.a p', d);
      return q && a ? { '@type': 'Question', 'name': q.textContent.trim(), 'acceptedAnswer': { '@type': 'Answer', 'text': a.textContent.replace(/\s+/g, ' ').trim() } } : null;
    }).filter(Boolean);
    if (faqs.length) { var ld = doc.createElement('script'); ld.type = 'application/ld+json'; ld.textContent = JSON.stringify({ '@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': faqs }); doc.head.appendChild(ld); }
  } catch (e) {}

  /* ---------- 8. Year ---------- */
  var y = $('#year'); if (y) y.textContent = new Date().getFullYear();
})();
