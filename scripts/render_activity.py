#!/usr/bin/env python3
"""Render assets/activity.svg (heatmap + streaks + languages) from data/stats.json."""
import datetime
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from theme import *  # noqa: E402,F403

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "data", "stats.json")
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, "..", "assets", "activity.svg")

W, H = 900, 322
LEVELS = ["#1c150b", "#5a3c09", "#9a6505", "#db9200", AMBER]
LANG_COLOURS = [AMBER, RED, AMBER_HI, "#d9730d", AMBER_DIM, "#6b4a12"]
CELL, GAP = 12, 3
GX, GY = 52, 100  # heatmap origin


def heatmap(days):
    first = datetime.date.fromisoformat(days[0]["date"])
    sunday = first - datetime.timedelta(days=(first.weekday() + 1) % 7)
    cols = {}
    for d in days:
        dt = datetime.date.fromisoformat(d["date"])
        c = (dt - sunday).days // 7
        r = (dt.weekday() + 1) % 7
        cols.setdefault(c, []).append((r, d))
    out, months, seen = [], [], set()
    for c in sorted(cols):
        x = GX + c * (CELL + GAP)
        cells = []
        for r, d in cols[c]:
            lvl = max(0, min(4, d["level"]))
            cells.append(f'<rect x="{x}" y="{GY + r*(CELL+GAP)}" width="{CELL}" height="{CELL}" rx="2" fill="{LEVELS[lvl]}"/>')
            dt = datetime.date.fromisoformat(d["date"])
            key = dt.strftime("%Y-%m")
            if dt.day <= 7 and key not in seen and c > 0:
                seen.add(key)
                months.append(f'<text x="{x}" y="{GY-9}">{dt.strftime("%b")}</text>')
        out.append(f'<g class="col" style="animation-delay:{0.4 + c*0.018:.3f}s">{"".join(cells)}</g>')
    days_lbl = "".join(
        f'<text x="{GX-10}" y="{GY + r*(CELL+GAP) + 10}" text-anchor="end">{n}</text>'
        for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))
    return "".join(out), "".join(months) + days_lbl, max(cols) + 1


def stats_row(s, y):
    best = datetime.date.fromisoformat(s["best_day"]["date"]).strftime("%d %b")
    items = [
        ("contributions / 1y", f'{s["total"]:,}'),
        ("current streak", f'{s["current_streak"]}d'),
        ("longest streak", f'{s["longest_streak"]}d'),
        ("busiest day", f'{s["best_day"]["count"]} ({best})'),
    ]
    span = (W - 60) / len(items)
    out = []
    for i, (label, val) in enumerate(items):
        x = 30 + i * span
        out.append(f'<g class="pop" style="animation-delay:{1.2 + i*0.12:.2f}s">'
                   f'<text x="{x}" y="{y}" font-size="11" fill="{AMBER_DIM}">{esc(label.upper())}</text>'
                   f'<text x="{x}" y="{y+26}" font-size="22" font-weight="700" fill="{AMBER}">{esc(val)}</text></g>')
    return "".join(out)


def languages(langs, y):
    if not langs:
        return ""
    top = langs[:5]
    other = round(100 - sum(l["pct"] for l in top), 1)
    if other >= 0.5:
        top = top + [{"name": "Other", "pct": other}]
    x0, width = 30, W - 60
    bar, keys, x, kx = [], [], x0, x0
    for i, l in enumerate(top):
        w = width * l["pct"] / 100
        col = LANG_COLOURS[i % len(LANG_COLOURS)]
        bar.append(f'<rect x="{x:.1f}" y="{y}" width="{max(w-2, 1):.1f}" height="8" fill="{col}"/>')
        x += w
        label = f'{l["name"]} {l["pct"]}%'
        keys.append(f'<rect x="{kx}" y="{y+20}" width="8" height="8" fill="{col}"/>'
                    f'<text x="{kx+13}" y="{y+28}" font-size="11.5" fill="{AMBER_HI}">{esc(label)}</text>')
        kx += 13 + text_w(label, 11.5) + 22
    return (f'<clipPath id="barclip"><rect x="{x0}" y="{y}" width="{width}" height="8" rx="4"/></clipPath>'
            f'<g clip-path="url(#barclip)"><g class="grow">{"".join(bar)}</g></g>'
            f'<g class="pop" style="animation-delay:1.9s">{"".join(keys)}</g>')


def main():
    with open(SRC) as f:
        s = json.load(f)
    cells, labels, ncols = heatmap(s["days"])
    cmd = 'git log --author=ethan --since="1 year ago" | ./heatmap'
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{s['total']} GitHub contributions in the last year. Current streak {s['current_streak']} days, longest {s['longest_streak']} days.">
<title>JustLikeChuu: GitHub activity (last 12 months)</title>
<style>
  .col{{animation:fade .25s ease-out both}}
  .pop{{animation:fade .5s ease-out both}}
  .grow{{transform-origin:30px 0;animation:grow 1s cubic-bezier(.2,.8,.2,1) 1.6s both}}
  .blink{{animation:blink 1.05s steps(1) infinite}}
  @keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
  @keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
  @keyframes blink{{0%{{opacity:1}}50%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{*{{animation-duration:0s!important;animation-delay:0s!important}}}}
</style>
<defs>{defs_common()}</defs>
{window_open(W, H, "ethan@justlikechuu: ~/activity")}
  <text x="{W-20}" y="20.5" text-anchor="end" font-family="{FONT}" font-size="11" fill="{AMBER_FAINT}">synced {esc(s['generated_at'])}</text>
  <g font-family="{FONT}" xml:space="preserve">
    <text x="30" y="62" font-size="13.5"><tspan fill="{AMBER}" font-weight="700">$ </tspan><tspan fill="{CREAM}">{esc(cmd)}</tspan></text>
    <g font-size="10.5" fill="{AMBER_DIM}">{labels}</g>
    {cells}
    <line x1="30" y1="{GY + 7*(CELL+GAP) + 10}" x2="{W-30}" y2="{GY + 7*(CELL+GAP) + 10}" stroke="{AMBER_FAINT}" stroke-dasharray="2 4"/>
    {stats_row(s, GY + 7*(CELL+GAP) + 34)}
    {languages(s.get("languages", []), GY + 7*(CELL+GAP) + 82)}
  </g>
{window_close(W, H)}
</svg>
"""
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT} ({len(svg)/1024:.1f} KB, {ncols} weeks)")


if __name__ == "__main__":
    main()
