"""Microsoft careers (Eightfold pcsx tenant): apply.careers.microsoft.com.

num is hard-capped at 10 per page. "intern" and "internship" return different
sets, so both are queried and deduped.
"""
import time

from ..http import request_json
from ..models import Job, as_date

API = "https://apply.careers.microsoft.com/api/pcsx/search"
JOB_URL = "https://apply.careers.microsoft.com/careers/job/{id}"
PAGE = 10
MAX_PAGES = 40


def fetch(cfg):
    jobs, seen = [], set()
    for query in cfg.get("queries", ["intern", "internship"]):
        start = 0
        for _ in range(MAX_PAGES):
            data = request_json("GET", API, params={
                "domain": "microsoft.com", "query": query,
                "num": PAGE, "start": start})
            payload = data.get("data") or {}
            positions = payload.get("positions", [])
            for p in positions:
                pid = str(p.get("id", ""))
                if not pid or pid in seen:
                    continue
                seen.add(pid)
                jobs.append(Job(
                    company=cfg["name"],
                    external_id=pid,
                    title=p.get("name", ""),
                    url=JOB_URL.format(id=pid),
                    locations=[str(l) for l in p.get("locations", []) or []],
                    posted=as_date(p.get("postedTs") or p.get("creationTs")),
                ))
            start += PAGE
            if not positions or start >= payload.get("count", 0):
                break
            time.sleep(0.5)
    return jobs
