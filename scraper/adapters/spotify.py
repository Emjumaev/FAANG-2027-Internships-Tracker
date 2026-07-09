"""Spotify: https://api.lifeatspotify.com — j=internship filters by job type."""
from ..http import request_json
from ..models import Job

API = "https://api.lifeatspotify.com/wp-json/animal/v1/job/search"
JOB_URL = "https://www.lifeatspotify.com/jobs/{id}"


def fetch(cfg):
    data = request_json("GET", API, params={"c": "", "l": "", "j": "internship"})
    jobs = []
    for j in data.get("result", []):
        locations = [l.get("location", "") for l in j.get("locations", []) or []]
        jobs.append(Job(
            company=cfg["name"],
            external_id=str(j["id"]),
            title=j.get("text", ""),
            url=JOB_URL.format(id=j["id"]),
            locations=locations,
            is_intern=True,  # the j=internship filter already guarantees it
        ))
    return jobs
