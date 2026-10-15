"""Phenom People career sites (Cisco, Snowflake): POST {host}/widgets"""
import time

from ..http import request_json
from ..models import Job, as_date

MAX_PAGES = 10


def fetch(cfg):
    host = cfg["host"]                    # e.g. "careers.cisco.com"
    job_url_tpl = cfg["job_url"]          # e.g. "https://careers.cisco.com/global/en/job/{id}"
    base_body = {
        "lang": "en", "deviceType": "desktop", "country": "global",
        "pageName": "search-results", "ddoKey": "refineSearch", "sortBy": "",
        "subsearch": "", "from": 0, "jobs": True, "counts": True,
        "all_fields": ["category", "country", "state", "city"],
        "size": 100, "clearAll": False, "jdsource": "facets",
        "isSliderEnable": False, "pageId": "page16", "siteType": "external",
        "keywords": cfg.get("keywords", "intern"), "global": True,
        "selected_fields": {}, "locationData": {},
    }
    base_body.update(cfg.get("body_overrides", {}))

    jobs, offset = [], 0
    for _ in range(MAX_PAGES):
        body = dict(base_body, **{"from": offset})
        data = request_json("POST", "https://{}/widgets".format(host),
                            json_body=body,
                            headers={"Content-Type": "application/json"})
        refine = data.get("refineSearch", {})
        batch = (refine.get("data") or {}).get("jobs", [])
        for j in batch:
            locations = [j.get("cityStateCountry", "")] or []
            if not locations[0]:
                locations = [", ".join(x for x in
                                       (j.get("city"), j.get("state"), j.get("country")) if x)]
            for ml in j.get("multi_location", []) or []:
                if isinstance(ml, str):
                    locations.append(ml)
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(j.get("jobId", "")),
                title=j.get("title", ""),
                url=job_url_tpl.format(id=j.get("jobId", "")),
                locations=locations,
                posted=as_date(j.get("postedDate") or j.get("dateCreated")),
            ))
        offset += len(batch)
        if not batch or offset >= refine.get("totalHits", 0):
            break
        time.sleep(0.5)
    return jobs
