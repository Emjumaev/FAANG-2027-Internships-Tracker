"""Wise (wise.jobs) — a SmartRecruiters Attrax careers site.

The listing is server-rendered 12 jobs per page with no usable page-size
parameter, and the public SmartRecruiters postings API returns nothing for
Wise. Cheapest reliable route: the vacancies sitemap lists every live job
URL (slug = "<title>-in-<city>-jid-<id>"), so we scan slugs for intern-ish
words and fetch only those pages, each of which embeds a schema.org
JobPosting JSON-LD block with the real title, location and datePosted.
"""
import json
import re

import requests

from ..http import USER_AGENT, request_json  # noqa: F401 (UA shared)
from ..models import Job, as_date, is_internship

SITEMAP = "https://wise.jobs/vacanciessitemap.xml"
LOC_RE = re.compile(r"<loc>\s*([^<]+?)\s*</loc>")
JID_RE = re.compile(r"-jid-(\d+)/?$")
LD_RE = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)
HEADERS = {"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"}


def _get(url):
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def _job_posting(html):
    for m in LD_RE.finditer(html):
        try:
            data = json.loads(m.group(1))
        except ValueError:
            continue
        if isinstance(data, dict) and data.get("@type") == "JobPosting":
            return data
    return None


def _locations(posting):
    out = []
    places = posting.get("jobLocation") or []
    if isinstance(places, dict):
        places = [places]
    for place in places:
        addr = (place or {}).get("address") or {}
        parts = [addr.get("addressLocality"), addr.get("addressRegion"), addr.get("addressCountry")]
        text = ", ".join(p for p in parts if p)
        if text:
            out.append(text)
    return out


def fetch(cfg):
    urls = LOC_RE.findall(_get(SITEMAP))
    if not urls:
        raise RuntimeError("wise sitemap listed no vacancies")
    jobs = []
    for url in urls:
        m = JID_RE.search(url)
        if not m:
            continue
        slug = url.rsplit("/", 1)[-1].replace("-", " ")
        if not is_internship(slug):
            continue  # slug mirrors the title, so this is a safe pre-filter
        posting = _job_posting(_get(url))
        if not posting:
            continue
        jobs.append(Job(
            company=cfg["name"],
            external_id=m.group(1),
            title=posting.get("title", ""),
            url=posting.get("url") or url,
            locations=_locations(posting),
            posted=as_date(posting.get("datePosted")),
        ))
    return jobs
