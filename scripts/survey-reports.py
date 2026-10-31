"""Build the public one-page PDF report for each survey year.

Reads src/data/survey.json (portfolio-wide numbers only) and the brand/DRE from
src/site.config.ts, renders an HTML page per year, and prints it to
public/surveys/tenant-survey-<year>.pdf with headless Edge or Chrome.

    python scripts/survey-reports.py
"""
import html
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'public' / 'surveys'
BROWSERS = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    'msedge', 'google-chrome', 'chromium',
]

config = (ROOT / 'src' / 'site.config.ts').read_text(encoding='utf-8')
SITE = {k: re.search(rf"{k}: '([^']*)'", config).group(1) for k in ('brand', 'legalLine', 'dre')}
survey = json.loads((ROOT / 'src' / 'data' / 'survey.json').read_text(encoding='utf-8'))

CSS = """
@page { size: Letter; margin: 0.6in; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', Inter, Arial, sans-serif; color: #0f1b2a; margin: 0; font-size: 11pt; }
.brand { color: #0e6a96; font-weight: 800; letter-spacing: .06em; text-transform: uppercase; font-size: 10pt; }
h1 { font-size: 22pt; margin: 4px 0 2px; }
.sub { color: #6b7a8f; margin: 0 0 18px; }
h2 { font-size: 12pt; margin: 20px 0 8px; padding-bottom: 4px; border-bottom: 1px solid #dfe5ec; }
.tiles { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
.tile { background: #e5f1f7; border-radius: 8px; padding: 12px; }
.tile b { display: block; font-size: 20pt; color: #0a5174; }
.tile b small { font-size: 10pt; color: #44546a; font-weight: 400; }
.tile span { font-size: 9.5pt; color: #44546a; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.bar { display: grid; grid-template-columns: 1fr 120px 30px; align-items: center; gap: 8px; margin: 5px 0; font-size: 9.5pt; }
.track { height: 9px; background: #eef2f6; border-radius: 5px; overflow: hidden; }
.fill { height: 100%; background: #0e6a96; }
.bar em { font-style: normal; font-weight: 600; text-align: right; }
.scale { color: #6b7a8f; font-size: 8.5pt; margin: 0 0 4px; }
blockquote { margin: 6px 0; padding: 6px 12px; border-left: 3px solid #0e6a96; color: #44546a; font-size: 10pt; }
ul.ysd { margin: 0; padding-left: 18px; font-size: 10pt; }
ul.ysd li { margin: 4px 0; }
footer { margin-top: 22px; padding-top: 8px; border-top: 1px solid #dfe5ec; color: #6b7a8f; font-size: 8.5pt; }
"""


def bars(scores, lo=1, hi=5):
    rows = []
    for label, v in scores.items():
        pct = (v - lo) / (hi - lo) * 100
        rows.append(f'<div class="bar"><span>{html.escape(label)}</span>'
                    f'<div class="track"><div class="fill" style="width:{pct:.0f}%"></div></div><em>{v:.1f}</em></div>')
    return ''.join(rows)


def page(y):
    maint = sum(y['maintenance'].values()) / len(y['maintenance'])
    done = [i for i in survey['youSaidWeDid'] if i['confirmed'] and i['year'] == y['year']]
    ysd = ''
    if done:
        items = ''.join(f'<li>You said: {html.escape(i["said"])} <b>We did:</b> {html.escape(i["did"])}</li>' for i in done)
        ysd = f'<h2>You said, we did</h2><ul class="ysd">{items}</ul>'
    quotes = ''.join(f'<blockquote>“{html.escape(q)}”</blockquote>' for q in y.get('quotes', []))
    e = html.escape
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>{y['year']} Tenant Survey Results</title>
<style>{CSS}</style></head><body>
<div class="brand">{e(SITE['brand'])}</div>
<h1>{y['year']} Tenant Survey Results</h1>
<p class="sub">Annual tenant satisfaction survey · {y['responses']} households responded · all homes combined</p>
<div class="tiles">
  <div class="tile"><b>{y['recommend']:.1f}<small> / 10</small></b><span>Would recommend us to a friend</span></div>
  <div class="tile"><b>{maint:.1f}<small> / 5</small></b><span>Maintenance handled well (average)</span></div>
  <div class="tile"><b>{y['value']:.1f}<small> / 10</small></b><span>Home &amp; amenities vs. comparable rentals</span></div>
</div>
<div class="cols">
  <div><h2>When I raise an issue, it's…</h2><p class="scale">1 = strongly disagree · 5 = strongly agree</p>{bars(y['maintenance'])}</div>
  <div><h2>Satisfaction with the home</h2><p class="scale">1 = very dissatisfied · 5 = very satisfied</p>{bars(y['satisfaction'])}</div>
</div>
<p class="scale" style="margin-top:10px">Rent relative to comparable homes averaged {y['rentVsMarket']:.1f} on a 1–5 scale where 3 means “at market.”</p>
{ysd}
<h2>In their words</h2>{quotes}
<footer>{e(SITE['legalLine'])} · CA DRE #{e(SITE['dre'])} · Comments are anonymous and lightly trimmed to remove names and locations. Equal Housing Opportunity.</footer>
</body></html>"""


def main():
    browser = next((b for b in BROWSERS if Path(b).exists() or shutil.which(b)), None)
    if not browser:
        raise SystemExit('Need Edge or Chrome to print PDFs.')
    OUT.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        for y in survey['years']:
            src = Path(tmp) / f"{y['year']}.html"
            src.write_text(page(y), encoding='utf-8')
            pdf = OUT / f"tenant-survey-{y['year']}.pdf"
            subprocess.run([browser, '--headless=new', '--disable-gpu', '--no-pdf-header-footer',
                            f'--print-to-pdf={pdf}', src.as_uri()], check=True, capture_output=True)
            print(pdf.relative_to(ROOT))


if __name__ == '__main__':
    main()
