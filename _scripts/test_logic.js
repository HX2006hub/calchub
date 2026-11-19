/* Offline, pure-logic regression tests. No DOM, no network.
   Run: node _scripts/test_logic.js
   Logic mirrors assets/js/tools.js; keep in sync when formulas change. */
'use strict';
var pass = 0, fail = 0;
function ok(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; console.error('FAIL:', name, detail === undefined ? '' : detail); }
}
function near(a, b, eps) { return Math.abs(a - b) <= (eps || 1e-9); }

/* ---- word / sentence / paragraph counting (mirrors tools.js helpers) ---- */
function countWords(s) {
  var m = s.trim().match(/[\u00C0-\u024F\u4e00-\u9fff\u3040-\u30ff\w]+(?:['’-][\u00C0-\u024F\u4e00-\u9fff\u3040-\u30ff\w]+)*/g);
  return m ? m.length : 0;
}
function countSentences(s) {
  var m = s.trim().match(/[^.!?]+[.!?]+(?=\s|$)|[^.!?]+$/g);
  return m ? m.length : 0;
}
ok('words: empty', countWords('') === 0);
ok('words: basic', countWords('one two three') === 3);
ok('words: hyphen/apostrophe kept together', countWords("don't well-known state-of-the-art") === 3, countWords("don't well-known state-of-the-art"));
ok('words: unicode accents', countWords('café naïve résumé') === 3, countWords('café naïve résumé'));
ok('sentences: empty', countSentences('') === 0);
ok('sentences: three', countSentences('One. Two! Three?') === 3, countSentences('One. Two! Three?'));

/* ---- percentage ---- */
function pctOf(x, y) { return x / 100 * y; }
function isWhat(x, y) { return y === 0 ? NaN : x / y * 100; }
function change(orig, next, kind) { return orig === 0 ? NaN : ((kind === 'increase' ? next - orig : orig - next) / orig) * 100; }
ok('pct-of: 20% of 150', near(pctOf(20, 150), 30));
ok('is-what: 30 of 150', near(isWhat(30, 150), 20));
ok('is-what: divide by zero guarded', isNaN(isWhat(10, 0)));
ok('increase: 100 -> 120', near(change(100, 120, 'increase'), 20));
ok('decrease: 120 -> 100', near(change(120, 100, 'decrease'), 16.6667, 1e-4), change(120, 100, 'decrease'));
ok('change: original zero guarded', isNaN(change(0, 10, 'increase')));

/* ---- age (years/months/days, leap-safe) ---- */
function ymd(from, to) {
  var y = to.getFullYear() - from.getFullYear();
  var m = to.getMonth() - from.getMonth();
  var d = to.getDate() - from.getDate();
  if (d < 0) { m--; d += new Date(to.getFullYear(), to.getMonth(), 0).getDate(); }
  if (m < 0) { y--; m += 12; }
  return [y, m, d];
}
function D(y, m, d) { return new Date(y, m - 1, d); }
function arrEq(a, b) { return a.length === b.length && a.every(function (v, i) { return v === b[i]; }); }
ok('age: exact birthday', arrEq(ymd(D(2000, 1, 1), D(2026, 1, 1)), [26, 0, 0]));
ok('age: day before birthday', arrEq(ymd(D(2000, 6, 15), D(2026, 6, 14)), [25, 11, 30]));
ok('age: leap day to non-leap', arrEq(ymd(D(2020, 2, 29), D(2021, 2, 28)), [0, 11, 30]), ymd(D(2020, 2, 29), D(2021, 2, 28)));
ok('age: month boundary Jan31->Feb28', arrEq(ymd(D(2024, 1, 31), D(2024, 2, 28)), [0, 0, 28]), ymd(D(2024, 1, 31), D(2024, 2, 28)));

/* ---- date difference (calendar days, UTC components to avoid DST) ---- */
function dayDiff(a, b) {
  return Math.round((Date.UTC(b.getFullYear(), b.getMonth(), b.getDate()) - Date.UTC(a.getFullYear(), a.getMonth(), a.getDate())) / 86400000);
}
ok('datediff: same day', dayDiff(D(2026, 1, 1), D(2026, 1, 1)) === 0);
ok('datediff: one day across DST-ish', dayDiff(D(2026, 3, 7), D(2026, 3, 8)) === 1);
ok('datediff: year', dayDiff(D(2025, 1, 1), D(2026, 1, 1)) === 365);
ok('datediff: reverse', dayDiff(D(2026, 1, 2), D(2026, 1, 1)) === -1);

/* ---- unit conversion factors ---- */
var F = {
  length: { mm: 0.001, cm: 0.01, m: 1, km: 1000, in: 0.0254, ft: 0.3048, yd: 0.9144, mi: 1609.344 },
  mass: { mg: 1e-6, g: 0.001, kg: 1, t: 1000, oz: 0.028349523125, lb: 0.45359237, st: 6.35029318 },
  speed: { mps: 1, kmh: 0.2777778, mph: 0.44704, kn: 0.5144444, fps: 0.3048 },
  area: { m2: 1, km2: 1e6, ft2: 0.09290304, yd2: 0.83612736, ac: 4046.8564224, ha: 10000, mi2: 2589988.110336 },
  volume: { ml: 1e-6, l: 0.001, m3: 1, tsp: 0.00000492892, tbsp: 0.0000147868, cup: 0.000236588, floz: 0.0000295735, gal: 0.00378541 }
};
function conv(cat, v, from, to) { return v * F[cat][from] / F[cat][to]; }
function temp(v, from, to) {
  var c = from === 'C' ? v : from === 'F' ? (v - 32) * 5 / 9 : v - 273.15;
  return to === 'C' ? c : to === 'F' ? c * 9 / 5 + 32 : c + 273.15;
}
ok('unit: 1 km = 1000 m', near(conv('length', 1, 'km', 'm'), 1000));
ok('unit: 1 in = 2.54 cm', near(conv('length', 1, 'in', 'cm'), 2.54, 1e-9));
ok('unit: 1 lb = 0.45359237 kg', near(conv('mass', 1, 'lb', 'kg'), 0.45359237));
ok('unit: 1 gal = 3.78541 l', near(conv('volume', 1, 'gal', 'l'), 3.78541, 1e-9));
ok('unit: 1 ha = 10000 m2', near(conv('area', 1, 'ha', 'm2'), 10000));
ok('unit: 100 km/h ~ 62.137 mph', near(conv('speed', 100, 'kmh', 'mph'), 62.1371192, 1e-4), conv('speed', 100, 'kmh', 'mph'));
ok('temp: 0C = 32F', near(temp(0, 'C', 'F'), 32));
ok('temp: 100C = 212F', near(temp(100, 'C', 'F'), 212));
ok('temp: -40C = -40F', near(temp(-40, 'C', 'F'), -40));
ok('temp: 0C = 273.15K', near(temp(0, 'C', 'K'), 273.15));
ok('temp: 98.6F = 37C', near(temp(98.6, 'F', 'C'), 37, 1e-9));

/* ---- BMI ---- */
function bmi(weightKg, heightM) { return weightKg / (heightM * heightM); }
ok('bmi: 70kg 1.75m = 22.86', near(bmi(70, 1.75), 22.857, 1e-3));
ok('bmi: lb->kg 154lb 69in', near(bmi(154 * 0.45359237, 69 * 0.0254), 22.74, 0.02), bmi(154 * 0.45359237, 69 * 0.0254));

/* ---- discount ---- */
function discount(price, pct, tax) { var d = price * pct / 100; return { saved: d, pre: price - d, final: (price - d) * (1 + (tax || 0) / 100) }; }
var dr = discount(100, 25, 0);
ok('discount: 100 @25% saved 25', near(dr.saved, 25) && near(dr.final, 75));
ok('discount: with 10% tax', near(discount(100, 25, 10).final, 82.5));

/* ---- UUID v4 compliance (fallback path mirror) ---- */
function fakeBytes() { var b = new Uint8Array(16); for (var i = 0; i < 16; i++) b[i] = (i * 17) % 256; return b; }
function uuidFromBytes(bytes) {
  bytes[6] = (bytes[6] & 0x0f) | 0x40;
  bytes[8] = (bytes[8] & 0x3f) | 0x80;
  var hex = Array.from(bytes, function (b) { return ('0' + b.toString(16)).slice(-2); }).join('');
  return hex.slice(0, 8) + '-' + hex.slice(8, 12) + '-' + hex.slice(12, 16) + '-' + hex.slice(16, 20) + '-' + hex.slice(20);
}
var u = uuidFromBytes(fakeBytes());
ok('uuid: shape', /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(u), u);
ok('uuid: version nibble 4', u.charAt(14) === '4');
ok('uuid: variant nibble 8-b', ['8', '9', 'a', 'b'].indexOf(u.charAt(19)) !== -1);

/* ---- secure integer range sanity (with injected deterministic source) ---- */
function unbiased(maxExclusive, rand) {
  if (maxExclusive <= 0) return 0;
  var limit = Math.floor(4294967296 / maxExclusive) * maxExclusive, v;
  do { v = rand(); } while (v >= limit);
  return v % maxExclusive;
}
var seq = [4294967295, 7]; var idx = 0;
ok('random: rejects out-of-range draw', unbiased(10, function () { return seq[idx++]; }) === 7);
ok('random: zero case', unbiased(0, function () { return 0; }) === 0);

console.log('RESULT: ' + pass + ' passed, ' + fail + ' failed');
if (fail) process.exit(1);
