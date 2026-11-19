/* =========================================================
   CalcHub — tools.js
   All 30 tool runners. Each page mounts a widget with
   data-tool="<slug>" and the matching runner initializes it.
   100% client-side processing; no data leaves the browser.
   ========================================================= */
(function () {
  'use strict';

  function $(sel, root) { return root.querySelector(sel); }
  function $$(sel, root) { return Array.prototype.slice.call(root.querySelectorAll(sel)); }
  function val(el) { return el ? el.value : ''; }

  function fmtNum(n, decimals) {
    var d = (decimals === undefined || decimals === null) ? 4 : decimals;
    var v = Number(n);
    if (isNaN(v)) return '—';
    return v.toLocaleString('en-US', { maximumFractionDigits: d });
  }

  function statusEl(root, msg, type) {
    var el = $('.status-msg', root);
    if (!el) return;
    if (msg) {
      el.textContent = msg;
      el.className = 'status-msg ' + (type || 'ok');
    } else {
      el.className = 'status-msg';
      el.textContent = '';
    }
  }

  // Unbiased integer in [0, maxExclusive) using rejection sampling over a
  // 32-bit random value. Avoids modulo bias without introducing Math.random.
  function secureRandomInt(maxExclusive) {
    if (maxExclusive <= 0) return 0;
    var buf = new Uint32Array(1);
    var limit = Math.floor(4294967296 / maxExclusive) * maxExclusive;
    do { crypto.getRandomValues(buf); } while (buf[0] >= limit);
    return buf[0] % maxExclusive;
  }

  function copyFrom(root, sel, btnSel) {
    var output = $(sel, root);
    var btn = btnSel ? $(btnSel, root) : null;
    if (!output) return;
    var text = output.value !== undefined ? output.value : output.textContent;
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(function () { flash(btn); });
    } else {
      var ta = document.createElement('textarea');
      ta.value = text; ta.style.position = 'fixed'; ta.style.opacity = '0';
      document.body.appendChild(ta); ta.select();
      try { document.execCommand('copy'); flash(btn); } catch (e) { flash(btn, 'Copy failed'); }
      document.body.removeChild(ta);
    }
  }

  function flash(btn, txt) {
    if (!btn) return;
    var o = btn.textContent;
    btn.textContent = txt || 'Copied!';
    setTimeout(function () { btn.textContent = o; }, 1500);
  }

  function loadImage(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () { resolve(img); URL.revokeObjectURL(url); };
      img.onerror = function () { reject(new Error('Could not read image')); URL.revokeObjectURL(url); };
      img.src = url;
    });
  }

  function downloadBlob(blob, filename) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url; a.download = filename;
    document.body.appendChild(a); a.click();
    setTimeout(function () { document.body.removeChild(a); URL.revokeObjectURL(url); }, 100);
  }

  function canvasToBlob(canvas, type, quality) {
    return new Promise(function (resolve) {
      canvas.toBlob(function (b) { resolve(b); }, type, quality);
    });
  }

  /* ---------- counters ---------- */
  function countWords(str) {
    var m = str.trim().match(/\S+/g);
    return m ? m.length : 0;
  }
  function countSentences(str) {
    var m = str.trim().match(/[^.!?]+[.!?]+["']?/g);
    return m ? m.length : 0;
  }
  function countParagraphs(str) {
    var m = str.trim().split(/\n{2,}/);
    return str.trim() === '' ? 0 : m.length;
  }

  /* =========================================================
     REGISTRY
     ========================================================= */
  var RUNNERS = {};

  /* ---------- 01 word-counter ---------- */
  RUNNERS['word-counter'] = function (root) {
    var textarea = $('textarea', root);
    var out = { words: null, chars: null, charsNoSpace: null, sent: null, para: null, read: null };
    function update() {
      var t = textarea.value;
      out.words.textContent = fmtNum(countWords(t), 0);
      out.chars.textContent = fmtNum(t.length, 0);
      out.charsNoSpace.textContent = fmtNum(t.replace(/\s/g, '').length, 0);
      out.sent.textContent = fmtNum(countSentences(t), 0);
      out.para.textContent = fmtNum(countParagraphs(t), 0);
      var wpm = 225, words = countWords(t);
      var mins = words / wpm;
      out.read.textContent = mins < 1 ? 'Less than 1 minute' : fmtNum(Math.ceil(mins), 0) + ' min read';
    }
    out.words = $('[data-out="words"]', root);
    out.chars = $('[data-out="chars"]', root);
    out.charsNoSpace = $('[data-out="charsNoSpace"]', root);
    out.sent = $('[data-out="sent"]', root);
    out.para = $('[data-out="para"]', root);
    out.read = $('[data-out="read"]', root);
    textarea.addEventListener('input', update);
    $$('[data-select]', root).forEach(function (btn) {
      btn.addEventListener('click', function () {
        var sel = btn.getAttribute('data-select');
        if (sel === 'sample') {
          textarea.value = 'The quick brown fox jumps over the lazy dog. This is a sample sentence with several words.\n\nWriting tools spend most of their time counting characters and words. A good counter updates instantly as you type, so you always know where you stand.\n\nUse the sample text to explore this counter, then paste your own content and see live numbers.';
        } else if (sel === 'clear') {
          textarea.value = '';
        }
        update();
      });
    });
    update();
  };

  /* ---------- 02 character-counter ---------- */
  RUNNERS['character-counter'] = function (root) {
    var ta = $('textarea', root);
    var outs = { total: null, noSpace: null, letters: null, digits: null, punct: null, spaces: null };
    function update() {
      var t = ta.value;
      outs.total.textContent = fmtNum(t.length, 0);
      outs.noSpace.textContent = fmtNum(t.replace(/\s/g, '').length, 0);
      outs.letters.textContent = fmtNum((t.match(/[a-zA-Z]/g) || []).length, 0);
      outs.digits.textContent = fmtNum((t.match(/[0-9]/g) || []).length, 0);
      outs.punct.textContent = fmtNum((t.match(/[^\w\s]/g) || []).length, 0);
      outs.spaces.textContent = fmtNum((t.match(/\s/g) || []).length, 0);
    }
    ['total', 'noSpace', 'letters', 'digits', 'punct', 'spaces'].forEach(function (k) {
      outs[k] = $('[data-out="' + k + '"]', root);
    });
    ta.addEventListener('input', update);
    $('[data-clear]', root).addEventListener('click', function () { ta.value = ''; update(); });
    update();
  };

  /* ---------- 03 reading-time ---------- */
  RUNNERS['reading-time'] = function (root) {
    var ta = $('textarea', root);
    var wpm = $('input[type="number"]', root);
    var outs = { read: null, speak: null, words: null, mins: null, secs: null };
    function update() {
      var w = countWords(ta.value), speed = parseFloat(wpm.value) || 225;
      var mins = w / speed;
      outs.words.textContent = fmtNum(w, 0);
      outs.read.textContent = mins < 1 ? 'Less than 1 minute' : fmtNum(mins, 1) + ' minutes';
      outs.mins.textContent = fmtNum(Math.floor(mins), 0);
      outs.secs.textContent = fmtNum(Math.round((mins % 1) * 60), 0);
      var s = w / 130;
      outs.speak.textContent = s < 1 ? 'Less than 1 minute' : fmtNum(s, 1) + ' minutes';
    }
    ['read', 'speak', 'words', 'mins', 'secs'].forEach(function (k) { outs[k] = $('[data-out="' + k + '"]', root); });
    ta.addEventListener('input', update);
    wpm.addEventListener('input', update);
    update();
  };

  /* ---------- 04 text-case-converter ---------- */
  RUNNERS['text-case-converter'] = function (root) {
    var ta = $('textarea', root);
    var output = $('[data-output]', root);
    var status = $('.status-msg', root);
    function toTitle(s) {
      var small = ['a','an','and','as','at','but','by','for','if','in','nor','of','on','or','so','the','to','up','yet'];
      return s.replace(/\S+/g, function (w, idx, all) {
        var lower = w.toLowerCase();
        if (idx !== 0 && small.indexOf(lower) !== -1) return lower;
        return lower.charAt(0).toUpperCase() + lower.slice(1);
      });
    }
    function transform(kind) {
      var t = ta.value;
      if (kind === 'upper') output.value = t.toUpperCase();
      else if (kind === 'lower') output.value = t.toLowerCase();
      else if (kind === 'title') output.value = toTitle(t);
      else if (kind === 'sentence') output.value = t.replace(/(^\s*|\.\s+)([a-z])/g, function (m, p, c) { return p + c.toUpperCase(); });
      else if (kind === 'camel') {
        output.value = t.toLowerCase().replace(/[^a-zA-Z0-9]+(.)/g, function (m, c) { return c.toUpperCase(); }).replace(/^[A-Z]/, function (c) { return c.toLowerCase(); });
      }
      else if (kind === 'alternating') {
        var r = '';
        for (var i = 0; i < t.length; i++) {
          r += i % 2 === 0 ? t.charAt(i).toUpperCase() : t.charAt(i).toLowerCase();
        }
        output.value = r;
      }
      status.textContent = 'Converted. Copy the result or adjust the input.';
      status.className = 'status-msg ok';
      status.style.display = 'block';
      setTimeout(function () { status.style.display = 'none'; }, 2200);
    }
    $$('[data-case]', root).forEach(function (b) {
      b.addEventListener('click', function () { transform(b.getAttribute('data-case')); });
    });
    $('[data-clear]', root).addEventListener('click', function () { ta.value = ''; output.value = ''; status.className = 'status-msg'; status.textContent = ''; status.style.display = 'none'; });
  };

  /* ---------- 05 remove-duplicate-lines ---------- */
  RUNNERS['remove-duplicate-lines'] = function (root) {
    var ta = $('textarea', root);
    var output = $('[data-output]', root);
    var count = $('[data-count]', root);
    var ignoreCase = $('[data-ignore-case]', root);
    var trim = $('[data-trim]', root);
    function run() {
      var lines = ta.value.split('\n');
      var seen = {}, out = [];
      for (var i = 0; i < lines.length; i++) {
        var line = lines[i];
        if (trim && trim.checked) line = line.trim();
        if (line === '') continue;
        var key = ignoreCase && ignoreCase.checked ? line.toLowerCase() : line;
        if (seen[key]) continue;
        seen[key] = true;
        out.push(line);
      }
      output.value = out.join('\n');
      count.textContent = out.length + ' unique line' + (out.length === 1 ? '' : 's') + ' (from ' + lines.length + ' total)';
    }
    ta.addEventListener('input', run);
    if (ignoreCase) ignoreCase.addEventListener('change', run);
    if (trim) trim.addEventListener('change', run);
    $('[data-run]', root).addEventListener('click', run);
    run();
  };

  /* ---------- 06 lorem-ipsum-generator ---------- */
  RUNNERS['lorem-ipsum-generator'] = function (root) {
    var paras = $('[data-paras]', root);
    var words = $('[data-words]', root);
    var output = $('[data-output]', root);
    var WORDS = ('lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure in reprehenderit voluptate velit esse cillum fugiat nulla pariatur excepteur sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim id est laborum').split(' ');
    function randWord() { return WORDS[secureRandomInt(WORDS.length)]; }
    function cap(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
    function sentence(min) {
      var n = min + secureRandomInt(8);
      var w = [];
      for (var i = 0; i < n; i++) w.push(randWord());
      return cap(w.join(' ')) + '.';
    }
    function generate() {
      var n = parseInt(paras.value, 10) || 3;
      var w = parseInt(words.value, 10) || 0;
      if (n < 1) n = 1;
      if (w > 0) {
        var wordsArr = [];
        for (var i = 0; i < w; i++) wordsArr.push(randWord());
        output.value = cap(wordsArr.join(' ')) + '.';
        return;
      }
      var p = [];
      for (var pIdx = 0; pIdx < n; pIdx++) {
        var sCount = 3 + secureRandomInt(3);
        var pArr = [];
        for (var sIdx = 0; sIdx < sCount; sIdx++) pArr.push(sentence(6 + secureRandomInt(8)));
        p.push(pArr.join(' '));
      }
      output.value = p.join('\n\n');
    }
    $('[data-generate]', root).addEventListener('click', generate);
    generate();
  };

  /* ---------- 07 image-compressor ---------- */
  RUNNERS['image-compressor'] = function (root) {
    var fileInput = $('input[type="file"]', root);
    var dropzone = $('.dropzone', root);
    var scale = $('[data-scale]', root);
    var quality = $('[data-quality]', root);
    var scaleVal = $('[data-scale-val]', root);
    var qualityVal = $('[data-quality-val]', root);
    var preview = $('[data-preview]', root);
    var previewWrap = $('[data-preview-wrap]', root);
    var info = $('[data-info]', root);
    var status = $('.status-msg', root);
    var downloadBtn = $('[data-download]', root);
    var originalFile = null;
    var lastBlob = null;
    var lastName = 'compressed';

    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }

    function handleFile(file) {
      if (!file || !/^image\//.test(file.type)) { setStatus('Please choose an image file.', 'err'); return; }
      originalFile = file;
      lastName = file.name.replace(/\.[^.]+$/, '') + '-compressed';
      loadImage(file).then(function (img) {
        runCompress(img, file);
      }).catch(function () { setStatus('Could not read that image.', 'err'); });
    }

    function readOriginalSize() {
      return originalFile ? originalFile.size : 0;
    }

    function runCompress(img, file) {
      var k = parseFloat(scale.value) || 100;
      var targetW = Math.max(1, Math.round(img.naturalWidth * k / 100));
      var targetH = Math.max(1, Math.round(img.naturalHeight * k / 100));
      var canvas = document.createElement('canvas');
      canvas.width = targetW; canvas.height = targetH;
      var ctx = canvas.getContext('2d');
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(img, 0, 0, targetW, targetH);
      var q = (parseInt(quality.value, 10) || 80) / 100;
      canvasToBlob(canvas, 'image/jpeg', q).then(function (blob) {
        lastBlob = blob;
        var before = readOriginalSize();
        preview.src = URL.createObjectURL(blob);
        var saved = before - blob.size;
        var pct = before > 0 ? Math.round((saved / before) * 100) : 0;
        if (previewWrap) previewWrap.hidden = false;
        if (downloadBtn) downloadBtn.disabled = false;
        info.innerHTML = '<span><b>Original</b> ' + fmtNum(before / 1024, 1) + ' KB</span><span><b>Output</b> ' + fmtNum(blob.size / 1024, 1) + ' KB</span><span><b>Dimensions</b> ' + targetW + ' × ' + targetH + ' px</span>';
        if (before > 0 && saved <= 0) {
          info.innerHTML += '<span style="color:var(--error)"><b>Result</b> ' + fmtNum((blob.size - before) / 1024, 1) + ' KB larger — not compressed</span>';
          setStatus('Output is larger than the original. This image may not benefit from JPEG re-encoding.', 'err');
        } else {
          info.innerHTML += '<span style="color:var(--success)"><b>Result</b> ' + (pct > 0 ? pct + '% smaller than original' : 'Same size as original') + '</span>';
          setStatus('Compressed image ready. Check the preview, then download.', 'ok');
        }
      });
    }

    dropzone.addEventListener('click', function () { fileInput.click(); });
    dropzone.addEventListener('dragover', function (e) { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('dragover'); });
    dropzone.addEventListener('drop', function (e) { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]); });
    fileInput.addEventListener('change', function () { if (fileInput.files.length) handleFile(fileInput.files[0]); });
    scale.addEventListener('input', function () { scaleVal.textContent = scale.value + '%'; if (originalFile) loadImage(originalFile).then(function (img) { runCompress(img, originalFile); }); });
    quality.addEventListener('input', function () { qualityVal.textContent = quality.value + '%'; if (originalFile) loadImage(originalFile).then(function (img) { runCompress(img, originalFile); }); });
    downloadBtn.addEventListener('click', function () { if (lastBlob) downloadBlob(lastBlob, lastName + '.jpg'); });
  };

  /* ---------- 08 image-resizer ---------- */
  RUNNERS['image-resizer'] = function (root) {
    var fileInput = $('input[type="file"]', root);
    var dropzone = $('.dropzone', root);
    var widthIn = $('[data-width]', root);
    var heightIn = $('[data-height]', root);
    var lock = $('[data-lock]', root);
    var preview = $('[data-preview]', root);
    var info = $('[data-info]', root);
    var status = $('.status-msg', root);
    var downloadBtn = $('[data-download]', root);
    var originalFile = null; var natural = null; var lastBlob = null; var lastName = 'resized';

    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }

    function handleFile(file) {
      if (!file || !/^image\//.test(file.type)) { setStatus('Please choose an image file.', 'err'); return; }
      originalFile = file;
      lastName = file.name.replace(/\.[^.]+$/, '') + '-resized';
      loadImage(file).then(function (img) {
        natural = { w: img.naturalWidth, h: img.naturalHeight };
        widthIn.value = natural.w; heightIn.value = natural.h;
        render();
      }).catch(function () { setStatus('Could not read that image.', 'err'); });
    }

    function render() {
      if (!natural) return;
      var w = parseInt(widthIn.value, 10), h = parseInt(heightIn.value, 10);
      if (!w || !h || w < 1 || h < 1) { setStatus('Enter valid dimensions.', 'err'); return; }
      var canvas = document.createElement('canvas');
      canvas.width = w; canvas.height = h;
      var ctx = canvas.getContext('2d');
      ctx.imageSmoothingQuality = 'high';
      loadImage(originalFile).then(function (img) {
        ctx.drawImage(img, 0, 0, w, h);
        canvasToBlob(canvas, 'image/png').then(function (blob) {
          lastBlob = blob;
          preview.src = URL.createObjectURL(blob);
          info.textContent = natural.w + ' × ' + natural.h + ' px → ' + w + ' × ' + h + ' px (' + fmtNum(blob.size / 1024, 1) + ' KB)';
          setStatus('Resized image ready. Download to save it.', 'ok');
        });
      });
    }

    function syncFromWidth() {
      if (!lock.checked || !natural) return;
      var w = parseInt(widthIn.value, 10);
      if (w && w > 0) heightIn.value = Math.round(w * natural.h / natural.w);
      render();
    }
    function syncFromHeight() {
      if (!lock.checked || !natural) return;
      var h = parseInt(heightIn.value, 10);
      if (h && h > 0) widthIn.value = Math.round(h * natural.w / natural.h);
      render();
    }

    dropzone.addEventListener('click', function () { fileInput.click(); });
    dropzone.addEventListener('dragover', function (e) { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('dragover'); });
    dropzone.addEventListener('drop', function (e) { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]); });
    fileInput.addEventListener('change', function () { if (fileInput.files.length) handleFile(fileInput.files[0]); });
    widthIn.addEventListener('input', syncFromWidth);
    heightIn.addEventListener('input', syncFromHeight);
    lock.addEventListener('change', render);
    $('[data-apply]', root).addEventListener('click', render);
    downloadBtn.addEventListener('click', function () { if (lastBlob) downloadBlob(lastBlob, lastName + '.png'); });
  };

  /* ---------- 09 jpg-to-png & 10 png-to-webp ---------- */
  function buildConvertRunner(outputType, mime, ext) {
    return function (root) {
      var fileInput = $('input[type="file"]', root);
      var dropzone = $('.dropzone', root);
      var preview = $('[data-preview]', root);
      var info = $('[data-info]', root);
      var status = $('.status-msg', root);
      var downloadBtn = $('[data-download]', root);
      var originalFile = null; var lastName = 'converted'; var lastBlob = null;

      function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }

      function handleFile(file) {
        if (!file || !/^image\//.test(file.type)) { setStatus('Please choose an image file.', 'err'); return; }
        originalFile = file;
        lastName = file.name.replace(/\.[^.]+$/, '') + '.' + ext;
        loadImage(file).then(function (img) {
          var canvas = document.createElement('canvas');
          canvas.width = img.naturalWidth; canvas.height = img.naturalHeight;
          var ctx = canvas.getContext('2d');
          if (mime === 'image/jpeg') { ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, canvas.width, canvas.height); }
          ctx.drawImage(img, 0, 0);
          canvasToBlob(canvas, mime, 0.92).then(function (blob) {
            lastBlob = blob;
            preview.src = URL.createObjectURL(blob);
            info.textContent = img.naturalWidth + ' × ' + img.naturalHeight + ' px converted to ' + ext.toUpperCase() + ' (' + fmtNum(blob.size / 1024, 1) + ' KB)';
            setStatus('Conversion complete. Download your ' + ext.toUpperCase() + ' file.', 'ok');
          });
        }).catch(function () { setStatus('Could not read that image.', 'err'); });
      }

      dropzone.addEventListener('click', function () { fileInput.click(); });
      dropzone.addEventListener('dragover', function (e) { e.preventDefault(); dropzone.classList.add('dragover'); });
      dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('dragover'); });
      dropzone.addEventListener('drop', function (e) { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]); });
      fileInput.addEventListener('change', function () { if (fileInput.files.length) handleFile(fileInput.files[0]); });
      downloadBtn.addEventListener('click', function () { if (lastBlob) downloadBlob(lastBlob, lastName); });
    };
  }
  RUNNERS['jpg-to-png'] = buildConvertRunner('png', 'image/png', 'png');
  RUNNERS['png-to-webp'] = buildConvertRunner('webp', 'image/webp', 'webp');

  /* ---------- 11 image-cropper ---------- */
  RUNNERS['image-cropper'] = function (root) {
    var fileInput = $('input[type="file"]', root);
    var dropzone = $('.dropzone', root);
    var aspectSelect = $('[data-aspect]', root);
    var preview = $('[data-preview]', root);
    var status = $('.status-msg', root);
    var downloadBtn = $('[data-download]', root);
    var originalFile = null; var img = null; var lastBlob = null; var lastName = 'cropped';
    var crop = { x: 0, y: 0, w: 0, h: 0, imgW: 0, imgH: 0, ratios: {} };

    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }

    var stage = $('[data-stage]', root) || root;

    function resetCropToAspect() {
      var a = aspectSelect.value;
      if (a === 'free') {
        crop.w = crop.imgW; crop.h = crop.imgH; crop.x = 0; crop.y = 0;
        return;
      }
      var parts = a.split(':');
      var ar = parseInt(parts[0], 10) / parseInt(parts[1], 10);
      var w = crop.imgW, h = Math.round(w / ar);
      if (h > crop.imgH) { h = crop.imgH; w = Math.round(h * ar); }
      crop.w = w; crop.h = h; crop.x = Math.round((crop.imgW - w) / 2); crop.y = Math.round((crop.imgH - h) / 2);
    }

    function draw() {
      var canvas = document.createElement('canvas');
      canvas.width = crop.w; canvas.height = crop.h;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, crop.x, crop.y, crop.w, crop.h, 0, 0, crop.w, crop.h);
      preview.src = canvas.toDataURL('image/png');
      canvasToBlob(canvas, 'image/png').then(function (b) { lastBlob = b; });
    }

    function handleFile(file) {
      if (!file || !/^image\//.test(file.type)) { setStatus('Please choose an image file.', 'err'); return; }
      originalFile = file;
      lastName = file.name.replace(/\.[^.]+$/, '') + '-cropped';
      loadImage(file).then(function (im) {
        img = im;
        crop.imgW = im.naturalWidth; crop.imgH = im.naturalHeight;
        resetCropToAspect();
        draw();
        setStatus('Crop area selected (center). Adjust aspect if needed, then download.', 'ok');
      }).catch(function () { setStatus('Could not read that image.', 'err'); });
    }

    dropzone.addEventListener('click', function () { fileInput.click(); });
    dropzone.addEventListener('dragover', function (e) { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('dragover'); });
    dropzone.addEventListener('drop', function (e) { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]); });
    fileInput.addEventListener('change', function () { if (fileInput.files.length) handleFile(fileInput.files[0]); });
    aspectSelect.addEventListener('change', function () { if (!img) return; resetCropToAspect(); draw(); });
    downloadBtn.addEventListener('click', function () { if (lastBlob) downloadBlob(lastBlob, lastName + '.png'); });
  };

  /* ---------- 12 favicon-generator ---------- */
  RUNNERS['favicon-generator'] = function (root) {
    var fileInput = $('input[type="file"]', root);
    var dropzone = $('.dropzone', root);
    var textIn = $('[data-text]', root);
    var bgIn = $('[data-bg]', root);
    var fgIn = $('[data-fg]', root);
    var sizeSel = $('[data-size]', root);
    var preview = $('[data-preview]', root);
    var status = $('.status-msg', root);
    var downloadBtn = $('[data-download]', root);
    var lastBlob = null; var lastName = 'favicon';
    var useImage = null;

    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }

    function render() {
      var size = parseInt(sizeSel.value, 10) || 32;
      var canvas = document.createElement('canvas');
      canvas.width = size; canvas.height = size;
      var ctx = canvas.getContext('2d');
      if (useImage) {
        ctx.fillStyle = bgIn.value; ctx.fillRect(0, 0, size, size);
        var ratio = Math.min(size / useImage.naturalWidth, size / useImage.naturalHeight) * 0.8;
        var w = useImage.naturalWidth * ratio, h = useImage.naturalHeight * ratio;
        ctx.drawImage(useImage, (size - w) / 2, (size - h) / 2, w, h);
      } else {
        var text = textIn.value || 'C';
        ctx.fillStyle = bgIn.value; ctx.fillRect(0, 0, size, size);
        ctx.fillStyle = fgIn.value;
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.font = 'bold ' + Math.round(size * 0.62) + 'px sans-serif';
        ctx.fillText(text.slice(0, 1).toUpperCase(), size / 2, size / 2 + Math.round(size * 0.04));
      }
      preview.src = canvas.toDataURL('image/png');
      canvasToBlob(canvas, 'image/png').then(function (b) { lastBlob = b; });
    }

    function handleFile(file) {
      if (!file || !/^image\//.test(file.type)) { setStatus('Please choose an image file.', 'err'); return; }
      loadImage(file).then(function (im) { useImage = im; lastName = 'favicon'; render(); setStatus('Favicon rendered from image. Download to save.', 'ok'); })
        .catch(function () { setStatus('Could not read that image.', 'err'); });
    }

    dropzone.addEventListener('click', function () { fileInput.click(); });
    dropzone.addEventListener('dragover', function (e) { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', function () { dropzone.classList.remove('dragover'); });
    dropzone.addEventListener('drop', function (e) { e.preventDefault(); dropzone.classList.remove('dragover'); if (e.dataTransfer.files.length) { useImage = null; handleFile(e.dataTransfer.files[0]); } });
    fileInput.addEventListener('change', function () { if (fileInput.files.length) { useImage = null; handleFile(fileInput.files[0]); } });
    textIn.addEventListener('input', function () { useImage = null; render(); });
    bgIn.addEventListener('input', render);
    fgIn.addEventListener('input', render);
    sizeSel.addEventListener('change', render);
    $('[data-render]', root).addEventListener('click', function () { useImage = null; render(); setStatus('Favicon regenerated.', 'ok'); });
    downloadBtn.addEventListener('click', function () { if (lastBlob) downloadBlob(lastBlob, lastName + '.png'); });
    render();
  };

  /* ---------- 13 percentage-calculator ---------- */
  RUNNERS['percentage-calculator'] = function (root) {
    var mode = $('[data-mode]', root);
    var a = $('[data-a]', root), b = $('[data-b]', root);
    var out1 = $('[data-out1]', root), out2 = $('[data-out2]', root), out3 = $('[data-out3]', root);
    var labelB = $('[data-label-b]', root), labelA = $('[data-label-a]', root);
    function update() {
      var m = mode.value, av = parseFloat(a.value), bv = parseFloat(b.value);
      var needsBothNonZero = (m === 'percent-of' || m === 'is-what');
      if (isNaN(av) || isNaN(bv) || av === 0 || (needsBothNonZero && bv === 0)) {
        out1.textContent = '—'; out2.textContent = '—'; out3.textContent = '—';
        if (!isNaN(av) && av === 0 && (m === 'increase' || m === 'decrease')) {
          out3.textContent = 'Original value must be greater than 0.';
        }
        return;
      }
      if (m === 'percent-of') {
        var r1 = (av / 100) * bv;
        out1.textContent = fmtNum(r1, 6) + (Number.isInteger(r1) ? '' : '');
        out2.textContent = av + '% of ' + fmtNum(bv, 6) + ' = ' + fmtNum(r1, 6);
        out3.textContent = 'Remaining: ' + fmtNum(bv - r1, 6);
        labelA.textContent = 'Percentage (X)';
        labelB.textContent = 'Whole number (Y)';
      } else if (m === 'is-what') {
        var r2 = (av / bv) * 100;
        out1.textContent = fmtNum(r2, 4) + '%';
        out2.textContent = av + ' is ' + fmtNum(r2, 4) + '% of ' + fmtNum(bv, 6);
        out3.textContent = 'Complement: ' + fmtNum(100 - r2, 4) + '%';
        labelA.textContent = 'First value (X)';
        labelB.textContent = 'Second value (Y)';
      } else {
        var base = m === 'increase' ? bv - av : av - bv;
        var pct = (base / av) * 100;
        out1.textContent = fmtNum(pct, 4) + '% ' + (m === 'increase' ? 'increase' : 'decrease');
        out2.textContent = 'Difference: ' + fmtNum(Math.abs(av - bv), 6);
        out3.textContent = m === 'increase' ? 'Result is ' + fmtNum(bv, 6) + ' (larger)' : 'Result is ' + fmtNum(bv, 6) + ' (smaller)';
        labelA.textContent = 'Original value';
        labelB.textContent = 'New value';
      }
    }
    mode.addEventListener('change', update);
    a.addEventListener('input', update);
    b.addEventListener('input', update);
    var resetBtn = root.querySelector('#pc-reset');
    if (resetBtn) resetBtn.addEventListener('click', function () {
      mode.value = 'percent-of'; a.value = '15'; b.value = '240'; update();
    });
    update();
  };

  /* ---------- 14 age-calculator ---------- */
  RUNNERS['age-calculator'] = function (root) {
    var birth = $('[data-birth]', root), target = $('[data-target]', root);
    var outs = { y: null, m: null, d: null, totalM: null, totalW: null, totalD: null };
    ['y','m','d','totalM','totalW','totalD'].forEach(function (k) { outs[k] = $('[data-out="' + k + '"]', root); });
    function parseDate(v) {
      if (!v) return null;
      var p = v.split('-');
      return new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
    }
    function update() {
      var from = parseDate(birth.value), to = parseDate(target.value);
      if (!from || !to || isNaN(from.getTime()) || isNaN(to.getTime()) || to < from) {
        outs.y.textContent = outs.m.textContent = outs.d.textContent = outs.totalM.textContent = outs.totalW.textContent = outs.totalD.textContent = '—';
        return;
      }
      var y = to.getFullYear() - from.getFullYear();
      var m = to.getMonth() - from.getMonth();
      var d = to.getDate() - from.getDate();
      if (d < 0) {
        m--;
        var prev = new Date(to.getFullYear(), to.getMonth(), 0).getDate();
        d += prev;
      }
      if (m < 0) { y--; m += 12; }
      var totalD = Math.floor((to - new Date(from.getFullYear(), from.getMonth(), from.getDate())) / 86400000);
      outs.y.textContent = fmtNum(y, 0);
      outs.m.textContent = fmtNum(m, 0);
      outs.d.textContent = fmtNum(d, 0);
      outs.totalM.textContent = fmtNum(Math.floor(totalD / 30.437), 0);
      outs.totalW.textContent = fmtNum(Math.floor(totalD / 7), 0);
      outs.totalD.textContent = fmtNum(totalD, 0);
    }
    birth.addEventListener('change', update);
    target.addEventListener('change', update);
    var now = new Date();
    target.value = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    update();
  };

  /* ---------- 15 date-difference ---------- */
  RUNNERS['date-difference'] = function (root) {
    var start = $('[data-start]', root), end = $('[data-end]', root), incl = $('[data-include]', root);
    var outs = { d: null, w: null, m: null, y: null, desc: null };
    ['d','w','m','y','desc'].forEach(function (k) { outs[k] = $('[data-out="' + k + '"]', root); });
    function parseDate(v) {
      if (!v) return null;
      var p = v.split('-');
      return new Date(parseInt(p[0], 10), parseInt(p[1], 10) - 1, parseInt(p[2], 10));
    }
    function update() {
      var s = parseDate(start.value), e = parseDate(end.value);
      if (!s || !e || isNaN(s.getTime()) || isNaN(e.getTime())) {
        outs.d.textContent = outs.w.textContent = outs.m.textContent = outs.y.textContent = outs.desc.textContent = '—';
        return;
      }
      var diff = Math.floor((e - s) / 86400000);
      if (incl.checked) {
        if (diff >= 0) diff += 1;
        else diff -= 1;
      }
      var sign = diff < 0 ? '-' : '';
      var ad = Math.abs(diff);
      outs.d.textContent = sign + fmtNum(ad, 0);
      outs.w.textContent = sign + fmtNum(ad / 7, 2);
      outs.m.textContent = sign + fmtNum(ad / 30.437, 2);
      outs.y.textContent = sign + fmtNum(ad / 365.25, 2);
      outs.desc.textContent = (incl.checked ? 'Including' : 'Excluding') + ' the end date • ' + (diff === 0 ? 'same day' : Math.abs(diff) + ' day' + (Math.abs(diff) === 1 ? '' : 's'));
    }
    start.addEventListener('change', update);
    end.addEventListener('change', update);
    incl.addEventListener('change', update);
    var now = new Date();
    var iso = now.getFullYear() + '-' + String(now.getMonth() + 1).padStart(2, '0') + '-' + String(now.getDate()).padStart(2, '0');
    end.value = iso;
    update();
  };

  /* ---------- 16 unit-converter ---------- */
  RUNNERS['unit-converter'] = function (root) {
    var cat = $('[data-category]', root), from = $('[data-from]', root), to = $('[data-to]', root), valueIn = $('[data-value]', root);
    var out = $('[data-result]', root), outSub = $('[data-result-sub]', root);
    var CATS = {
      length: { label: 'Length', units: { mm: ['Millimeters', 0.001], cm: ['Centimeters', 0.01], m: ['Meters', 1], km: ['Kilometers', 1000], in: ['Inches', 0.0254], ft: ['Feet', 0.3048], yd: ['Yards', 0.9144], mi: ['Miles', 1609.344] } },
      mass: { label: 'Mass', units: { mg: ['Milligrams', 0.000001], g: ['Grams', 0.001], kg: ['Kilograms', 1], t: ['Metric tons', 1000], oz: ['Ounces', 0.028349523125], lb: ['Pounds', 0.45359237], st: ['Stones', 6.35029318] } },
      temperature: { label: 'Temperature', units: { C: ['Celsius', 0], F: ['Fahrenheit', 0], K: ['Kelvin', 0] } },
      speed: { label: 'Speed', units: { mps: ['Meters/sec', 1], kmh: ['km/h', 0.2777778], mph: ['mph', 0.44704], kn: ['Knots', 0.5144444], fps: ['ft/sec', 0.3048] } },
      area: { label: 'Area', units: { m2: ['Square meters', 1], km2: ['Square km', 1000000], ft2: ['Square feet', 0.09290304], yd2: ['Square yards', 0.83612736], ac: ['Acres', 4046.8564224], ha: ['Hectares', 10000], mi2: ['Square miles', 2589988.110336] } },
      volume: { label: 'Volume', units: { ml: ['Milliliters', 0.000001], l: ['Liters', 0.001], m3: ['Cubic meters', 1], tsp: ['Teaspoons', 0.00000492892], tbsp: ['Tablespoons', 0.0000147868], cup: ['Cups (US)', 0.000236588], floz: ['Fluid ounces', 0.0000295735], gal: ['Gallons (US)', 0.00378541] } }
    };
    function tempConvert(value, fromUnit, toUnit) {
      var c;
      if (fromUnit === 'C') c = value;
      else if (fromUnit === 'F') c = (value - 32) * 5 / 9;
      else c = value - 273.15;
      if (toUnit === 'C') return c;
      else if (toUnit === 'F') return c * 9 / 5 + 32;
      else return c + 273.15;
    }
    function fillUnits() {
      var c = CATS[cat.value].units;
      var fromSel = from, toSel = to;
      fromSel.innerHTML = ''; toSel.innerHTML = '';
      for (var key in c) {
        fromSel.appendChild(new Option(c[key][0] + ' (' + key + ')', key));
        toSel.appendChild(new Option(c[key][0] + ' (' + key + ')', key));
      }
      toSel.value = fromSel.value === 'm' ? 'ft' : (fromSel.value === 'C' ? 'F' : fromSel.options.length > 1 ? fromSel.options[1].value : fromSel.value);
      convert();
    }
    function convert() {
      var v = parseFloat(valueIn.value);
      if (isNaN(v)) { out.textContent = '—'; outSub.textContent = 'Enter a valid number.'; return; }
      var c = CATS[cat.value];
      var fromUnit = from.value, toUnit = to.value;
      var result;
      if (cat.value === 'temperature') result = tempConvert(v, fromUnit, toUnit);
      else result = (v * c.units[fromUnit][1]) / c.units[toUnit][1];
      out.textContent = fmtNum(result, 8);
      outSub.textContent = v + ' ' + fromUnit + ' = ' + fmtNum(result, 8) + ' ' + toUnit;
    }
    cat.addEventListener('change', fillUnits);
    from.addEventListener('change', convert);
    to.addEventListener('change', convert);
    valueIn.addEventListener('input', convert);
    fillUnits();
  };

  /* ---------- 17 bmi-calculator ---------- */
  RUNNERS['bmi-calculator'] = function (root) {
    var sys = $('[data-system]', root), h1 = $('[data-h1]', root), h2 = $('[data-h2]', root), w = $('[data-weight]', root);
    var out = $('[data-result]', root), catOut = $('[data-result-sub]', root);
    function kg() {
      var weight = parseFloat(w.value);
      if (sys.value === 'metric') return weight;
      return weight * 0.45359237;
    }
    function meters() {
      if (sys.value === 'metric') return parseFloat(h1.value) / 100;
      var ft = parseFloat(h1.value) || 0, inch = parseFloat(h2.value) || 0;
      return (ft * 12 + inch) * 0.0254;
    }
    function update() {
      var m = meters(), k = kg();
      if (!m || !k || m <= 0 || k <= 0) { out.textContent = '—'; catOut.textContent = 'Enter height and weight.'; return; }
      var bmi = k / (m * m);
      var cat;
      if (bmi < 18.5) cat = 'Underweight';
      else if (bmi < 25) cat = 'Normal weight';
      else if (bmi < 30) cat = 'Overweight';
      else cat = 'Obesity';
      out.textContent = fmtNum(bmi, 1);
      catOut.textContent = cat + ' • BMI is a screening measure, not a medical diagnosis.';
    }
    sys.addEventListener('change', function () {
      var metric = sys.value === 'metric';
      document.querySelector('[data-ft-label]').style.display = metric ? 'none' : '';
      document.querySelector('[data-ft]').style.display = metric ? 'none' : '';
      document.querySelector('[data-cm]').style.display = metric ? '' : 'none';
      update();
    });
    h1.addEventListener('input', update);
    h2.addEventListener('input', update);
    w.addEventListener('input', update);
    update();
  };

  /* ---------- 18 discount-calculator ---------- */
  RUNNERS['discount-calculator'] = function (root) {
    var price = $('[data-price]', root), disc = $('[data-discount]', root), tax = $('[data-tax]', root), useTax = $('[data-use-tax]', root);
    var out1 = $('[data-final]', root), out2 = $('[data-saved]', root), out3 = $('[data-detail]', root);
    function update() {
      var p = parseFloat(price.value), d = parseFloat(disc.value);
      if (isNaN(p) || isNaN(d)) { out1.textContent = '—'; out2.textContent = '—'; out3.textContent = 'Enter price and discount percentage.'; return; }
      var discount = p * d / 100;
      var final = p - discount;
      if (useTax.checked) {
        var t = parseFloat(tax.value) || 0;
        final = final * (1 + t / 100);
      }
      out1.textContent = '$' + fmtNum(final, 2);
      out2.textContent = 'You save $' + fmtNum(discount, 2) + ' (' + fmtNum(d, 2) + '% of $' + fmtNum(p, 2) + ')';
      out3.textContent = 'Discounted price before tax: $' + fmtNum(p - discount, 2) + (useTax.checked ? ' • plus tax' : '');
    }
    price.addEventListener('input', update);
    disc.addEventListener('input', update);
    tax.addEventListener('input', update);
    useTax.addEventListener('change', function () { $('[data-tax-field]', root).style.display = useTax.checked ? '' : 'none'; update(); });
    update();
  };

  /* ---------- 19 password-generator ---------- */
  RUNNERS['password-generator'] = function (root) {
    var len = $('[data-length]', root), lenVal = $('[data-length-val]', root);
    var upper = $('[data-upper]', root), lower = $('[data-lower]', root), nums = $('[data-nums]', root), syms = $('[data-syms]', root);
    var output = $('[data-output]', root), strength = $('[data-strength]', root);
    var meter = $('[data-pw-meter]', root);
    var SYMBOLS = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    var UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', LOWER = 'abcdefghijklmnopqrstuvwxyz', NUMS = '0123456789';
    function entropyEstimate() {
      var pool = 0, sets = 0;
      if (upper.checked) { pool += UPPER.length; sets++; }
      if (lower.checked) { pool += LOWER.length; sets++; }
      if (nums.checked) { pool += NUMS.length; sets++; }
      if (syms.checked) { pool += SYMBOLS.length; sets++; }
      if (!sets) return 0;
      var l = parseInt(len.value, 10) || 1;
      return Math.round(l * Math.log2(pool));
    }
    function generate() {
      var l = parseInt(len.value, 10) || 16;
      if (l < 4) l = 4; if (l > 128) l = 128;
      var groups = [];
      if (upper.checked) groups.push(UPPER);
      if (lower.checked) groups.push(LOWER);
      if (nums.checked) groups.push(NUMS);
      if (syms.checked) groups.push(SYMBOLS);
      if (!groups.length) { output.value = 'Select at least one character type'; strength.textContent = ''; return; }
      var pool = groups.join('');
      var chars = [];
      // guarantee at least one char from each selected group
      for (var g = 0; g < groups.length && g < l; g++) {
        chars.push(groups[g].charAt(secureRandomInt(groups[g].length)));
      }
      for (var i = chars.length; i < l; i++) {
        chars.push(pool.charAt(secureRandomInt(pool.length)));
      }
      // unbiased Fisher-Yates shuffle with crypto randomness
      for (var j = chars.length - 1; j > 0; j--) {
        var k = secureRandomInt(j + 1);
        var tmp = chars[j]; chars[j] = chars[k]; chars[k] = tmp;
      }
      output.value = chars.join('');
      var bits = entropyEstimate();
      var level = bits < 45 ? 1 : (bits < 70 ? 2 : (bits < 100 ? 3 : 4));
      var label = ['', 'Weak', 'Fair', 'Strong', 'Very strong'][level];
      strength.textContent = label + ' · ~' + bits + ' bits';
      if (meter) {
        var segs = meter.querySelectorAll('i');
        for (var s = 0; s < segs.length; s++) {
          segs[s].className = s < level ? 'on' + level : '';
        }
      }
    }
    len.addEventListener('input', function () { lenVal.textContent = len.value; generate(); });
    [upper, lower, nums, syms].forEach(function (c) { c.addEventListener('change', generate); });
    $('[data-generate]', root).addEventListener('click', generate);
    $('[data-copy]', root).addEventListener('click', function () { copyFrom(root, '[data-output]', '[data-copy]'); });
    generate();
  };

  /* ---------- 20 qr-code-generator ---------- */
  RUNNERS['qr-code-generator'] = function (root) {
    var input = $('input[type="text"]', root) || $('input[type="url"]', root);
    var sizeSel = $('[data-size]', root);
    var canvas = $('[data-canvas]', root);
    var status = $('.status-msg', root);
    var downloadBtn = $('[data-download]', root);
    var lastUrl = null;
    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }
    function render() {
      var text = input.value.trim();
      if (!text) { setStatus('Type a URL or text to generate a QR code.', 'warn'); return; }
      if (text.length > 1500) { setStatus('Input is too long — QR codes over ~1500 characters become unreadable.', 'err'); return; }
      if (!window.qrcode) { setStatus('QR library failed to load.', 'err'); return; }
      var qr = qrcode(0, 'M');
      qr.addData(text);
      qr.make();
      var size = parseInt(sizeSel.value, 10) || 256;
      var modCount = qr.getModuleCount();
      canvas.width = size; canvas.height = size;
      var ctx = canvas.getContext('2d');
      var quiet = 4;
      var cell = Math.floor(size / (modCount + quiet * 2));
      var offset = Math.floor((size - cell * modCount) / 2);
      ctx.fillStyle = '#ffffff'; ctx.fillRect(0, 0, size, size);
      ctx.fillStyle = '#0f172a';
      for (var r = 0; r < modCount; r++) {
        for (var c = 0; c < modCount; c++) {
          if (qr.isDark(r, c)) ctx.fillRect(c * cell + offset, r * cell + offset, cell, cell);
        }
      }
      lastUrl = canvas.toDataURL('image/png');
      setStatus('QR code ready. Download the PNG for printing or embedding.', 'ok');
    }
    input.addEventListener('input', render);
    sizeSel.addEventListener('change', render);
    downloadBtn.addEventListener('click', function () {
      if (!lastUrl) return;
      var a = document.createElement('a');
      a.href = lastUrl; a.download = 'qrcode-' + (input.value.trim().replace(/[^a-z0-9]/gi, '-').slice(0, 30) || 'code') + '.png';
      document.body.appendChild(a); a.click(); setTimeout(function () { document.body.removeChild(a); }, 100);
    });
    render();
  };

  /* ---------- 21 random-number-generator ---------- */
  RUNNERS['random-number-generator'] = function (root) {
    var min = $('[data-min]', root), max = $('[data-max]', root), count = $('[data-count]', root);
    var unique = $('[data-unique]', root), decimals = $('[data-decimals]', root);
    var output = $('[data-output]', root);
    function run() {
      var lo = parseFloat(min.value) || 0, hi = parseFloat(max.value) || 100;
      var n = parseInt(count.value, 10) || 1;
      var dec = parseInt(decimals.value, 10) || 0;
      if (lo > hi) { var t = lo; lo = hi; hi = t; }
      if (n < 1) n = 1; if (n > 1000) n = 1000;
      var needUnique = unique.checked && dec === 0;
      if (needUnique && (hi - lo + 1) < n) {
        output.value = 'Range too small for ' + n + ' unique integers.';
        return;
      }
      var results = [];
      var seen = {};
      var guard = 0;
      while (results.length < n && guard < 100000) {
        guard++;
        var r;
        if (dec > 0) {
          // Uniform, cryptographically secure float in [lo, hi], scaled to `dec` places.
          var u = new Uint32Array(1); crypto.getRandomValues(u);
          r = lo + (u[0] / 4294967296) * (hi - lo);
          r = parseFloat(r.toFixed(dec));
        } else {
          var span = hi - lo + 1;
          r = lo + secureRandomInt(span);
        }
        if (needUnique) {
          var key = String(r);
          if (seen[key]) continue;
          seen[key] = true;
        }
        results.push(r);
      }
      output.value = results.join(', ');
    }
    $('[data-generate]', root).addEventListener('click', run);
    run();
  };

  /* ---------- 22 random-name-picker ---------- */
  RUNNERS['random-name-picker'] = function (root) {
    var ta = $('textarea', root), removePick = $('[data-remove]', root);
    var result = $('[data-result]', root), historyList = $('[data-history]', root);
    var picked = [];
    function names() {
      return ta.value.split('\n').map(function (s) { return s.trim(); }).filter(Boolean);
    }
    function pick() {
      var list = names();
      var remaining = [];
      if (removePick.checked) {
        remaining = list.filter(function (n) { return picked.indexOf(n) === -1; });
        if (!remaining.length) {
          result.textContent = 'All names have been picked. Reset to start over.';
          return;
        }
      } else {
        remaining = list;
      }
      if (!remaining.length) { result.textContent = 'Add at least one name.'; return; }
      var name = remaining[secureRandomInt(remaining.length)];
      result.textContent = name;
      picked.push(name);
      var li = document.createElement('li');
      li.textContent = name;
      historyList.prepend(li);
    }
    $('[data-pick]', root).addEventListener('click', pick);
    $('[data-reset]', root).addEventListener('click', function () { picked = []; historyList.innerHTML = ''; result.textContent = '—'; });
    ta.addEventListener('input', function () { picked = []; historyList.innerHTML = ''; });
  };

  /* ---------- 23 uuid-generator ---------- */
  RUNNERS['uuid-generator'] = function (root) {
    var count = $('[data-count]', root), output = $('[data-output]', root);
    function uuidV4() {
      if (crypto.randomUUID) return crypto.randomUUID();
      var bytes = new Uint8Array(16);
      crypto.getRandomValues(bytes);
      bytes[6] = (bytes[6] & 0x0f) | 0x40;
      bytes[8] = (bytes[8] & 0x3f) | 0x80;
      var hex = Array.from(bytes, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
      return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-' + hex.slice(16, 20) + '-' + hex.slice(20);
    }
    function generate() {
      var n = parseInt(count.value, 10) || 1;
      if (n < 1) n = 1; if (n > 20) n = 20;
      var out = [];
      for (var i = 0; i < n; i++) out.push(uuidV4());
      output.value = out.join('\n');
    }
    $('[data-generate]', root).addEventListener('click', generate);
    generate();
  };

  /* ---------- 24 json-formatter ---------- */
  RUNNERS['json-formatter'] = function (root) {
    var input = $('[data-input]', root), output = $('[data-output]', root), indent = $('[data-indent]', root);
    var status = $('.status-msg', root);
    function setStatus(msg, type) { status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }
    function doParse() {
      var text = input.value.trim();
      if (!text) { setStatus('Paste some JSON to format or validate.', 'warn'); return null; }
      try { return JSON.parse(text); }
      catch (e) {
        var msg = e.message || 'Invalid JSON';
        var pos = (e.message || '').match(/position\s+(\d+)/);
        setStatus('Invalid JSON: ' + msg + (pos ? ' (at position ' + pos[1] + ')' : ''), 'err');
        return null;
      }
    }
    function format() {
      var obj = doParse();
      if (obj === null) return;
      var sp = indent.value === 'tab' ? '\t' : parseInt(indent.value, 10) || 2;
      var json = JSON.stringify(obj, null, sp);
      if (indent.value === 'min') json = JSON.stringify(obj);
      output.value = json;
      setStatus('Formatted successfully.' + (indent.value === 'min' ? ' (minified)' : ''), 'ok');
    }
    $('[data-format]', root).addEventListener('click', format);
    $('[data-validate]', root).addEventListener('click', function () {
      var obj = doParse();
      if (obj !== null) setStatus('Valid JSON. Ready to format or minify.', 'ok');
    });
    $('[data-clear]', root).addEventListener('click', function () { input.value = ''; output.value = ''; status.className = 'status-msg'; status.textContent = ''; status.style.display = 'none'; });
    $('[data-copy]', root).addEventListener('click', function () { copyFrom(root, '[data-output]', '[data-copy]'); });
  };

  /* ---------- 25 countdown-timer ---------- */
  function buildTimer(countdown) {
    return function (root) {
      var hh = $('[data-hh]', root), mm = $('[data-mm]', root), ss = $('[data-ss]', root);
      var display = $('[data-display]', root);
      var startBtn = $('[data-start]', root), pauseBtn = $('[data-pause]', root), resetBtn = $('[data-reset]', root);
      var status = $('.status-msg', root);
      var totalMs = 0, remaining = 0, endTs = 0, running = false, raf = 0;
      var phase = countdown ? 'countdown' : 'stopwatch';
      function setStatus(msg, type) { if (!status) return; status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }
      function fmt(ms) {
        var sign = ms < 0 ? '-' : '';
        ms = Math.abs(ms);
        var h = Math.floor(ms / 3600000), m = Math.floor(ms % 3600000 / 60000), s = Math.floor(ms % 60000 / 1000);
        if (phase === 'stopwatch') {
          var cs = Math.floor(ms % 1000 / 10);
          return sign + String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0') + '.' + String(cs).padStart(2, '0');
        }
        return sign + String(h).padStart(2, '0') + ':' + String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
      }
      function tick() {
        if (!running) return;
        var now = Date.now();
        if (phase === 'countdown') {
          remaining = Math.max(0, endTs - now);
          display.textContent = fmt(remaining);
          if (remaining <= 0) {
            running = false;
            cancelAnimationFrame(raf);
            startBtn.disabled = false; pauseBtn.disabled = true;
            setStatus('Time is up! 🎉', 'ok');
            return;
          }
        } else {
          remaining = now - startTs;
          display.textContent = fmt(remaining);
        }
        raf = requestAnimationFrame(tick);
      }
      var startTs = 0;
      function start() {
        if (running) return;
        if (phase === 'countdown') {
          if (remaining <= 0) {
            var h = parseInt(hh.value, 10) || 0, m = parseInt(mm.value, 10) || 0, s = parseInt(ss.value, 10) || 0;
            totalMs = (h * 3600 + m * 60 + s) * 1000;
            if (totalMs <= 0) { setStatus('Set a time greater than zero.', 'err'); return; }
            remaining = totalMs;
          }
          endTs = Date.now() + remaining;
        } else {
          startTs = Date.now() - remaining;
        }
        running = true;
        startBtn.disabled = true; pauseBtn.disabled = false;
        setStatus('', '');
        raf = requestAnimationFrame(tick);
      }
      function pause() {
        if (!running) return;
        running = false;
        cancelAnimationFrame(raf);
        if (phase === 'countdown') remaining = Math.max(0, endTs - Date.now());
        startBtn.disabled = false; pauseBtn.disabled = true;
        setStatus(phase === 'countdown' ? 'Paused.' : 'Stopped.', 'warn');
      }
      function reset() {
        running = false; cancelAnimationFrame(raf);
        if (phase === 'countdown') { remaining = 0; totalMs = 0; display.textContent = '00:00:00'; }
        else { remaining = 0; display.textContent = '00:00:00.00'; }
        startBtn.disabled = false; pauseBtn.disabled = true;
        setStatus('', '');
      }
      startBtn.addEventListener('click', start);
      pauseBtn.addEventListener('click', pause);
      resetBtn.addEventListener('click', reset);
      if (phase === 'countdown') {
        [hh, mm, ss].forEach(function (el) { if (el) el.addEventListener('change', reset); });
      }
      reset();
    };
  }
  RUNNERS['countdown-timer'] = buildTimer(true);
  RUNNERS['stopwatch'] = buildTimer(false);

  /* ---------- 27 pomodoro-timer ---------- */
  RUNNERS['pomodoro-timer'] = function (root) {
    var focus = $('[data-focus]', root), short = $('[data-short]', root), long = $('[data-long]', root);
    var display = $('[data-display]', root), phaseLabel = $('[data-phase]', root), cycleOut = $('[data-cycles]', root);
    var startBtn = $('[data-start]', root), pauseBtn = $('[data-pause]', root), skipBtn = $('[data-skip]', root), resetBtn = $('[data-reset]', root);
    var status = $('.status-msg', root);
    var state = { phase: 'focus', cycle: 0, remainingMs: 25 * 60000, totalMs: 25 * 60000, endTs: 0, running: false, raf: 0, lastChange: 0 };
    function setStatus(msg, type) { if (!status) return; status.textContent = msg || ''; status.className = 'status-msg ' + (type || 'ok'); status.style.display = msg ? 'block' : 'none'; }
    function currentLen() {
      var f = parseInt(focus.value, 10) || 25, s = parseInt(short.value, 10) || 5, l = parseInt(long.value, 10) || 15;
      if (state.phase === 'focus') return f * 60000;
      if (state.phase === 'short') return s * 60000;
      return l * 60000;
    }
    function fmt(ms) {
      var m = Math.floor(ms / 60000), s = Math.floor(ms % 60000 / 1000);
      return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    }
    function tick() {
      if (!state.running) return;
      state.remainingMs = Math.max(0, state.endTs - Date.now());
      display.textContent = fmt(state.remainingMs);
      if (state.remainingMs <= 0) {
        advance();
        state.running = true;
        state.endTs = Date.now() + state.remainingMs;
        setStatus('Phase finished!', 'ok');
      }
      if (state.running) state.raf = requestAnimationFrame(tick);
    }
    function advance() {
      if (state.phase === 'focus') {
        state.cycle++;
        state.phase = state.cycle % 4 === 0 ? 'long' : 'short';
      } else {
        state.phase = 'focus';
      }
      state.totalMs = currentLen();
      state.remainingMs = state.totalMs;
      renderPhase();
    }
    function renderPhase() {
      phaseLabel.textContent = state.phase === 'focus' ? 'Focus' : (state.phase === 'short' ? 'Short break' : 'Long break');
      cycleOut.textContent = 'Completed focus sessions: ' + state.cycle;
      display.textContent = fmt(state.remainingMs);
    }
    function start() {
      if (state.running) return;
      if (state.remainingMs <= 0) { state.remainingMs = currentLen(); state.totalMs = state.remainingMs; }
      state.endTs = Date.now() + state.remainingMs;
      state.running = true;
      startBtn.disabled = true; pauseBtn.disabled = false;
      setStatus('', '');
      state.raf = requestAnimationFrame(tick);
    }
    function pause() {
      if (!state.running) return;
      state.running = false; cancelAnimationFrame(state.raf);
      state.remainingMs = Math.max(0, state.endTs - Date.now());
      startBtn.disabled = false; pauseBtn.disabled = true;
      setStatus('Paused.', 'warn');
    }
    function skip() { advance(); renderPhase(); setStatus('Skipped to next phase.', 'warn'); }
    function reset() {
      state.running = false; cancelAnimationFrame(state.raf);
      state.phase = 'focus'; state.cycle = 0;
      state.totalMs = currentLen(); state.remainingMs = state.totalMs;
      startBtn.disabled = false; pauseBtn.disabled = true;
      renderPhase(); setStatus('', '');
    }
    startBtn.addEventListener('click', start);
    pauseBtn.addEventListener('click', pause);
    skipBtn.addEventListener('click', skip);
    resetBtn.addEventListener('click', reset);
    [focus, short, long].forEach(function (el) { if (el) el.addEventListener('change', reset); });
    reset();
  };

  /* ---------- 28 time-zone-converter ---------- */
  RUNNERS['time-zone-converter'] = function (root) {
    var sourceTz = $('[data-source-tz]', root), targetTz = $('[data-target-tz]', root);
    var dt = $('[data-datetime]', root);
    var out = $('[data-result]', root), outSub = $('[data-result-sub]', root);
    var ZONES = [];
    try { ZONES = Intl.supportedValuesOf('timeZone'); }
    catch (e) {
      var fallback = ['UTC','America/New_York','America/Chicago','America/Denver','America/Los_Angeles','Europe/London','Europe/Paris','Europe/Berlin','Asia/Dubai','Asia/Singapore','Asia/Shanghai','Asia/Tokyo','Australia/Sydney','Pacific/Auckland'];
      ZONES = fallback;
    }
    (function fill() {
      var localTz = Intl.DateTimeFormat().resolvedOptions().timeZone;
      [sourceTz, targetTz].forEach(function (sel) {
        sel.innerHTML = '';
        ZONES.forEach(function (z) { sel.appendChild(new Option(z, z)); });
      });
      sourceTz.value = localTz;
      targetTz.value = ZONES.indexOf('Europe/London') !== -1 ? 'Europe/London' : (localTz === 'UTC' ? 'America/New_York' : 'UTC');
    })();
    function convert() {
      var v = dt.value;
      if (!v) { out.textContent = '—'; outSub.textContent = 'Pick a date and time.'; return; }
      var d = new Date(v);
      if (isNaN(d.getTime())) { out.textContent = '—'; outSub.textContent = 'Invalid date/time.'; return; }
      // Build a date in source zone
      var parts = v.split('T');
      var dateParts = parts[0].split('-');
      var timeParts = (parts[1] || '00:00').split(':');
      var sourceDate = new Date(Date.UTC(
        parseInt(dateParts[0], 10),
        parseInt(dateParts[1], 10) - 1,
        parseInt(dateParts[2], 10),
        parseInt(timeParts[0], 10),
        parseInt(timeParts[1], 10),
        parseInt(timeParts[2] || '0', 10)
      ));
      // Offset of source zone at that instant (using Intl)
      var sourceOffset = getOffset(sourceTz.value, sourceDate);
      var instant = sourceDate.getTime() - sourceOffset;
      var targetOffset = getOffset(targetTz.value, new Date(instant));
      var converted = new Date(instant + targetOffset);
      out.textContent = converted.toLocaleString('en-US', { timeZone: 'UTC', year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true });
      outSub.textContent = 'in ' + targetTz.value + ' (UTC' + (targetOffset >= 0 ? '+' : '') + (targetOffset / 3600000) + 'h) • Source ' + sourceTz.value + ' (UTC' + (sourceOffset >= 0 ? '+' : '') + (sourceOffset / 3600000) + 'h)';
    }
    function getOffset(tz, date) {
      var dtf = new Intl.DateTimeFormat('en-US', { timeZone: tz, hour12: false, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit' });
      var parts = dtf.formatToParts(date);
      var map = {};
      parts.forEach(function (p) { map[p.type] = p.value; });
      var asUTC = Date.UTC(+map.year, +map.month - 1, +map.day, +map.hour % 24, +map.minute, +map.second);
      return asUTC - date.getTime();
    }
    sourceTz.addEventListener('change', convert);
    targetTz.addEventListener('change', convert);
    dt.addEventListener('change', convert);
    var now = new Date();
    var localIso = new Date(now.getTime() - now.getTimezoneOffset() * 60000).toISOString().slice(0, 16);
    dt.value = localIso;
    convert();
  };

  /* ---------- 29 online-counter ---------- */
  function buildCounter(clickStyle) {
    return function (root) {
      var display = $('[data-display]', root);
      var step = $('[data-step]', root);
      var persist = $('[data-persist]', root);
      var KEY = 'calchub-counter-' + (clickStyle ? 'click' : 'online');
      var count = 0;
      function load() {
        if (persist && persist.checked) {
          try { count = parseInt(localStorage.getItem(KEY) || '0', 10) || 0; } catch (e) { count = 0; }
        } else { count = 0; }
        render();
      }
      function save() {
        if (persist && persist.checked) {
          try { localStorage.setItem(KEY, String(count)); } catch (e) {}
        }
      }
      function render() { display.textContent = fmtNum(count, 0); }
      function add() { count += parseInt(step.value, 10) || 1; render(); save(); }
      function sub() { count -= parseInt(step.value, 10) || 1; render(); save(); }
      function reset() { count = 0; render(); save(); }
      if (clickStyle) {
        var big = $('[data-bigbtn]', root);
        big.addEventListener('click', add);
        if (persist) persist.addEventListener('change', load);
        $('[data-reset]', root).addEventListener('click', reset);
      } else {
        $('[data-plus]', root).addEventListener('click', add);
        $('[data-minus]', root).addEventListener('click', sub);
        $('[data-reset]', root).addEventListener('click', reset);
        if (persist) persist.addEventListener('change', load);
        var kd = function (e) {
          if (e.key === '+' || e.key === '=') add();
          else if (e.key === '-' || e.key === '_') sub();
          else if (e.key === 'r' || e.key === 'R') reset();
        };
        document.addEventListener('keydown', kd);
      }
      load();
    };
  }
  RUNNERS['online-counter'] = buildCounter(false);
  RUNNERS['click-counter'] = buildCounter(true);

  /* =========================================================
     Mount
     ========================================================= */
  function mountTools() {
    $$('[data-tool]', document).forEach(function (el) {
      var name = el.getAttribute('data-tool');
      if (RUNNERS[name]) {
        try { RUNNERS[name](el); }
        catch (e) {
          if (window.console) console.error('Tool runner error: ' + name, e);
        }
      }
    });
  }
  // Scripts are deferred, so DOMContentLoaded may already have fired by the
  // time this runs. Handle both states so runners always mount.
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountTools);
  } else {
    mountTools();
  }
})();