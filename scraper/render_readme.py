"""Render README.md from data/jobs.json. The README is generated — never hand-edit."""
import os
from datetime import datetime, timedelta, timezone

README_PATH = os.path.join(os.path.dirname(__file__), "..", "README.md")
NEW_BADGE_DAYS = 7

HEADER = """\
# 🎯 Software Engineering Internship Tracker

Auto-updated list of **open software-engineering internships** — AI/ML, Data,
Mobile, Frontend, Backend/Infra, QA and Security roles — at {n_companies} top tech
companies, scraped directly from each company's careers API every 6 hours by
GitHub Actions.

> 🕐 Last updated: **{updated}** · 📌 **{n_open}** open internships
> · 🆕 = added in the last {new_days} days

⭐ Star this repo to keep an eye on new openings — or watch *Releases/Activity* for commits titled “new internship(s)”.

"""

FOOTER = """
---

## How this works

A [Python scraper]({repo}/tree/scraper/scraper) (kept on the `scraper` branch
so this page stays front and center) queries each company's official careers
API (Greenhouse, Ashby, Workday, Eightfold or their in-house endpoints),
filters titles matching *intern / internship / co-op*, keeps only
software-engineering roles ([categories.py]({repo}/blob/scraper/scraper/categories.py)),
and diffs against [`data/jobs.json`]({repo}/blob/scraper/data/jobs.json).
A GitHub Actions [workflow]({repo}/blob/main/.github/workflows/update.yml)
runs it on a cron schedule and commits only when something changed. Positions
that disappear from a careers page are closed automatically.

Found a problem or want another company added? Open an issue or PR.
""".replace("{repo}", "https://github.com/Emjumaev/FAANG-2027-Internships-Tracker")


def _slug(name):
    return "".join(c if c.isalnum() else "-" for c in name.lower()).strip("-")


def _md_escape(text):
    return text.replace("|", "\\|").strip()


def _fmt_locations(locations, limit=3):
    locs = [l for l in locations if l]
    if not locs:
        return "—"
    shown = "; ".join(_md_escape(l) for l in locs[:limit])
    extra = len(locs) - limit
    if extra > 0:
        shown += " *(+{} more)*".format(extra)
    return shown


def render(state):
    from .companies import COMPANIES, UNSUPPORTED
    tracked = [c["name"] for c in COMPANIES]
    jobs = [j for j in state["jobs"].values() if j.get("active", True)]
    updated = state.get("updated_at") or datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    cutoff = (datetime.now(timezone.utc) - timedelta(days=NEW_BADGE_DAYS)).strftime("%Y-%m-%d")

    by_company = {name: [] for name in tracked}
    for j in jobs:
        by_company.setdefault(j["company"], []).append(j)

    companies = sorted(by_company)
    out = [HEADER.format(
        n_companies=len(companies),
        updated=updated.replace("T", " ").replace("Z", " UTC"),
        n_open=len(jobs),
        new_days=NEW_BADGE_DAYS,
    )]

    # summary table with anchors
    out.append("| Company | Open internships |\n|---|---|\n")
    for c in companies:
        n = len(by_company[c])
        label = "[{}](#{})".format(c, _slug(c)) if n else c
        out.append("| {} | {} |\n".format(label, n or "—"))
    for name, why in sorted(UNSUPPORTED.items()):
        out.append("| {} | *{}* |\n".format(name, why))
    out.append("\n---\n\n")

    for c in companies:
        if not by_company[c]:
            continue
        rows = sorted(by_company[c],
                      key=lambda j: (j.get("posted") or j.get("first_seen", ""),
                                     j["title"]),
                      reverse=True)
        out.append("## {}\n\n".format(c))
        out.append("| Role | Category | Location | Posted | First seen |\n"
                   "|---|---|---|---|---|\n")
        for j in rows:
            badge = " 🆕" if j.get("first_seen", "") >= cutoff else ""
            out.append("| [{}]({}){} | {} | {} | {} | {} |\n".format(
                _md_escape(j["title"]), j["url"], badge,
                j.get("category") or "—",
                _fmt_locations(j.get("locations", [])),
                j.get("posted") or "—",
                j.get("first_seen", "—"),
            ))
        out.append("\n")

    out.append(FOOTER)
    with open(README_PATH, "w") as fh:
        fh.write("".join(out))
