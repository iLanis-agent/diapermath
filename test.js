const fs = require("fs");
eval(fs.readFileSync("engine.js", "utf8"));
const exp = JSON.parse(fs.readFileSync("expected.json", "utf8"));
const fns = { size: sizeTruth, diapers: diapersTruth, packs: packsTruth, date: dateTruth };
let fail = 0;
for (const c of exp.cases) {
  const got = JSON.stringify(fns[c.fn](...c.args));
  if (got !== JSON.stringify(c.expect)) { fail++; console.log("MISMATCH", c.fn, c.args, "\n got:", got, "\n exp:", JSON.stringify(c.expect)); }
}
const ERRS = ["the current weight must be from 1000 to 20000 grams with no decimal places",
  "the weekly gain must be from 1 to 1000 grams with no decimal places",
  "the size line must be from 1001 to 30000 grams with no decimal places",
  "the size line must be above the current weight",
  "the diapers a day must be from 1 to 30 with no decimal places",
  "the pack size must be from 1 to 200 with no decimal places",
  "the pack price must be from 1 to 99999 cents with no decimal places",
  "the start date must be a real date as YYYY-MM-DD between 2000 and 2100"];
for (const [fn, args] of exp.errors) {
  let threw = null;
  try { fns[fn](...args); } catch (e) { threw = e.message; }
  if (!threw || !ERRS.includes(threw)) { fail++; console.log("ERRCASE FAIL", fn, args, "->", threw); }
}
console.log(fail ? `${fail} FAILURES` : "all green");
process.exit(fail ? 1 : 0);
