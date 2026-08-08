"""Oracle HCM public requisitions API (Oracle careers).

The finder-string param syntax is exact — offset lives inside the finder.
Keyword search is full-text, so the title filter in main.py does the real work.
"""
import time

from ..http import request_json
from ..models import Job, as_date

API = ("https://eeho.fa.us2.oraclecloud.com/hcmRestApi/resources/latest/"
       "recruitingCEJobRequisitions")
JOB_URL = "https://careers.oracle.com/jobs/#en/sites/jobsearch/job/{id}"
PAGE = 100
MAX_PAGES = 30


def fetch(cfg):
    site = cfg.get("site_number", "CX_45001")
    keyword = cfg.get("query", "intern")
    jobs, offset, total = [], 0, None
    for _ in range(MAX_PAGES):
        finder = ('findReqs;siteNumber={site},keyword="{kw}",limit={limit},'
                  'offset={offset}').format(site=site, kw=keyword,
                                            limit=PAGE, offset=offset)
        params = {"onlyData": "true",
                  "expand": "requisitionList.secondaryLocations",
                  "finder": finder}
        data = request_json("GET", API, params=params)
        items = data.get("items") or [{}]
        reqs = items[0].get("requisitionList", [])
        total = items[0].get("TotalJobsCount", 0)
        for r in reqs:
            locations = [r.get("PrimaryLocation", "")]
            for sec in r.get("secondaryLocations", []) or []:
                locations.append(sec.get("Name", ""))
            jobs.append(Job(
                company=cfg["name"],
                external_id=str(r["Id"]),
                title=r.get("Title", ""),
                url=JOB_URL.format(id=r["Id"]),
                locations=locations,
                posted=as_date(r.get("PostedDate")),
            ))
        offset += PAGE
        if not reqs or offset >= total:
            break
        time.sleep(0.5)
    return jobs
