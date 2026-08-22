"""GitHub careers (JIBE/Radancy): https://www.github.careers/api/jobs"""
from ..http import request_json
from ..models import Job, as_date

API = "https://www.github.careers/api/jobs"


def fetch(cfg):
    jobs, page = [], 1
    while page <= 10:
        data = request_json("GET", API, params={"page": page, "limit": 100})
        batch = data.get("jobs", [])
        for wrapper in batch:
            j = wrapper.get("data", {})
            url = (j.get("meta_data") or {}).get("canonical_url", "")
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(j.get("req_id") or j.get("slug", "")),
                title=j.get("title", ""),
                url=url,
                locations=[j.get("location_name") or j.get("full_location", "")],
                posted=as_date(j.get("posted_date") or j.get("create_date")),
            ))
        if len(jobs) >= data.get("totalCount", 0) or not batch:
            break
        page += 1
    return jobs
