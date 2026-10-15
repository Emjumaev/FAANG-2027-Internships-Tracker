"""Meta careers: unauthenticated GraphQL, but two quirks (verified):

1. Every request needs Sec-Fetch-* headers or Meta returns 400.
2. The POST needs an LSD token scraped from the jobsearch page HTML first.

doc_id is the Relay persisted-query id for CareersJobSearchResultsDataQuery;
it rotates with site deploys. If it dies the fetch raises, the workflow opens
a scraper-health issue, and the fix is grabbing the new id from the site's JS
bundle (module ...RelayOperation in static.xx.fbcdn.net).
"""
import json
import re

import requests

from ..http import USER_AGENT
from ..models import Job

PAGE_URL = "https://www.metacareers.com/jobsearch/"
GRAPHQL_URL = "https://www.metacareers.com/graphql"
JOB_URL = "https://www.metacareers.com/jobs/{id}"
DOC_ID = "27506805582236862"
LSD_RE = re.compile(r'"LSD",\[\],\{"token":"([^"]+)"')

NAV_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
}


def fetch(cfg):
    session = requests.Session()
    resp = session.get(PAGE_URL, headers=NAV_HEADERS, timeout=30)
    resp.raise_for_status()
    m = LSD_RE.search(resp.text)
    if not m:
        raise RuntimeError("could not extract LSD token from metacareers page")
    lsd = m.group(1)

    resp = session.post(GRAPHQL_URL, timeout=30, headers={
        "User-Agent": USER_AGENT,
        "Content-Type": "application/x-www-form-urlencoded",
        "x-fb-lsd": lsd,
        "Origin": "https://www.metacareers.com",
        "Referer": PAGE_URL,
        "Sec-Fetch-Dest": "empty", "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }, data={
        "lsd": lsd,
        "fb_api_caller_class": "RelayModern",
        "fb_api_req_friendly_name": "CareersJobSearchResultsDataQuery",
        "doc_id": DOC_ID,
        "variables": json.dumps({"search_input": {"q": cfg.get("query", "intern")}}),
    })
    resp.raise_for_status()
    data = resp.json()
    all_jobs = ((data.get("data") or {})
                .get("job_search_with_featured_jobs") or {}).get("all_jobs")
    if all_jobs is None:
        raise RuntimeError("meta graphql response missing all_jobs "
                           "(doc_id likely rotated): {}".format(str(data)[:200]))

    jobs = []
    for j in all_jobs:
        jobs.append(Job(
            company=cfg["name"],
            external_id=str(j["id"]),
            title=j.get("title", ""),
            url=JOB_URL.format(id=j["id"]),
            locations=j.get("locations", []) or [],
        ))
    return jobs
