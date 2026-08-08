"""Company registry. Every entry: display name + adapter fetch fn + its config.

Endpoints were each verified by hand (2026-07). If one breaks, the workflow
opens a `scraper-health` issue automatically — see .github/workflows/update.yml.

"""
from .adapters import (amazon, apple, ashby, bloomberg, eightfold,
                       github_careers, google, greenhouse, janestreet, meta,
                       microsoft, oracle_hcm, phenom, spotify, uber, workday)

# Companies we can't cover, and why — rendered into the README summary table.
UNSUPPORTED = {
    "Citadel Securities": ("no API — entire site behind a Cloudflare browser "
                           "challenge; needs a headless browser"),
    "LinkedIn": ("careers site only links to linkedin.com/jobs, which is "
                 "authwalled and prohibits scraping"),
}

COMPANIES = [
    # --- Greenhouse boards ---------------------------------------------------
    {"name": "Airbnb", "fetch": greenhouse.fetch, "token": "airbnb"},
    {"name": "Anthropic", "fetch": greenhouse.fetch, "token": "anthropic"},
    {"name": "Cloudflare", "fetch": greenhouse.fetch, "token": "cloudflare"},
    {"name": "Databricks", "fetch": greenhouse.fetch, "token": "databricks"},
    {"name": "Hudson River Trading", "fetch": greenhouse.fetch, "token": "wehrtyou"},
    {"name": "Pinterest", "fetch": greenhouse.fetch, "token": "pinterest"},
    {"name": "Stripe", "fetch": greenhouse.fetch, "token": "stripe"},

    # --- Ashby ---------------------------------------------------------------
    {"name": "OpenAI", "fetch": ashby.fetch, "org": "openai"},

    # --- Workday CXS ---------------------------------------------------------
    {"name": "NVIDIA", "fetch": workday.fetch,
     "host": "nvidia.wd5.myworkdayjobs.com", "site": "NVIDIAExternalCareerSite"},
    {"name": "Adobe", "fetch": workday.fetch,
     "host": "adobe.wd5.myworkdayjobs.com", "site": "external_experienced"},
    {"name": "Salesforce", "fetch": workday.fetch,
     "host": "salesforce.wd12.myworkdayjobs.com", "site": "External_Career_Site"},
    {"name": "Intel", "fetch": workday.fetch,
     "host": "intel.wd1.myworkdayjobs.com", "site": "External"},
    {"name": "PayPal", "fetch": workday.fetch,
     "host": "paypal.wd1.myworkdayjobs.com", "site": "jobs"},
    {"name": "Snap", "fetch": workday.fetch,
     "host": "snapchat.wd1.myworkdayjobs.com", "tenant": "snapchat", "site": "snap"},

    # --- Eightfold -----------------------------------------------------------
    {"name": "Netflix", "fetch": eightfold.fetch,
     "host": "explore.jobs.netflix.net", "domain": "netflix.com"},

    # --- Phenom (/widgets) ---------------------------------------------------
    {"name": "Cisco", "fetch": phenom.fetch, "host": "careers.cisco.com",
     "job_url": "https://careers.cisco.com/global/en/job/{id}"},
    {"name": "Snowflake", "fetch": phenom.fetch, "host": "careers.snowflake.com",
     "job_url": "https://careers.snowflake.com/us/en/job/{id}",
     "body_overrides": {"lang": "en_us", "country": "us",
                        "all_fields": ["category", "country", "state", "city", "type"]}},

    # --- Custom --------------------------------------------------------------
    {"name": "Google", "fetch": google.fetch},
    {"name": "Meta", "fetch": meta.fetch},
    {"name": "Microsoft", "fetch": microsoft.fetch},
    {"name": "Amazon", "fetch": amazon.fetch},
    {"name": "Apple", "fetch": apple.fetch},
    {"name": "GitHub", "fetch": github_careers.fetch},
    {"name": "Jane Street", "fetch": janestreet.fetch},
    {"name": "Uber", "fetch": uber.fetch},
    {"name": "Oracle", "fetch": oracle_hcm.fetch},
    {"name": "Spotify", "fetch": spotify.fetch},
    {"name": "Bloomberg", "fetch": bloomberg.fetch},
]
