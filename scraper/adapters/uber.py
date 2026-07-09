"""Uber: POST https://www.uber.com/api/loadSearchJobsResults (dummy csrf token required).

The "text" search is loose full-text (matches "Internal Comms" etc.) — the
title filter in main.py does the real internship selection.
"""
import time

from ..http import request_json
from ..models import Job, as_date

API = "https://www.uber.com/api/loadSearchJobsResults?localeCode=en"
JOB_URL = "https://www.uber.com/global/en/careers/list/{id}/"
MAX_PAGES = 10


def fetch(cfg):
    jobs, page = [], 0
    total = None
    while page < MAX_PAGES:
        body = {"params": {"text": cfg.get("query", "intern")},
                "page": page, "limit": 100}
        data = request_json("POST", API, json_body=body, headers={
            "x-csrf-token": "x", "Content-Type": "application/json"})
        payload = data.get("data") or {}
        results = payload.get("results") or []
        total = (payload.get("totalResults") or {}).get("low", 0)
        for j in results:
            loc = j.get("location") or {}
            locations = ["{}, {}".format(loc.get("city", ""), loc.get("countryName", "")).strip(", ")]
            for extra in j.get("allLocations", []) or []:
                locations.append("{}, {}".format(
                    extra.get("city", ""), extra.get("countryName", "")).strip(", "))
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(j["id"]),
                title=j.get("title", ""),
                url=JOB_URL.format(id=j["id"]),
                locations=locations,
                posted=as_date(j.get("creationDate")),
            ))
        page += 1
        if not results or len(jobs) >= total:
            break
        time.sleep(0.5)
    return jobs
