"""Greenhouse job boards: https://boards-api.greenhouse.io/v1/boards/{token}/jobs"""
from ..http import request_json
from ..models import Job, as_date

API = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"


def fetch(cfg):
    data = request_json("GET", API.format(token=cfg["token"]))
    jobs = []
    for j in data.get("jobs", []):
        location = (j.get("location") or {}).get("name", "")
        jobs.append(Job(
            company=cfg["name"],
            external_id=str(j["id"]),
            title=j.get("title", ""),
            url=j.get("absolute_url", ""),
            locations=[loc.strip() for loc in location.split(";")] if location else [],
            posted=as_date(j.get("first_published")),
        ))
    return jobs
