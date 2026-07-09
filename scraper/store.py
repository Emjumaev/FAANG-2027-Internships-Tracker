"""Load/save data/jobs.json and diff new scrape results against it.

jobs.json layout:
{
  "updated_at": "2026-07-09T12:00:00Z",
  "jobs": {
    "<uid>": {
      "company": ..., "external_id": ..., "title": ..., "url": ..., "locations": [...],
      "first_seen": "2026-07-09", "last_seen": "2026-07-09", "active": true
    }
  }
}

Jobs are never deleted; when a posting disappears from a successful scrape it is
flagged active=false (so first_seen survives a posting flapping on/off).
If a company's scraper FAILED this run, its existing jobs are left untouched.
"""
import json
import os
from datetime import datetime, timezone

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "jobs.json")


def load():
    if not os.path.exists(DATA_PATH):
        return {"updated_at": None, "jobs": {}}
    with open(DATA_PATH) as fh:
        return json.load(fh)


def save(state):
    state["updated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w") as fh:
        json.dump(state, fh, indent=2, sort_keys=True)
        fh.write("\n")


def merge(state, scraped_jobs, succeeded_companies):
    """Merge scraped Job objects into state.

    scraped_jobs: list[Job] from every company whose fetch SUCCEEDED.
    succeeded_companies: set of company display names that fetched without error.
    Returns (added, closed, reopened) lists of job dicts for reporting.
    """
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    jobs = state["jobs"]
    seen_uids = set()
    added, closed, reopened = [], [], []

    for job in scraped_jobs:
        uid = job.uid
        seen_uids.add(uid)
        if uid in jobs:
            entry = jobs[uid]
            if not entry.get("active", True):
                entry["active"] = True
                reopened.append(entry)
            # Workday's relative "30+ Days Ago" degrades to posted=None once a
            # posting ages past 30 days — keep the date we captured earlier.
            known_posted = entry.get("posted")
            entry.update(job.to_dict())
            if not entry.get("posted") and known_posted:
                entry["posted"] = known_posted
            entry["last_seen"] = today
        else:
            entry = job.to_dict()
            entry["first_seen"] = today
            entry["last_seen"] = today
            entry["active"] = True
            jobs[uid] = entry
            added.append(entry)

    for uid, entry in jobs.items():
        if uid in seen_uids or not entry.get("active", True):
            continue
        # Only close jobs for companies that scraped successfully this run.
        if entry["company"] in succeeded_companies:
            entry["active"] = False
            entry["closed"] = today
            closed.append(entry)

    return added, closed, reopened
