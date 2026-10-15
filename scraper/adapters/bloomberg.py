"""Bloomberg: Avature board at bloomberg.avature.net — server-rendered HTML only.

Markup per posting (stable Avature classes):
  <h3 class="article__header__text__title ..."><a class="link" href=".../careers/JobDetail/{slug}/{id}">{title}</a></h3>
  <span class="list-item-location">{location}</span>
Pagination via ?jobOffset=N (12 per page).
"""
import re
import time

import requests

from ..http import USER_AGENT
from ..models import Job

SEARCH_URL = "https://bloomberg.avature.net/careers/SearchJobs/{query}"
PAGE = 12
MAX_PAGES = 30

TITLE_RE = re.compile(
    r'href="(https://bloomberg\.avature\.net/careers/JobDetail/[^"/]+/(\d+))">\s*'
    r'([^<]+?)\s*</a>\s*</h3>')
LOCATION_RE = re.compile(r'<span class="list-item-location">([^<]*)</span>')


def fetch(cfg):
    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    query = cfg.get("query", "intern")

    jobs, seen, offset = [], set(), 0
    for _ in range(MAX_PAGES):
        resp = session.get(SEARCH_URL.format(query=query),
                           params={"jobOffset": offset} if offset else None,
                           timeout=30)
        resp.raise_for_status()
        found_new = False
        # one <article> per posting; parse title and location within each block
        for block in resp.text.split("<article")[1:]:
            m = TITLE_RE.search(block)
            if not m:
                continue
            url, job_id, title = m.groups()
            if job_id in seen:
                continue
            seen.add(job_id)
            found_new = True
            loc = LOCATION_RE.search(block)
            jobs.append(Job(
                company=cfg["name"],
                external_id=job_id,
                title=title.strip(),
                url=url,
                locations=[loc.group(1).strip()] if loc else [],
            ))
        if not found_new:
            break
        offset += PAGE
        time.sleep(0.5)
    return jobs
