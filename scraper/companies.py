"""Company registry. Every entry: display name + adapter fetch fn + its config.

Endpoints were each verified by hand (2026-07). If one breaks, the workflow
opens a `scraper-health` issue automatically — see .github/workflows/update.yml.

"""
from .adapters import (amazon, apple, ashby, bloomberg, eightfold,
                       github_careers, google, greenhouse, ibm, janestreet,
                       meta, microsoft, oracle_hcm, phenom, spotify, uber,
                       wise, workday)

# Companies we can't cover, and why — rendered into the README summary table.
UNSUPPORTED = {
    "Revolut": ("revolut.com serves a 'quick security check' browser "
                "challenge to every non-browser client, careers pages and "
                "sitemaps included; needs a headless browser"),
    "TikTok": ("careers.tiktok.com now redirects to lifeattiktok.com, a "
               "Next.js app that loads jobs through server actions; the old "
               "/api/v1/search/job/posts endpoint answers 405 or an empty "
               "body; needs a headless browser"),
    "Tesla": ("careers site and its JSON API sit behind Akamai bot protection "
              "that returns 403 to every non-browser client; needs a headless browser"),
    "ByteDance": ("joinbytedance.com's job-search API rejects requests that "
                  "don't carry its in-browser client signature; needs a headless browser"),
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
    {"name": "Dropbox", "fetch": greenhouse.fetch, "token": "dropbox"},
    {"name": "Reddit", "fetch": greenhouse.fetch, "token": "reddit"},
    {"name": "Scale AI", "fetch": greenhouse.fetch, "token": "scaleai"},
    {"name": "Waymo", "fetch": greenhouse.fetch, "token": "waymo"},
    {"name": "Figma", "fetch": greenhouse.fetch, "token": "figma"},
    {"name": "DoorDash", "fetch": greenhouse.fetch, "token": "doordashusa"},
    {"name": "Lyft", "fetch": greenhouse.fetch, "token": "lyft"},
    {"name": "Coinbase", "fetch": greenhouse.fetch, "token": "coinbase"},
    {"name": "MongoDB", "fetch": greenhouse.fetch, "token": "mongodb"},

    # --- Ashby ---------------------------------------------------------------
    {"name": "OpenAI", "fetch": ashby.fetch, "org": "openai"},
    {"name": "Perplexity AI", "fetch": ashby.fetch, "org": "perplexity"},

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
    # Mastercard tags interns with a workerSubType facet, so filter on it
    # instead of the fuzzy "intern" text search (which matches ~700 postings).
    {"name": "Mastercard", "fetch": workday.fetch,
     "host": "mastercard.wd1.myworkdayjobs.com", "site": "CorporateCareers",
     "search_text": "",
     "applied_facets": {"workerSubType": ["cfba33fac07f49c9b6d3d53336c6a291"]}},
    # Visa likewise: its "Intern" jobFamily facet holds every intern posting.
    {"name": "Visa", "fetch": workday.fetch,
     "host": "visa.wd5.myworkdayjobs.com", "site": "Visa", "search_text": "",
     "applied_facets": {"jobFamily": ["2745bc1368021016a99151158b7a3a64"]}},

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
    {"name": "IBM", "fetch": ibm.fetch},
    {"name": "Wise", "fetch": wise.fetch},
]
