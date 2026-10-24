// Diaper Math engine: weight gain against the next size line - the days and weeks to the line, the diapers that takes, the packs to buy with cost, and the size-up date. Exact integers, half-up on display only, civil-date arithmetic with no library. No named constants; every number is the owner's own entry.
function _i(t, err, digits, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!new RegExp("^[0-9]{1," + digits + "}$").test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _pl(n, one, many) { return n + (n === 1 ? one : many); }
function _v(n, one, many) { return n === 1 ? one : many; }
function _m(c) { return "$" + Math.floor(c / 100) + "." + String(c % 100).padStart(2, "0"); }
var _C = "the current weight must be from 1000 to 20000 grams with no decimal places";
var _G = "the weekly gain must be from 1 to 1000 grams with no decimal places";
var _N = "the size line must be from 1001 to 30000 grams with no decimal places";
var _X = "the size line must be above the current weight";
var _P = "the diapers a day must be from 1 to 30 with no decimal places";
var _K = "the pack size must be from 1 to 200 with no decimal places";
var _R = "the pack price must be from 1 to 99999 cents with no decimal places";
var _D = "the start date must be a real date as YYYY-MM-DD between 2000 and 2100";
function _days_to(cur, gain, line) {
  var c = _i(cur, _C, 5, 1000, 20000), g = _i(gain, _G, 4, 1, 1000), n = _i(line, _N, 5, 1001, 30000);
  if (n <= c) throw new Error(_X);
  var gap = n - c;
  return Math.floor((gap * 7 + g - 1) / g);
}
function _days(y, m, d) {
  y -= m <= 2 ? 1 : 0;
  var era = Math.floor((y >= 0 ? y : y - 399) / 400);
  var yoe = y - era * 400;
  var doy = Math.floor((153 * (m > 2 ? m - 3 : m + 9) + 2) / 5) + d - 1;
  var doe = yoe * 365 + Math.floor(yoe / 4) - Math.floor(yoe / 100) + doy;
  return era * 146097 + doe - 719468;
}
function _civil(z) {
  z += 719468;
  var era = Math.floor((z >= 0 ? z : z - 146096) / 146097);
  var doe = z - era * 146097;
  var yoe = Math.floor((doe - Math.floor(doe / 1460) + Math.floor(doe / 36524) - Math.floor(doe / 146096)) / 365);
  var y = yoe + era * 400;
  var doy = doe - (365 * yoe + Math.floor(yoe / 4) - Math.floor(yoe / 100));
  var mp = Math.floor((5 * doy + 2) / 153);
  var d = doy - Math.floor((153 * mp + 2) / 5) + 1;
  var m = mp + (mp < 10 ? 3 : -9);
  return [y + (m <= 2 ? 1 : 0), m, d];
}
function _date(t) {
  t = typeof t === "string" ? t.trim() : "";
  var m = /^([0-9]{4})-([0-9]{2})-([0-9]{2})$/.exec(t);
  if (!m) throw new Error(_D);
  var y = +m[1], mo = +m[2], d = +m[3];
  if (y < 2000 || y > 2100) throw new Error(_D);
  var c = _civil(_days(y, mo, d));
  if (c[0] !== y || c[1] !== mo || c[2] !== d) throw new Error(_D);
  return _days(y, mo, d);
}
function _fmt(z) {
  var c = _civil(z);
  var wd = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][(z + 4) % 7];
  function p(x) { return String(x).padStart(2, "0"); }
  return c[0] + "-" + p(c[1]) + "-" + p(c[2]) + ", a " + wd;
}
function sizeTruth(cur, gain, line) {
  var d = _days_to(cur, gain, line), w = Math.floor(d / 7), r = d % 7;
  return "The " + cur.trim() + "-gram baby at " + _pl(parseInt(gain, 10), " gram", " grams") + " a week reaches the " + line.trim() + "-gram size line in " + _pl(w, " week", " weeks") + " and " + _pl(r, " day", " days") + ".";
}
function diapersTruth(cur, gain, line, per) {
  var d = _days_to(cur, gain, line), p = _i(per, _P, 2, 1, 30), n = d * p;
  return "At " + _pl(p, " diaper", " diapers") + " a day, the " + _pl(d, " day", " days") + " " + _v(d, "takes", "take") + " " + _pl(n, " diaper", " diapers") + ".";
}
function packsTruth(cur, gain, line, per, pack, price) {
  var d = _days_to(cur, gain, line), p = _i(per, _P, 2, 1, 30), n = d * p;
  var k = _i(pack, _K, 3, 1, 200), r = _i(price, _R, 5, 1, 99999);
  var packs = Math.ceil(n / k), last = n - (packs - 1) * k, cost = packs * r;
  var pd = Math.floor((2 * cost + n) / (2 * n));
  return "The " + _pl(n, " diaper", " diapers") + " " + _v(n, "makes", "make") + " " + _pl(packs, " pack", " packs") + " of " + k + ", the last pack holding " + _pl(last, " diaper", " diapers") + ", costing " + _m(cost) + ", " + _m(pd) + " a diaper.";
}
function dateTruth(start, cur, gain, line) {
  var z = _date(start), d = _days_to(cur, gain, line);
  return "Starting " + start.trim() + ", the size line lands on " + _fmt(z + d) + ".";
}
