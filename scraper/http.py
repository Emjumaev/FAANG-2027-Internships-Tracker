"""Thin HTTP helper with retries, timeouts and a browser-ish user agent."""
import time

import requests

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
)

DEFAULT_TIMEOUT = 30
RETRIES = 3
BACKOFF_SECONDS = 5


def request_json(method, url, *, headers=None, params=None, json_body=None,
                 data=None, cookies=None, session=None, timeout=DEFAULT_TIMEOUT):
    """Perform a request expecting a JSON response. Retries on 5xx/429/network errors."""
    h = {"User-Agent": USER_AGENT, "Accept": "application/json"}
    if headers:
        h.update(headers)
    client = session or requests
    last_err = None
    for attempt in range(RETRIES):
        try:
            resp = client.request(
                method, url, headers=h, params=params, json=json_body,
                data=data, cookies=cookies, timeout=timeout,
            )
            if resp.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError("HTTP {}".format(resp.status_code), response=resp)
            resp.raise_for_status()
            return resp.json()
        except (requests.RequestException, ValueError) as err:
            last_err = err
            if attempt < RETRIES - 1:
                time.sleep(BACKOFF_SECONDS * (attempt + 1))
    raise RuntimeError("request failed after {} attempts: {} {} ({})".format(
        RETRIES, method, url, last_err))
