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
      var scope = listEl.parentElement || listEl;
      var empty = listEl.querySelector('.search-empty') || scope.querySelector('.search-empty');
      if (empty) { empty.style.display = shown === 0 ? '' : 'none'; }
      var count = listEl.querySelector('.search-count') || scope.querySelector('.search-count');
      if (count) { count.textContent = shown + ' tool' + (shown === 1 ? '' : 's'); }
    });
  }

  // Home page quick search: live dropdown over all tools + filter the grid below.
  var homeSearch = document.querySelector('#home-search');
  var homeList = document.querySelector('#home-tool-list');
  var homeResults = document.querySelector('#home-results');
  var searchGo = document.querySelector('#home-search-go');
  // Read tools lazily: tools-data.js may load after this script (script order
  // varies by page), so resolve at call time rather than snapshotting here.
  function getTools() { return (window.CalcHubData && window.CalcHubData.tools) || []; }
  var activeIndex = -1;

  // Unified base: read the same prefix the build script used for static HTML
  // links. Falls back to pathname derivation only if the meta is absent.
  var baseMeta = document.querySelector('meta[name="calchub-base"]');
  function siteRoot() {
    if (baseMeta) return baseMeta.getAttribute('content') || '';
    return window.location.pathname.replace(/[^/]*$/, '');
  }
  function resultLink(t) { return siteRoot() + 'tools/' + t.slug + '/'; }
  function renderResults(q) {
    if (!homeResults) return;
    var query = q.trim().toLowerCase();
    var matches = [];
    var tools = getTools();
    for (var i = 0; i < tools.length && matches.length < 8; i++) {
      var t = tools[i];
      if (!query || (t.name + ' ' + t.slug + ' ' + (t.desc || '')).toLowerCase().indexOf(query) !== -1) {
        matches.push(t);
      }
    }
    activeIndex = -1;
    if (!query) { homeResults.classList.remove('open'); homeResults.innerHTML = ''; return; }
    if (!matches.length) {
      homeResults.innerHTML = '<div class="search-empty"><strong>No tools found</strong>Try a different keyword.</div>';
    } else {
      homeResults.innerHTML = matches.map(function (t) {
        return '<a class="search-result" href="' + resultLink(t) + '">' +
          '<span class="sr-icon"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="M21 21l-4.3-4.3"/></svg></span>' +
          '<span class="sr-meta"><strong>' + t.name + '</strong><small>' + (t.desc || '') + '</small></span></a>';
      }).join('');
    }
    homeResults.classList.add('open');
    if (homeSearch) homeSearch.setAttribute('aria-expanded', 'true');
  }
  function closeResults() {
    if (homeResults) { homeResults.classList.remove('open'); }
    if (homeSearch) homeSearch.setAttribute('aria-expanded', 'false');
    activeIndex = -1;
  }
  if (homeSearch) {
    homeSearch.addEventListener('input', function () {
      renderResults(homeSearch.value);
      if (homeList) setupSearch(homeSearch, homeList);
    });
    homeSearch.addEventListener('keydown', function (e) {
      var items = homeResults ? homeResults.querySelectorAll('.search-result') : [];
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = Math.min(activeIndex + 1, items.length - 1);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = Math.max(activeIndex - 1, 0);
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && items[activeIndex]) { window.location.href = items[activeIndex].href; return; }
        if (items.length) { window.location.href = items[0].href; return; }
        if (searchGo) searchGo.click();
      } else if (e.key === 'Escape') { closeResults(); }
      for (var i = 0; i < items.length; i++) { items[i].classList.toggle('active', i === activeIndex); }
    });
    homeSearch.addEventListener('focus', function () { if (homeSearch.value.trim()) renderResults(homeSearch.value); });
  }
  if (searchGo) searchGo.addEventListener('click', function () {
    window.location.href = siteRoot() + 'search/?q=' + encodeURIComponent(homeSearch ? homeSearch.value : '');
  });
  document.addEventListener('click', function (e) {
    if (homeResults && homeSearch && !e.target.closest('.hero-search')) closeResults();
  });

  // Search page
  var pageSearch = document.querySelector('#page-search');
  var pageList = document.querySelector('#page-tool-list');
  if (pageSearch && pageList) {
    setupSearch(pageSearch, pageList);
    var qParam = new URLSearchParams(window.location.search).get('q');
    if (qParam) {
      pageSearch.value = qParam;
      pageSearch.dispatchEvent(new Event('input'));
    }
  }

  // ---------- Category filter tabs (home All Tools + directory) ----------
  var filterTabs = document.querySelectorAll('.filter-tab');
  if (filterTabs.length) {
    var filterScope = document.querySelector('#home-tool-list') || document.querySelector('#category-tool-list');
    var filterCount = document.querySelector('#all-tools-count') || document.querySelector('.search-count');
    var filterEmpty = document.querySelector('#all-tools-empty');
    filterTabs.forEach(function (tab) {
      tab.addEventListener('click', function () {
        filterTabs.forEach(function (t) { t.classList.remove('active'); });
        tab.classList.add('active');
        var cat = tab.getAttribute('data-filter');
        var shown = 0;
        if (filterScope) {
          var cards = filterScope.querySelectorAll('[data-cat]');
          for (var i = 0; i < cards.length; i++) {
            var match = (cat === 'all' || cards[i].getAttribute('data-cat') === cat);
            cards[i].style.display = match ? '' : 'none';
            if (match) shown++;
          }
        }
        if (filterCount) filterCount.textContent = shown + ' tool' + (shown === 1 ? '' : 's');
        if (filterEmpty) filterEmpty.classList.toggle('show', shown === 0);
      });
    });
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