"""Jane Street: https://www.janestreet.com/jobs/main.json

Internships are flagged by the `availability` field ("Summer Internship",
"Winter Internship", "Winter Co-Op"), not the title, so we mark is_intern
explicitly and fold the season into the displayed title.
"""
from ..http import request_json
from ..models import Job

API = "https://www.janestreet.com/jobs/main.json"
JOB_URL = "https://www.janestreet.com/join-jane-street/position/{id}/"


def fetch(cfg):
    data = request_json("GET", API)
    jobs = []
    for j in data:
        availability = j.get("availability") or ""
        is_intern = any(k in availability.lower() for k in ("internship", "co-op"))
        title = j.get("position", "")
        if is_intern and availability:
            title = "{} ({})".format(title, availability)
        jobs.append(Job(
            company=cfg["name"],
            external_id=str(j["id"]),
            title=title,
            url=JOB_URL.format(id=j["id"]),
            locations=[j.get("city", "")],
            is_intern=is_intern,
        ))
    return jobs
