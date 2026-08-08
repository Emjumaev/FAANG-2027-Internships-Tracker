"""Ashby job boards: https://api.ashbyhq.com/posting-api/job-board/{org}"""
from ..http import request_json
from ..models import Job, as_date

API = "https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=false"


def fetch(cfg):
    data = request_json("GET", API.format(org=cfg["org"]))
    jobs = []
    for j in data.get("jobs", []):
        if not j.get("isListed", True):
            continue
        locations = [j.get("location") or ""]
        for extra in j.get("secondaryLocations", []) or []:
            locations.append(extra.get("location", ""))
        jobs.append(Job(
            company=cfg["name"],
            external_id=str(j["id"]),
            title=j.get("title", ""),
            url=j.get("jobUrl") or j.get("applyUrl", ""),
            locations=locations,
            # Ashby carries an explicit employment type; trust it when it says
            # Intern, fall back to the title regex otherwise.
            is_intern=True if j.get("employmentType") == "Intern" else None,
            posted=as_date(j.get("publishedAt")),
        ))
    return jobs
