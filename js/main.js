/* OLIMAIS — site público. JavaScript simples, sem bibliotecas.
   Faz quatro coisas: abre/fecha o menu no celular, controla o carrossel de
   depoimentos, atualiza o ano no rodapé e mostra os posts mais recentes do Instagram. Se o JavaScript falhar, o site
   continua inteiro legível (só o menu e as setas do carrossel deixam de abrir). */
(function () {
  'use strict';
  var doc = document;

  function onMediaChange(mq, fn) {
    if (mq.addEventListener) mq.addEventListener('change', fn);
    else if (mq.addListener) mq.addListener(fn);   // Safari antigo
  }

  // ---- Ano do rodapé ----
  var ano = doc.getElementById('ano');
  if (ano) ano.textContent = String(new Date().getFullYear());

  // ---- Instagram: troca os quadrinhos fixos pelos posts mais recentes ----
  // A automação do GitHub (scripts/instagram_sync.py) grava data/instagram.json e as imagens em
  // img/instagram/. Se o arquivo não existir, estiver vazio ou for inválido, os quadrinhos fixos
  // que já estão no HTML continuam valendo. Só são aceitos links do Instagram e imagens da pasta
  // img/instagram/ (nada de fora), e tudo é montado como texto, nunca como HTML.
  var feed = doc.querySelector('[data-insta-feed]');
  if (feed && window.fetch) {
    var LINK_OK = /^https:\/\/(www\.)?instagram\.com\/(p|reel|reels|tv)\/[A-Za-z0-9_-]+\/?(\?\S*)?$/;
    var IMG_OK = /^img\/instagram\/[A-Za-z0-9_-]+\.jpg$/;
    window.fetch(feed.getAttribute('data-insta-feed'), { cache: 'no-cache' })
      .then(function (r) { return r.ok ? r.json() : null; })
      .then(function (d) {
        if (!d || !d.posts || !d.posts.length) return;
        var posts = [];
        for (var i = 0; i < d.posts.length && posts.length < 12; i++) {
          var p = d.posts[i];
          if (p && LINK_OK.test(String(p.url)) && IMG_OK.test(String(p.image))) posts.push(p);
        }
        if (!posts.length) return;
        var frag = doc.createDocumentFragment();
        posts.forEach(function (p) {
          var a = doc.createElement('a');
          a.href = p.url; a.target = '_blank'; a.rel = 'noopener';
          if (p.video) a.className = 'is-video';
          var img = doc.createElement('img');
          img.src = p.image; img.width = 640; img.height = 640; img.loading = 'lazy'; img.decoding = 'async';
          img.alt = String(p.alt || 'Publicação do Instagram da OLIMAIS').slice(0, 160);
          a.appendChild(img);
          frag.appendChild(a);
        });
        while (feed.firstChild) feed.removeChild(feed.firstChild);
        feed.appendChild(frag);
      })
      .catch(function () { /* sem problema: ficam os quadrinhos fixos */ });
  }

  // ---- Menu no celular ----
  var header = doc.querySelector('.site-header');
  var menuBtn = doc.querySelector('[data-menu-btn]');
  if (header && menuBtn) {
    var setOpen = function (open) {
      header.classList.toggle('is-open', open);
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    };
    menuBtn.addEventListener('click', function () {
      setOpen(!header.classList.contains('is-open'));
    });
    header.addEventListener('click', function (e) {
      var t = e.target;
      if (t && t.closest && t.closest('.site-nav a')) setOpen(false);   // fecha ao escolher um link
    });
    doc.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && header.classList.contains('is-open')) { setOpen(false); menuBtn.focus(); }
    });
    onMediaChange(window.matchMedia('(min-width: 1201px)'), function (m) { if (m.matches) setOpen(false); });
  }

  // ---- Carrossel de depoimentos ----
  var car = doc.querySelector('[data-carousel]');
  if (car) {
    var track = car.querySelector('[data-track]');
    var slides = track.children;
    var dotsBox = car.querySelector('[data-dots]');
    var prev = car.querySelector('[data-prev]');
    var next = car.querySelector('[data-next]');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var dots = [];
    var index = 0;

    var goTo = function (i) {
      i = Math.max(0, Math.min(slides.length - 1, i));
      var left = slides[i].getBoundingClientRect().left - track.getBoundingClientRect().left + track.scrollLeft;
      track.scrollTo({ left: left, behavior: reduce ? 'auto' : 'smooth' });
    };

    var current = function () {
      var best = 0, bestDist = Infinity, trackLeft = track.getBoundingClientRect().left;
      for (var i = 0; i < slides.length; i++) {
        var d = Math.abs(slides[i].getBoundingClientRect().left - trackLeft);
        if (d < bestDist) { bestDist = d; best = i; }
      }
      return best;
    };

    var paint = function () {
      index = current();
      for (var i = 0; i < dots.length; i++) dots[i].setAttribute('aria-current', i === index ? 'true' : 'false');
      prev.disabled = index === 0;
      next.disabled = index === slides.length - 1;
    };

    for (var n = 0; n < slides.length; n++) {
      (function (k) {
        var b = doc.createElement('button');
        b.type = 'button';
        b.className = 'dot-btn';
        b.setAttribute('aria-label', 'Ir para o depoimento ' + (k + 1));
        b.addEventListener('click', function () { goTo(k); });
        dotsBox.appendChild(b);
        dots.push(b);
      })(n);
    }

    prev.addEventListener('click', function () { goTo(index - 1); });
    next.addEventListener('click', function () { goTo(index + 1); });
    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); goTo(index + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(index - 1); }
    });

    var ticking = false;
    track.addEventListener('scroll', function () {
      if (ticking) return;
      ticking = true;
      window.requestAnimationFrame(function () { paint(); ticking = false; });
    }, { passive: true });
    window.addEventListener('resize', paint);
    paint();
  }
})();
