#!/usr/bin/env python3
# Diaper Math oracle - independent mirror of engine.js; writes expected.json.
import json, math

def days_to(cur, gain, line):
    c, g, n = int(cur), int(gain), int(line)
    assert 1000 <= c <= 20000 and 1 <= g <= 1000 and 1001 <= n <= 30000 and n > c
    gap = n - c
    return (gap * 7 + g - 1) // g

def civil(z):
    z += 719468
    era = (z if z >= 0 else z - 146096) // 146097
    doe = z - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    y = yoe + era * 400
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    d = doy - (153 * mp + 2) // 5 + 1
    m = mp + (3 if mp < 10 else -9)
    return [y + (1 if m <= 2 else 0), m, d]

def gday(y, m, d):
    y -= 1 if m <= 2 else 0
    era = (y if y >= 0 else y - 399) // 400
    yoe = y - era * 400
    doy = (153 * (m - 3 if m > 2 else m + 9) + 2) // 5 + d - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468

def fmt(z):
    c = civil(z)
    wd = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"][(z + 4) % 7]
    return f"{c[0]}-{str(c[1]).zfill(2)}-{str(c[2]).zfill(2)}, a {wd}"

def pl(n, one, many): return f"{n}{one if n == 1 else many}"
def v(n, one, many): return one if n == 1 else many
def m(c): return f"${c//100}.{str(c%100).zfill(2)}"

def size(cur, gain, line):
    d = days_to(cur, gain, line)
    w, r = divmod(d, 7)
    return f"The {cur.strip()}-gram baby at {pl(int(gain),' gram',' grams')} a week reaches the {line.strip()}-gram size line in {pl(w,' week',' weeks')} and {pl(r,' day',' days')}."

def diapers(cur, gain, line, per):
    d = days_to(cur, gain, line)
    p = int(per); n = d * p
    return f"At {pl(p,' diaper',' diapers')} a day, the {pl(d,' day',' days')} {v(d,'takes','take')} {pl(n,' diaper',' diapers')}."

def packs(cur, gain, line, per, pack, price):
    d = days_to(cur, gain, line)
    p = int(per); n = d * p
    k, r = int(pack), int(price)
    pk = math.ceil(n / k); last = n - (pk - 1) * k; cost = pk * r
    pd = (2 * cost + n) // (2 * n)
    return f"The {pl(n,' diaper',' diapers')} {v(n,'makes','make')} {pl(pk,' pack',' packs')} of {k}, the last pack holding {pl(last,' diaper',' diapers')}, costing {m(cost)}, {m(pd)} a diaper."

def date(start, cur, gain, line):
    y, mo, dd = map(int, start.strip().split("-"))
    z = gday(y, mo, dd)
    d = days_to(cur, gain, line)
    return f"Starting {start.strip()}, the size line lands on {fmt(z + d)}."

