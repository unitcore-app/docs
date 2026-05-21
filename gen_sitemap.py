#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).parent
DATA = json.loads((ROOT / "errors.json").read_text())

BASE = "https://docs.unitcore.app"

urls = [BASE + "/"]
for g in DATA["groups"]:
    for c in g["codes"]:
        urls.append(BASE + "/errors/" + c["code"].replace(".", "/"))

body = ['<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    body.append(f"  <url><loc>{u}</loc></url>")
body.append("</urlset>")

(ROOT / "sitemap.xml").write_text("\n".join(body) + "\n")
print(f"Wrote sitemap with {len(urls)} URLs.")
