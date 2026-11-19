/* =========================================================
   CalcHub — main.js
   Shared UI logic: mobile nav, copy-to-clipboard, search,
   generic helpers for tool pages.
   ========================================================= */
(function () {
  'use strict';

  // ---------- Mobile nav toggle ----------
  var toggle = document.querySelector('.menu-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var open = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    // Close nav when a link is clicked on mobile
    nav.addEventListener('click', function (e) {
      if (e.target.closest('a')) {
        nav.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      }
    });
  }

  // ---------- Copy to clipboard (data-copy="<target selector>") ----------
  function copyText(text, btn) {
    if (!text) return;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () {
        flashCopied(btn);
      }, function () {
        fallbackCopy(text, btn);
      });
    } else {
      fallbackCopy(text, btn);
    }
  }

  function fallbackCopy(text, btn) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed';
    ta.style.opacity = '0';
    document.body.appendChild(ta);
    ta.select();
    try { document.execCommand('copy'); flashCopied(btn); }
    catch (err) { flashCopied(btn, 'Copy failed'); }
    document.body.removeChild(ta);
  }

  function flashCopied(btn, label) {
    if (!btn) return;
    var original = btn.textContent;
    btn.textContent = label || 'Copied!';
    btn.classList.add('btn-secondary');
    setTimeout(function () {
      btn.textContent = original;
      btn.classList.remove('btn-secondary');
    }, 1600);
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-copy]');
    if (!btn) return;
    var target = btn.getAttribute('data-copy');
    var el = document.querySelector(target);
    if (!el) return;
    var text = (el.value !== undefined ? el.value : el.textContent) || '';
    copyText(text, btn);
  });

  // ---------- Search (home & search page) ----------
  function setupSearch(inputEl, listEl, allTools) {
    if (!inputEl || !listEl) return;
    inputEl.addEventListener('input', function () {
      var q = inputEl.value.trim().toLowerCase();
      var items = listEl.querySelectorAll('[data-search-item]');
      var shown = 0;
      for (var i = 0; i < items.length; i++) {
        var hay = (items[i].getAttribute('data-search-item') || '').toLowerCase();
        // Also search title and desc text
        var txt = (items[i].textContent || '').toLowerCase();
        var hit = !q || hay.indexOf(q) !== -1 || txt.indexOf(q) !== -1;
        items[i].style.display = hit ? '' : 'none';
        if (hit) shown++;
      }
      var empty = listEl.querySelector('.search-empty');
      if (empty) { empty.style.display = shown === 0 ? '' : 'none'; }
      var count = listEl.querySelector('.search-count');
      if (count) { count.textContent = shown + ' tool' + (shown === 1 ? '' : 's'); }
    });
  }

  // Home page quick search
  var homeSearch = document.querySelector('#home-search');
  var homeList = document.querySelector('#home-tool-list');
  if (homeSearch && homeList) {
    setupSearch(homeSearch, homeList);
  }

  // Search page
  var pageSearch = document.querySelector('#page-search');
  var pageList = document.querySelector('#page-tool-list');
  if (pageSearch && pageList) {
    setupSearch(pageSearch, pageList);
  }

  // Category page filter
  var catSearch = document.querySelector('#category-search');
  var catList = document.querySelector('#category-tool-list');
  if (catSearch && catList) {
    setupSearch(catSearch, catList, window.CalcHubData || {});
  }

  // ---------- Footer year ----------
  var yearEl = document.querySelector('[data-year]');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // ---------- Expose ----------
  window.CalcHub = {
    copyText: copyText,
    setupSearch: setupSearch
  };
})();