cases = []
# defaults
D = ("6200", "150", "8000"); PER = "8"; PACK = "44"; PRICE = "1150"; START = "2026-10-24"
cases.append({"fn":"size","args":list(D)})
cases.append({"fn":"diapers","args":list(D)+[PER]})
cases.append({"fn":"packs","args":list(D)+[PER,PACK,PRICE]})
cases.append({"fn":"date","args":[START]+list(D)})
# singular grammar probes
cases.append({"fn":"size","args":["6993","7","7000"]})            # 1 day -> 0 weeks 1 day
cases.append({"fn":"size","args":["6990","70","7000"]})           # 7d -> 1 week 0 days
cases.append({"fn":"size","args":["6990","10","7000"]})           # 70d -> 10 weeks
cases.append({"fn":"size","args":["1000","1","1001"]})            # gap 1g, gain 1 -> 7 days
cases.append({"fn":"size","args":["19999","1000","20001"]})       # tiny gap big gain -> 1 day
cases.append({"fn":"size","args":["3400","180","5200"]})
cases.append({"fn":"size","args":["4500","200","9000"]})
cases.append({"fn":"size","args":["8000","250","13000"]})
cases.append({"fn":"size","args":["11000","300","17000"]})
cases.append({"fn":"size","args":["2900","90","3400"]})
cases.append({"fn":"size","args":["5000","167","6400"]})
cases.append({"fn":"size","args":["7200","165","10000"]})
cases.append({"fn":"size","args":["9200","210","12500"]})
cases.append({"fn":"size","args":["3000","100","5000"]})
cases.append({"fn":"size","args":["6000","175","9500"]})
cases.append({"fn":"size","args":["1500","50","3000"]})
cases.append({"fn":"size","args":["12500","400","18000"]})
cases.append({"fn":"size","args":["4100","130","6000"]})
cases.append({"fn":"size","args":["5500","190","8200"]})
cases.append({"fn":"size","args":["6800","220","11000"]})
cases.append({"fn":"size","args":["2000","60","3500"]})
cases.append({"fn":"size","args":["10500","350","15000"]})
cases.append({"fn":"size","args":["8800","275","14000"]})
cases.append({"fn":"diapers","args":["6993","7","7000","1"]})     # 1 day, 1 diaper/day -> 1 diaper
cases.append({"fn":"diapers","args":["6993","7","7000","5"]})     # 1 day takes 5
cases.append({"fn":"diapers","args":["6990","70","7000","9"]})    # 7 days
cases.append({"fn":"diapers","args":["3400","180","5200","6"]})
cases.append({"fn":"diapers","args":["4500","200","9000","10"]})
cases.append({"fn":"diapers","args":["8000","250","13000","7"]})
cases.append({"fn":"diapers","args":["11000","300","17000","12"]})
cases.append({"fn":"diapers","args":["2900","90","3400","4"]})
cases.append({"fn":"diapers","args":["5000","167","6400","8"]})
cases.append({"fn":"diapers","args":["7200","165","10000","30"]})
cases.append({"fn":"diapers","args":["9200","210","12500","11"]})
cases.append({"fn":"diapers","args":["3000","100","5000","2"]})
cases.append({"fn":"diapers","args":["6000","175","9500","9"]})
cases.append({"fn":"diapers","args":["1500","50","3000","3"]})
cases.append({"fn":"diapers","args":["12500","400","18000","6"]})
cases.append({"fn":"diapers","args":["4100","130","6000","5"]})
cases.append({"fn":"diapers","args":["5500","190","8200","8"]})
cases.append({"fn":"diapers","args":["6800","220","11000","7"]})
cases.append({"fn":"diapers","args":["2000","60","3500","10"]})
cases.append({"fn":"diapers","args":["10500","350","15000","4"]})
cases.append({"fn":"diapers","args":["8800","275","14000","6"]})
cases.append({"fn":"diapers","args":["3000","80","4500","1"]})
cases.append({"fn":"diapers","args":["9500","260","15000","13"]})
cases.append({"fn":"diapers","args":["7000","140","9100","8"]})
cases.append({"fn":"packs","args":["6993","7","7000","1","44","1150"]})   # 1 diaper -> 1 pack holding 1
cases.append({"fn":"packs","args":["6990","70","7000","8","44","1150"]})  # 56 -> 2 packs last 12
cases.append({"fn":"packs","args":["3400","180","5200","6","30","899"]})
cases.append({"fn":"packs","args":["4500","200","9000","10","36","1049"]})
cases.append({"fn":"packs","args":["8000","250","13000","7","50","1399"]})
cases.append({"fn":"packs","args":["11000","300","17000","12","80","2199"]})
cases.append({"fn":"packs","args":["2900","90","3400","4","24","649"]})
cases.append({"fn":"packs","args":["5000","167","6400","8","44","999"]})
cases.append({"fn":"packs","args":["7200","165","10000","30","96","1799"]})
cases.append({"fn":"packs","args":["9200","210","12500","11","40","1249"]})
cases.append({"fn":"packs","args":["3000","100","5000","2","20","499"]})
cases.append({"fn":"packs","args":["6000","175","9500","9","48","1149"]})
cases.append({"fn":"packs","args":["1500","50","3000","3","28","779"]})
cases.append({"fn":"packs","args":["12500","400","18000","6","60","1549"]})
cases.append({"fn":"packs","args":["4100","130","6000","5","32","925"]})
cases.append({"fn":"packs","args":["5500","190","8200","8","44","1075"]})
cases.append({"fn":"packs","args":["6800","220","11000","7","52","1325"]})
cases.append({"fn":"packs","args":["2000","60","3500","10","40","1125"]})
cases.append({"fn":"packs","args":["10500","350","15000","4","36","989"]})
cases.append({"fn":"packs","args":["8800","275","14000","6","46","1199"]})
cases.append({"fn":"packs","args":["3000","80","4500","1","1","99999"]})   # pack size 1, max price
cases.append({"fn":"packs","args":["9500","260","15000","13","64","1450"]})
cases.append({"fn":"packs","args":["7000","140","9100","8","44","1"]})     # min price 1 cent
cases.append({"fn":"packs","args":["6990","10","7000","9","200","1500"]})  # max pack 200
cases.append({"fn":"packs","args":["6200","150","8000","8","44","1150"]})  # default again
cases.append({"fn":"date","args":["2026-10-24","6993","7","7000"]})        # +1 day
cases.append({"fn":"date","args":["2026-10-24","6990","70","7000"]})       # +7 days
cases.append({"fn":"date","args":["2026-02-28","3400","180","5200"]})      # non-leap Feb
cases.append({"fn":"date","args":["2028-02-28","4500","200","9000"]})      # leap year Feb 29 real
cases.append({"fn":"date","args":["2026-12-31","8000","250","13000"]})     # year rollover
cases.append({"fn":"date","args":["2027-01-01","11000","300","17000"]})
cases.append({"fn":"date","args":["2030-06-15","2900","90","3400"]})
cases.append({"fn":"date","args":["2044-01-15","5000","167","6400"]})
cases.append({"fn":"date","args":["2026-10-24","7200","165","10000"]})
cases.append({"fn":"date","args":["2099-12-01","9200","210","12500"]})     # far date, may pass 2100 in result
cases.append({"fn":"date","args":["2026-10-24","3000","100","5000"]})
cases.append({"fn":"date","args":["2031-03-20","6000","175","9500"]})
cases.append({"fn":"date","args":["2026-10-24","1500","50","3000"]})
cases.append({"fn":"date","args":["2040-07-04","12500","400","18000"]})
cases.append({"fn":"date","args":["2026-10-24","4100","130","6000"]})
cases.append({"fn":"date","args":["2035-11-11","5500","190","8200"]})
cases.append({"fn":"date","args":["2026-10-24","6800","220","11000"]})
cases.append({"fn":"date","args":["2029-09-09","2000","60","3500"]})
cases.append({"fn":"date","args":["2026-10-24","10500","350","15000"]})
cases.append({"fn":"date","args":["2050-05-25","8800","275","14000"]})
cases.append({"fn":"date","args":["2026-10-24","3000","80","4500"]})
cases.append({"fn":"date","args":["2033-08-08","9500","260","15000"]})
cases.append({"fn":"date","args":["2026-10-24","7000","140","9100"]})
cases.append({"fn":"date","args":["2100-12-31","6993","7","7000"]})        # max start date
cases.append({"fn":"date","args":["2000-01-01","6990","10","7000"]})       # min start date

