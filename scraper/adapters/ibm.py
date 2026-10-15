"""IBM careers search (an Elasticsearch proxy behind www.ibm.com/careers/search).

POST https://www-api.ibm.com/search/api/v2
body: {"appId": "careers", "scopes": ["careers2"],
       "query": {"bool": {"must": [{"term": {"field_keyword_18": "Internship"}}]}},
       "_source": [...], "size": 100, "from": N}

Field map (the index uses anonymous keyword slots):
  field_keyword_05 = country, field_keyword_08 = job category,
  field_keyword_17 = work mode, field_keyword_18 = employment type,
  field_keyword_19 = "City, CC".
The index exposes no posting date, `_source` must be an explicit list of known
fields (anything else is rejected with "Invalid value"), `size` is capped at
100 (pages are walked with `from`), and the same jobId can appear more than
once (localized copies) — deduped here.
"""
import re

from ..http import request_json
from ..models import Job

API = "https://www-api.ibm.com/search/api/v2"
PAGE = 100
MAX_PAGES = 20
FIELDS = ["title", "url", "field_keyword_05", "field_keyword_08",
          "field_keyword_17", "field_keyword_18", "field_keyword_19"]
HEADERS = {"Content-Type": "application/json", "Origin": "https://www.ibm.com",
           "Referer": "https://www.ibm.com/careers/search"}
JOB_ID_RE = re.compile(r"jobId=(\d+)")


def fetch(cfg):
    jobs, seen, offset = [], set(), 0
    for _ in range(MAX_PAGES):
        body = {
            "appId": "careers", "scopes": ["careers2"],
            "query": {"bool": {"must": [{"term": {"field_keyword_18": "Internship"}}]}},
            "_source": FIELDS, "size": PAGE, "from": offset,
        }
        data = request_json("POST", API, json_body=body, headers=HEADERS)
        hits = (data.get("hits") or {}).get("hits") or []
        if not hits:
            break
        for h in hits:
            src = h.get("_source") or {}
            url = src.get("url", "")
            m = JOB_ID_RE.search(url)
            external_id = m.group(1) if m else h.get("_id", "")
            if external_id in seen:  # the index holds localized duplicates
                continue
            seen.add(external_id)
            city = src.get("field_keyword_19") or ""
            country = src.get("field_keyword_05") or ""
            # "Austin, US" + "United States" -> "Austin, United States"
            location = re.sub(r",\s*[A-Z]{2}$", ", " + country, city) if city and country else (city or country)
            jobs.append(Job(
                company=cfg["name"],
                external_id=external_id,
                title=src.get("title", ""),
                url=url,
                locations=[location] if location else [],
                # Employment type is "Internship" by query; titles like
                # "Duales Studium" or "Estudiante" wouldn't match the regex.
                is_intern=True,
            ))
        offset += PAGE
        if len(hits) < PAGE:
            break
    if not jobs:
        raise RuntimeError("ibm search returned no internships")
    return jobs
