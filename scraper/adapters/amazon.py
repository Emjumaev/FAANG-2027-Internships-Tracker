"""Amazon: https://www.amazon.jobs/en/search.json

Two passes, deduped: a full-text "intern" query plus the studentprograms
business category (which catches internships whose titles the query misses).
"""
import time

from ..http import request_json
from ..models import Job, as_date

API = "https://www.amazon.jobs/en/search.json"
PAGE = 100
MAX_PAGES = 10

PASSES = [
    {"base_query": "intern"},
    {"business_category[]": "studentprograms"},
]


def fetch(cfg):
    jobs, seen = [], set()
    for base_params in PASSES:
        offset = 0
        for _ in range(MAX_PAGES):
            params = dict(base_params, result_limit=PAGE, offset=offset)
            data = request_json("GET", API, params=params)
            batch = data.get("jobs", [])
            for j in batch:
                jid = str(j.get("id_icims") or j.get("id", ""))
                if not jid or jid in seen:
                    continue
                seen.add(jid)
                jobs.append(Job(
                    company=cfg["name"],
                    external_id=jid,
                    title=j.get("title", ""),
                    url="https://www.amazon.jobs{}".format(j.get("job_path", "")),
                    locations=[j.get("normalized_location", "")],
                    posted=as_date(j.get("posted_date")),
                ))
            offset += PAGE
            if not batch or offset >= data.get("hits", 0):
                break
            time.sleep(0.5)
    return jobs
