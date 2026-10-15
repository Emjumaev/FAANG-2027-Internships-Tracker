"""Google careers: server-rendered results page with embedded AF_initDataCallback JSON.

employment_type=INTERN filters server-side (verified), so every result is an
internship. Jobs are positional arrays: job[0]=id, job[1]=title,
job[9]=locations (each loc[0] is the display string).
"""
import json
import re
import time

import requests

from ..http import USER_AGENT
from ..models import Job, as_date

URL = "https://www.google.com/about/careers/applications/jobs/results"
JOB_URL = "https://www.google.com/about/careers/applications/jobs/results/{id}"
DATA_RE = re.compile(r"AF_initDataCallback\(\{key: 'ds:1'.*?data:(\[.*?\]), sideChannel",
                     re.DOTALL)
MAX_PAGES = 20


def fetch(cfg):
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    jobs, page = [], 1
    while page <= MAX_PAGES:
        resp = session.get(URL, params={"q": cfg.get("query", "intern"),
                                        "employment_type": "INTERN",
                                        "page": page}, timeout=30)
        resp.raise_for_status()
        m = DATA_RE.search(resp.text)
        if not m:
            if page == 1:
                raise RuntimeError("could not find ds:1 payload on Google careers page")
            break
        data = json.loads(m.group(1))
        raw_jobs = data[0]
        if not raw_jobs:
            break
        for j in raw_jobs:
            locations = [loc[0] for loc in (j[9] or []) if loc and loc[0]]
            # slot 12 is [epoch_seconds, nanos] — the oldest of the job's three
            # timestamps, i.e. its publication time (13/14 are modifications)
            ts = j[12][0] if len(j) > 12 and isinstance(j[12], list) and j[12] else None
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(j[0]),
                title=j[1] or "",
                url=JOB_URL.format(id=j[0]),
                locations=locations,
                is_intern=True,  # employment_type=INTERN is filtered server-side
                posted=as_date(ts),
            ))
        total = data[2] if len(data) > 2 and isinstance(data[2], int) else 0
        if len(jobs) >= total:
            break
        page += 1
        time.sleep(0.5)
    return jobs
