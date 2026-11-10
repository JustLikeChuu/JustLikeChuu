#!/usr/bin/env python3
"""
Pull live profile data into data/stats.json:
  - daily contributions for the last year, scraped from the same public
    fragment GitHub's own profile page uses (counts private work if the
    profile shows it, no token needed)
  - language bytes across your own public, non-fork repos (REST API)

Run daily by .github/workflows/refresh.yml.
"""
import datetime
import json
import os
import re
import sys

import requests
from bs4 import BeautifulSoup

USER = os.environ.get("GH_USER", "JustLikeChuu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "stats.json")

# Generated or doc-only languages that would otherwise drown out real code
# (e.g. tofuFTP's HTML report). Edit to taste.
SKIP_LANGS = {"HTML", "CSS", "Makefile", "Roff", "Batchfile", "PowerShell", "Dockerfile", "Jupyter Notebook"}
SKIP_REPOS = {USER}  # the profile repo itself

UA = {"User-Agent": "justlikechuu-profile-bot/1.0"}


def fetch_days():
    r = requests.get(f"https://github.com/users/{USER}/contributions", headers=UA, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    tips = {t.get("for"): t.get_text(strip=True) for t in soup.find_all("tool-tip")}
    days = []
    for td in soup.select("td.ContributionCalendar-day"):
        date = td.get("data-date")
        if not date:
            continue
        text = tips.get(td.get("id"), "")
        m = re.match(r"(\d[\d,]*)", text)
        count = int(m.group(1).replace(",", "")) if m and not re.search(r"no contributions", text, re.I) else 0
        days.append({"date": date, "count": count, "level": int(td.get("data-level") or 0)})
    if not days:
        sys.exit("no calendar cells found: GitHub markup may have changed")
    days.sort(key=lambda d: d["date"])
    return days


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] else 0
        longest = max(longest, run)
    i = len(days) - 1
    if days[i]["count"] == 0:
        i -= 1  # today isn't over yet; don't break the streak on it
    current = 0
    while i >= 0 and days[i]["count"]:
        current += 1
        i -= 1
    return current, longest


def fetch_languages():
    h = dict(UA, Accept="application/vnd.github+json")
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    repos = requests.get(f"https://api.github.com/users/{USER}/repos",
                         params={"per_page": 100, "type": "owner"}, headers=h, timeout=30)
    repos.raise_for_status()
    totals = {}
    for repo in repos.json():
        if repo["fork"] or repo["archived"] or repo["name"] in SKIP_REPOS:
            continue
        r = requests.get(repo["languages_url"], headers=h, timeout=30)
        if r.ok:
            for lang, n in r.json().items():
                if lang not in SKIP_LANGS:
                    totals[lang] = totals.get(lang, 0) + n
    total = sum(totals.values()) or 1
    ranked = sorted(totals.items(), key=lambda kv: -kv[1])
    return [{"name": k, "pct": round(v * 100 / total, 1)} for k, v in ranked]


def main():
    days = fetch_days()
    current, longest = streaks(days)
    best = max(days, key=lambda d: d["count"])
    try:
        langs = fetch_languages()
    except requests.RequestException as e:
        print(f"languages skipped: {e}", file=sys.stderr)
        langs = []
    data = {
        "user": USER,
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "total": sum(d["count"] for d in days),
        "active_days": sum(1 for d in days if d["count"]),
        "current_streak": current,
        "longest_streak": longest,
        "best_day": {"date": best["date"], "count": best["count"]},
        "languages": langs,
        "days": days,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(data, f, indent=1)
    print(f"{data['total']} contributions, streak {current}/{longest}, {len(langs)} languages")


if __name__ == "__main__":
    main()