for c in cases:
    f = {"size":size,"diapers":diapers,"packs":packs,"date":date}[c["fn"]]
    c["expect"] = f(*c["args"])

errors = [
  ["size",["999","150","8000"]],            # cur too low
  ["size",["20001","150","8000"]],          # cur too high
  ["size",["6200","0","8000"]],             # gain 0
  ["size",["6200","1001","8000"]],          # gain too high
  ["size",["6200","150","1000"]],           # line too low
  ["size",["6200","150","30001"]],          # line too high
  ["size",["8000","150","8000"]],           # line == cur
  ["size",["9000","150","8000"]],           # line < cur
  ["diapers",["6200","150","8000","0"]],    # per 0
  ["diapers",["6200","150","8000","31"]],   # per too high
  ["packs",["6200","150","8000","8","0","1150"]],   # pack 0
  ["packs",["6200","150","8000","8","201","1150"]], # pack too high
  ["packs",["6200","150","8000","8","44","0"]],     # price 0
  ["packs",["6200","150","8000","8","44","100000"]],# price too high
  ["date",["2026-02-30","6200","150","8000"]],      # impossible date
  ["date",["2026-13-01","6200","150","8000"]],      # month 13
  ["date",["1999-12-31","6200","150","8000"]],      # year too low
  ["date",["2101-01-01","6200","150","8000"]],      # year too high
  ["size",["62x0","150","8000"]],           # non-digit
  ["diapers",["6200","150","8000",""]],     # empty
]
out = {"cases": cases, "errors": errors}
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print("cases:", len(cases), "errors:", len(errors))
