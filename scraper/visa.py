"""Per-company visa-sponsorship stance for internships.

This is hand-maintained reference data, not scraped: each entry was checked
against the company's student FAQ or the wording of its current intern
postings (see `source`). Policies change and individual postings override the
company default, so the listing itself is always the final word.

status values:
  "yes"      sponsors intern visas / explicitly accepts candidates who need one
  "limited"  case-by-case — depends on the role, country or visa type
  "no"       postings require existing work authorization, no sponsorship
  "unknown"  nothing conclusive published
"""

STATUS_LABEL = {
    "yes": "✅ Sponsors",
    "limited": "⚠️ Case-by-case",
    "no": "❌ No sponsorship",
    "unknown": "❔ Unknown",
}

VISA = {
    "Adobe": {
        "status": "limited",
        "note": "US 2027 SWE intern posting silent on sponsorship; F-1 CPT/OPT reported OK (secondary); some non-US postings bar sponsorship",
        "source": "https://builtin.com/job/2026-intern-software-engineer/7422310",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Airbnb": {
        "status": "no",
        "note": "SWE intern posting requires US work authorization; CPT/OPT accepted but no visa sponsorship (no J-1)",
        "source": "https://builtin.com/job/software-engineering-intern/7916098",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Amazon": {
        "status": "limited",
        "note": "Decided per posting: SDE intern postings silent; several non-SDE postings say 'unable to offer visa sponsorship'",
        "source": "https://amazon.jobs/en/jobs/2713207/2025-program-manager-intern",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Anthropic": {
        "status": "no",
        "note": "No traditional SWE internship; Fellows Program requires existing US/UK/CA work authorization, no visas",
        "source": "https://jobs.accel.com/companies/anthropic/jobs/74068663-anthropic-fellows-program",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Apple": {
        "status": "limited",
        "note": "US intern postings state no sponsorship policy either way; F-1 CPT/OPT typically used; confirm per role with recruiter",
        "source": "https://www.extern.com/post/apple-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Bloomberg": {
        "status": "limited",
        "note": "Non-eng NY intern post: no sponsorship now or future; eng interns reportedly sponsored case-by-case (secondary)",
        "source": "https://www.extern.com/post/bloomberg-internship-guide",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Cisco": {
        "status": "no",
        "note": "US SWE I Intern posting: must be a U.S. citizen with no need for visa sponsorship; other US intern roles say the same",
        "source": "https://jobright.ai/jobs/info/6a0bf82d963f7a67d95d42af",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Cloudflare": {
        "status": "limited",
        "note": "US postings silent on sponsorship (export-control clause only); secondary guide: F-1 CPT accepted",
        "source": "https://job-boards.greenhouse.io/cloudflare/jobs/7738938",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Coinbase": {
        "status": "limited",
        "note": "Posting silent; secondary guide: sponsorship for US roles possible, approval needed, covers internship only",
        "source": "https://www.extern.com/post/coinbase-internship-guide",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Databricks": {
        "status": "limited",
        "note": "Official 2027 SWE intern posting silent on sponsorship; secondary guide: valid CPT required for US roles",
        "source": "https://www.databricks.com/company/careers/university-recruiting/software-engineering-intern-2026-6865687002",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "DoorDash": {
        "status": "limited",
        "note": "Must be US work-authorized; F-1 students OK on CPT; J-1 not supported; no H-1B sponsorship for interns",
        "source": "https://jobs.khoslaventures.com/companies/doordash/jobs/60070337-software-engineer-intern-summer-2026-us",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Dropbox": {
        "status": "unknown",
        "note": "Summer 2027 SWE intern posting silent on visas; US-remote only, 'all authorized locations'; CPT likely OK",
        "source": "https://jobs.accel.com/companies/dropbox/jobs/92531026-software-engineering-intern-summer-2027",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Figma": {
        "status": "unknown",
        "note": "SWE intern postings (SF/NYC) do not mention work auth; Wellfound lists other intern roles as 'sponsorship not available'",
        "source": "https://www.extern.com/post/figma-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "GitHub": {
        "status": "unknown",
        "note": "Remote-US SWE intern postings contain no sponsorship or work-authorization wording; no official FAQ found",
        "source": "https://nodesk.co/remote-jobs/github-software-engineering-intern/",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Google": {
        "status": "limited",
        "note": "F-1 students on CPT/OPT hired (secondary reports); all non-US 2026 postings say 'not eligible for immigration sponsorship'",
        "source": "https://jobs.anitab.org/companies/google-24698/jobs/58499871-software-engineering-site-reliability-engineering-bs-ms-intern-2026",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Hudson River Trading": {
        "status": "yes",
        "note": "Intern postings list 'Work Visa Sponsorship' as a benefit; no authorization clause; CPT reported accepted",
        "source": "https://www.themuse.com/jobs/hudsonrivertrading/software-engineering-internship-c-or-python-summer-2027",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "IBM": {
        "status": "no",
        "note": "US 2026 Software Developer Intern postings: no visa sponsorship now or in future; need own work authorization",
        "source": "https://www.themuse.com/jobs/ibm/software-developer-internship-2026",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Intel": {
        "status": "no",
        "note": "2026/2027 US intern postings: not eligible for employment-based visa sponsorship (Intel sponsors only MS/PhD STEM roles)",
        "source": "https://builtin.com/job/software-engineering-intern-bachelor-s/7557806",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Jane Street": {
        "status": "yes",
        "note": "Internships in NY/London/HK; postings arrange visas, flights and housing; no authorization clause in US roles",
        "source": "https://jobsconnect.prosple.com/graduate-employers/jane-street/jobs-internships/software-engineer-internship",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Lyft": {
        "status": "unknown",
        "note": "Summer 2027 SF intern postings silent on visas; F-1 students can use CPT; sponsorship beyond CPT unconfirmed",
        "source": "https://www.extern.com/post/lyft-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Mastercard": {
        "status": "no",
        "note": "US 2026 intern postings: not eligible for sponsorship; F-1 students incl. CPT/OPT are excluded",
        "source": "https://builtin.com/job/platform-engineering-intern-summer-2026-st-louis-mo/7232224",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Meta": {
        "status": "limited",
        "note": "Postings require work authorization at hire (F-1 CPT works); J-1 for Canadian/abroad students reported on Blind (secondary)",
        "source": "https://jobs.anitab.org/companies/meta-3-c00df464-9d7f-4a12-a5c0-f043ccf7bf75/jobs/58835198-software-engineer-intern-co-op",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Microsoft": {
        "status": "limited",
        "note": "No blanket policy; F-1 CPT/OPT accepted in US; some country postings (e.g. Israel) say interns cannot be sponsored",
        "source": "https://flexa.careers/jobs/microsoft-software-engineer-internship-opportunities-66e806d24731caf085f888f7",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "MongoDB": {
        "status": "limited",
        "note": "Must be authorized to work in the US; posting says sponsorship may be available for certain roles",
        "source": "https://jobs.alleycorp.com/companies/mongodb/jobs/58571316-2026-software-engineering-intern-amer",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "NVIDIA": {
        "status": "limited",
        "note": "Intern JDs don't state a sponsorship policy; heavy H-1B sponsor overall; F-1 CPT/OPT used; ask recruiter per role",
        "source": "https://www.extern.com/post/nvidia-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Netflix": {
        "status": "limited",
        "note": "Summer 2026 SWE intern posting has no sponsorship statement; F-1 CPT used; decided per team, ask recruiter",
        "source": "https://www.extern.com/post/netflix-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "OpenAI": {
        "status": "limited",
        "note": "SF intern postings silent on visas (relocation support only); Residency sponsors visas; ask recruiter",
        "source": "https://jobs.stripes.co/companies/openai/jobs/65336977-software-engineer-internship-co-op-applied-emerging-talent-fall-2026",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Oracle": {
        "status": "no",
        "note": "US intern postings: no sponsorship now or ever (H-1B, OPT, CPT, F-1 all excluded); must have US work auth",
        "source": "https://simplify.jobs/p/c8105a36-7da9-4019-bfdb-e9668188553d/Java-Software-Engineer-Intern",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "PayPal": {
        "status": "limited",
        "note": "Postings require ability to obtain US work authorization for the summer; sponsorship case-by-case, not guaranteed",
        "source": "https://www.extern.com/post/paypal-internship-guide",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Pinterest": {
        "status": "no",
        "note": "US SWE intern postings require current US authorization with no sponsorship now or in future; US-based only",
        "source": "https://builtin.com/job/software-engineer-intern-2026/7199234",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Reddit": {
        "status": "no",
        "note": "Intern JDs state sponsorship not available; must be authorized to work in the US (secondary report of JD text)",
        "source": "https://www.extern.com/post/reddit-internship-guide",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Salesforce": {
        "status": "limited",
        "note": "F-1 CPT students at US/Canadian schools eligible; J-1 from abroad rare; some postings 'ineligible for visa sponsorship'",
        "source": "https://www.extern.com/post/salesforce-internship-guide",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Scale AI": {
        "status": "unknown",
        "note": "Summer 2027 SF SWE intern posting silent on visas; secondary says US work auth required, sponsorship unconfirmed",
        "source": "https://jobs.accel.com/companies/scale-ai/jobs/92358520-software-engineering-intern-summer-2027",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Snap": {
        "status": "limited",
        "note": "LA SWE intern posting silent; secondary guide says interns need existing authorization, no sponsorship/relocation",
        "source": "https://blog.internset.com/what-are-the-eligibility-criteria-for-snap-internships/",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Snowflake": {
        "status": "limited",
        "note": "US SWE intern postings silent on sponsorship; secondary guide: F-1 CPT accepted, no J-1 sponsorship",
        "source": "https://www.extern.com/post/snowflake-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Spotify": {
        "status": "no",
        "note": "NYC intern postings require existing US work authorization for June-Aug; no sponsorship mentioned",
        "source": "https://jobs.lever.co/spotify/4261f025-4ea4-4d24-9edd-ec0db9696152",
        "confidence": "high",
        "checked": "2026-10-15",
    },
    "Stripe": {
        "status": "limited",
        "note": "Official intern postings silent; secondary: CPT accepted for F-1 interns, sponsorship confirm with recruiter",
        "source": "https://www.extern.com/post/stripe-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
    "Uber": {
        "status": "limited",
        "note": "US SWE intern postings silent on sponsorship; CPT typical but unconfirmed; confirm with recruiter",
        "source": "https://www.themuse.com/jobs/uber/2026-software-engineering-internship-amsterdam",
        "confidence": "medium",
        "checked": "2026-10-15",
    },
    "Waymo": {
        "status": "unknown",
        "note": "2027 intern postings silent on visas; secondary guide says US work auth required, H-1B not standard for interns",
        "source": "https://www.extern.com/post/waymo-internship-guide",
        "confidence": "low",
        "checked": "2026-10-15",
    },
}


def visa_for(company):
    """Visa info dict for a company; a harmless 'unknown' entry when unlisted."""
    info = VISA.get(company) or {}
    status = info.get("status", "unknown")
    if status not in STATUS_LABEL:
        raise ValueError("bad visa status {!r} for {}".format(status, company))
    return {
        "status": status,
        "label": STATUS_LABEL[status],
        "note": info.get("note", ""),
        "source": info.get("source", ""),
        "checked": info.get("checked", ""),
    }
