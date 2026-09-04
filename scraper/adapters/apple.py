"""Apple: POST https://jobs.apple.com/api/v1/search

The "format" object in the body is REQUIRED — without it the API silently
returns zero results. query="internship" is clean (Apple stems it to match
"Intern" titles too); query="intern" matches internal/IN- retail codes.
"""
import time

from ..http import request_json
from ..models import Job, as_date

API = "https://jobs.apple.com/api/v1/search"
JOB_URL = "https://jobs.apple.com/en-us/details/{position_id}/{slug}"
PAGE = 20
MAX_PAGES = 30


def fetch(cfg):
    jobs, page, total = [], 1, None
    while page <= MAX_PAGES:
        body = {"query": cfg.get("query", "internship"), "filters": {},
                "page": page, "locale": "en-us", "sort": "",
                "format": {"longDate": "MMMM D, YYYY", "mediumDate": "MMM D, YYYY"}}
        data = request_json("POST", API, json_body=body,
                            headers={"Content-Type": "application/json"})
        res = data.get("res") or {}
        results = res.get("searchResults", [])
        if total is None:
            total = res.get("totalRecords", 0)
        if page == 1 and not results:
            raise RuntimeError("apple search returned no results — "
                               "did the required 'format' body field change?")
        for j in results:
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(j.get("positionId") or j.get("id", "")),
                title=j.get("postingTitle", ""),
                url=JOB_URL.format(position_id=j.get("positionId", ""),
                                   slug=j.get("transformedPostingTitle", "")),
                locations=[l.get("name", "") for l in j.get("locations", []) or []],
                posted=as_date(j.get("postDateInGMT")),
            ))
        if len(jobs) >= total or not results:
            break
        page += 1
        time.sleep(0.5)
    return jobs
