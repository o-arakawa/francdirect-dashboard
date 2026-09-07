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
  var VID = CFG.video || { type: 'none' };
  var LS_KEY = 'sins_lp_unlocked_v1:' + (VID.type || 'none') + ':' + (VID.src || '');   // 動画ごとに記憶（動画公開前の解放は保存しない）
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
        '<div class="ba" role="group" aria-label="施術例' + n + ' ビフォーアフター比較">' +
          pic(c.after, '施術例' + n + ' 施術後') +
          '<div class="ba__after" style="--pos:50%">' + pic(c.before, '施術例' + n + ' 施術前') + '</div>' +
          '<span class="ba__label ba__label--before" aria-hidden="true">Before</span><span class="ba__label ba__label--after" aria-hidden="true">After</span>' +
          '<div class="ba__handle" aria-hidden="true"><span></span></div><span class="ba__hint" aria-hidden="true">◂ ドラッグして比較 ▸</span>' +
          '<input class="ba__range" type="range" min="0" max="100" value="50" aria-label="ビフォーアフターの比較位置">' +
        '</div>' +
        '<div class="case__body"><p class="case__num">CASE ' + n + '</p><h3 class="case__title">' + esc(c.title || '') + '</h3>' +
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

  /* ---------- 6. Video + purchase gate ---------- */
  var video = CFG.video || { type: 'none' };
  var threshold = typeof CFG.unlockAt === 'number' ? CFG.unlockAt : 0.9;
  var unlocked = false;
  var stage = $('#video-stage'), progressEl = $('#video-progress'), progressTxt = $('#video-progress-text');
  var speedBtn = $('#speed-btn');
  var maxWatched = 0, duration = 0, poll = null;
  var buckets = {}, bucketCount = 0; // 実際に再生した区間（約5秒）のユニーク数で視聴率を判定（シークで飛ばした区間は数えない）
  function bucketSec() { return duration ? Math.max(1, Math.min(5, duration / 40)) : 5; }
  function totalBuckets() { return Math.max(1, Math.ceil(duration / bucketSec())); }
  function markTime(t) {
    if (!(t >= 0) || !duration) return;
    if (t > maxWatched) maxWatched = t;
    var b = Math.floor(t / bucketSec());
    if (!buckets[b]) { buckets[b] = 1; bucketCount++; saveProgress(); }
    setProgress(bucketCount / totalBuckets());
  }

  var ringFg = $('#ring-fg'), ringTxt = $('#ring-text'), ringBox = $('.ring'), lastAnnounced = -1;
  function setProgress(ratio) {
    ratio = Math.max(0, Math.min(1, ratio || 0));
    var pct = Math.round(ratio * 100);
    if (progressEl) { progressEl.style.width = (ratio * 100) + '%'; var pb = progressEl.parentNode; if (pb) pb.setAttribute('aria-valuenow', pct); }
    if (progressTxt) progressTxt.textContent = pct + '%';
    if (ringFg) ringFg.style.strokeDashoffset = String(1 - ratio);
    if (ringTxt) ringTxt.textContent = pct + '%';
    var step = Math.floor(pct / 10) * 10;
    if (step !== lastAnnounced && step > 0) { lastAnnounced = step; var live = $('#gate-live'); if (live) live.textContent = '視聴 ' + step + '% です'; }
    if (ratio >= threshold) unlock('progress');
  }
  var PROG_KEY = 'sins_video_progress_v1:' + (VID.type || 'none') + ':' + (VID.src || '');
  function saveProgress() { try { localStorage.setItem(PROG_KEY, JSON.stringify({ d: duration, b: Object.keys(buckets).map(Number) })); } catch (e) {} }
  function restoreProgress() {
    try {
      var s = JSON.parse(localStorage.getItem(PROG_KEY) || 'null');
      if (s && s.d && duration && Math.abs(s.d - duration) < 2 && s.b && s.b.length) {
        s.b.forEach(function (b) { if (!buckets[b]) { buckets[b] = 1; bucketCount++; } });
        setProgress(bucketCount / totalBuckets());
      }
    } catch (e) {}
  }

  function unlock(reason) {
    if (unlocked) return;
    unlocked = true;
    body.classList.add('is-unlocked');
    if (reason === 'progress' || reason === 'ended' || reason === 'self-report') { try { localStorage.setItem(LS_KEY, JSON.stringify({ t: Date.now(), r: reason })); } catch (e) {} }
    var gate = $('#purchase-gate');
    if (gate) {
      gate.classList.add('is-open');
      $$('a, button', gate).forEach(function (el) { el.removeAttribute('tabindex'); });
    }
    $$('[data-locked]').forEach(function (el) { el.hidden = true; });
    $$('[data-unlocked]').forEach(function (el) { el.hidden = false; });
    if (bar) bar.classList.add('is-unlocked');
    if (reason === 'progress' || reason === 'ended' || reason === 'self-report') {
      var note = $('#unlock-note');
      if (note) { note.hidden = false; }
      var live = $('#gate-live'); if (live) live.textContent = 'サンプルセットのご案内を表示しました';
      if (gate && reason !== 'progress') { // 再生中（90%到達）はフォーカスを奪わず、終了時だけ案内へ移動
        gate.setAttribute('tabindex', '-1');
        setTimeout(function () { gate.scrollIntoView({ behavior: reduceMotion ? 'auto' : 'smooth', block: 'nearest' }); try { gate.focus({ preventScroll: true }); } catch (e) {} }, 600);
      }
    }
  }

  // Already unlocked on a previous visit?
  try {
    var saved = JSON.parse(localStorage.getItem(LS_KEY) || 'null');
    if (saved && saved.t && (Date.now() - saved.t) < TTL_MS) unlock('remembered');
  } catch (e) {}

  function loadScript(src, cb) {
    var s = doc.createElement('script'); s.src = src; s.async = true; s.onload = cb; s.onerror = function () { showFallback(); }; doc.head.appendChild(s);
  }
  function videoUrl() {
    if (video.type === 'youtube') return 'https://www.youtube.com/watch?v=' + encodeURIComponent(video.src);
    if (video.type === 'vimeo') return 'https://vimeo.com/' + encodeURIComponent(video.src);
    return video.src || '#';
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

  function initMp4() {
    var v = doc.createElement('video');
    v.setAttribute('controls', ''); v.setAttribute('playsinline', ''); v.setAttribute('preload', 'metadata');
    if (video.poster) v.setAttribute('poster', video.poster);
    v.className = 'video__el';
    v.src = video.src;
    stage.innerHTML = ''; stage.appendChild(v);
    v.addEventListener('loadedmetadata', function () { duration = v.duration || 0; restoreProgress(); });
    v.addEventListener('timeupdate', function () { if (!v.paused) markTime(v.currentTime); });
    v.addEventListener('ended', function () { setProgress(1); unlock('ended'); });
    v.addEventListener('error', showFallback);
    if (speedBtn) speedBtn.addEventListener('click', function () {
      var fast = v.playbackRate < 1.9; v.playbackRate = fast ? 2 : 1; speedBtn.setAttribute('aria-pressed', fast ? 'true' : 'false');
      if (v.paused) { var pr = v.play(); if (pr && typeof pr.catch === 'function') pr.catch(function () {}); }
    });
  }

  function initYouTube() {
    var id = String(video.src).trim(); // YouTube video id
    var ytRestored = false;
    var holder = doc.createElement('div'); holder.id = 'yt-player'; stage.innerHTML = ''; stage.appendChild(holder);
    window.onYouTubeIframeAPIReady = function () {
      var player = new YT.Player('yt-player', {
        videoId: id,
        host: 'https://www.youtube-nocookie.com',
        playerVars: { rel: 0, modestbranding: 1, playsinline: 1, origin: location.origin },
        events: {
          onReady: function () { duration = player.getDuration() || 0; if (duration) { ytRestored = true; restoreProgress(); } },
          onStateChange: function (e) {
            if (e.data === YT.PlayerState.PLAYING) {
              duration = player.getDuration() || duration;
              if (!ytRestored && duration) { ytRestored = true; restoreProgress(); }
              if (!poll) poll = setInterval(function () { markTime(player.getCurrentTime()); }, 1000);
            } else if (poll && e.data !== YT.PlayerState.BUFFERING) { clearInterval(poll); poll = null; }
            if (e.data === YT.PlayerState.ENDED) { setProgress(1); unlock('ended'); }
          },
          onError: showFallback
        }
      });
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
    iframe.src = 'https://player.vimeo.com/video/' + encodeURIComponent(String(video.src).trim()) + '?dnt=1&title=0&byline=0&portrait=0&playsinline=1';
    iframe.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture'); iframe.setAttribute('allowfullscreen', ''); iframe.title = 'オンラインセミナー動画';
    iframe.className = 'video__el'; stage.innerHTML = ''; stage.appendChild(iframe);
    loadScript('https://player.vimeo.com/api/player.js', function () {
      var player = new Vimeo.Player(iframe);
      var restored = false;
      player.on('timeupdate', function (d) { if (d.duration) duration = d.duration; if (!restored && duration) { restored = true; restoreProgress(); } markTime(d.seconds); });
      player.on('ended', function () { setProgress(1); unlock('ended'); });
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
    if (video.type === 'mp4' && video.src) initMp4();
    else if (video.type === 'youtube' && video.src) initYouTube();
    else if (video.type === 'vimeo' && video.src) initVimeo();
    else {
      // No video configured yet → placeholder; purchase CTA available immediately (configurable)
      body.classList.add('no-video');
      if (speedBtn) speedBtn.hidden = true;
      var th = $('.gate__open .thanks'); if (th) th.textContent = '動画公開前のご案内';
      var hs = $('#hero .btn__sub'); if (hs) hs.textContent = '約25分・登録不要・動画は近日公開';
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
