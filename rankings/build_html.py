"""Build a single self-contained HTML file with the ranking data inlined.

Reads rankings.json and template.html, replaces a placeholder, and
writes ebk_rankings.html which opens correctly from the filesystem.
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
TEMPLATE = HERE / "template.html"
DATA = HERE / "rankings.json"
OUT = HERE / "ebk_rankings.html"

PLACEHOLDER = "/*__DATA__*/null"

html = TEMPLATE.read_text()
data = DATA.read_text()
if PLACEHOLDER not in html:
    raise SystemExit(f"Placeholder {PLACEHOLDER!r} not in template")
html = html.replace(PLACEHOLDER, data)
OUT.write_text(html)
print(f"Wrote {OUT}  ({OUT.stat().st_size / 1024:.1f} KB)")
