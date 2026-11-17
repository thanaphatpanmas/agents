#!/usr/bin/env python3
"""Pair before/after screenshots side by side for Story.

usage: compare.py <screenshots-dir> [--captions captions.json] [--before-label TEXT] [--after-label TEXT]

Reads <dir>/before/<name>.png and <dir>/after/<name>.png, preferring the ringed
<side>/marked/<name>.png. Writes <dir>/compare/_<name>.html for each name found on both sides and
<dir>/compare/render.js, then prints the playwright-cli command that renders <dir>/compare/<name>.png.
captions.json maps a name to the text of its red caption bar, e.g. "6 of 7 → 5.6 of 7".
"""
import argparse
import html
import json
import sys
from pathlib import Path


def shot(root: Path, side: str, name: str) -> Path:
    marked = root / side / "marked" / f"{name}.png"
    return marked if marked.exists() else root / side / f"{name}.png"


def main() -> int:
    parser = argparse.ArgumentParser(description="Pair before/after screenshots side by side.")
    parser.add_argument("dir", type=Path, help="screenshots folder holding before/ and after/")
    parser.add_argument("--captions", type=Path, help="JSON object: screenshot name -> caption")
    parser.add_argument("--before-label", default="Before")
    parser.add_argument("--after-label", default="After")
    args = parser.parse_args()

    root = args.dir.resolve()
    captions = json.loads(args.captions.read_text(encoding="utf-8")) if args.captions else {}
    before = {p.stem for p in (root / "before").glob("*.png")}
    after = {p.stem for p in (root / "after").glob("*.png")}
    names = sorted(before & after)
    for name in sorted(before ^ after):
        print(f"skipped {name}: only on one side", file=sys.stderr)
    if not names:
        print(f"no pairs: {root}/before and {root}/after share no .png names", file=sys.stderr)
        return 1

    out = root / "compare"
    out.mkdir(exist_ok=True)
    pages = []
    for name in names:
        page = out / f"_{name}.html"
        page.write_text(f"""<!doctype html><meta charset="utf-8"><style>
body{{margin:0;width:2000px;font:16px sans-serif;background:#fff}}
.bar{{background:#d32f2f;color:#fff;font:700 22px sans-serif;padding:14px 20px}}
.row{{display:flex;gap:16px;padding:12px}} .col{{flex:1}}
.label{{font:700 20px sans-serif;padding:6px 0}} .before .label{{color:#555}} .after .label{{color:#2e7d32}}
img{{width:100%;border:1px solid #ccc}}</style>
<div class="bar">{html.escape(captions.get(name, name))}</div><div class="row">
<div class="col before"><div class="label">{html.escape(args.before_label)}</div><img src="{shot(root, 'before', name).as_uri()}"></div>
<div class="col after"><div class="label">{html.escape(args.after_label)}</div><img src="{shot(root, 'after', name).as_uri()}"></div>
</div>""", encoding="utf-8")
        pages.append([page.as_uri(), str(out / f"{name}.png")])

    render = out / "render.js"
    render.write_text(f"""async page => {{
  const pages = {json.dumps(pages, ensure_ascii=False)};
  for (const [url, path] of pages) {{
    await page.setViewportSize({{ width: 2000, height: 900 }});
    await page.goto(url);
    await page.waitForLoadState('load');
    await page.screenshot({{ path, fullPage: true }});
  }}
  return `${{pages.length}} pairs`;
}}
""", encoding="utf-8")
    print(f"{len(names)} pairs; render with: playwright-cli -s=<session> run-code --filename={render}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
