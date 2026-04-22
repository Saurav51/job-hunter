import re
import json
import requests

BASE_URL = "https://www.google.com/about/careers/applications/jobs/results"

PARAMS = {
    "location": "United States",
    "target_level": ["MID", "EARLY"],
    "employment_type": "FULL_TIME",
    "q": '"Software Engineer"',
}

HEADERS = {
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    ),
}

DATA_RE = re.compile(
    r"AF_initDataCallback\(\{key: 'ds:1', hash: '\d+', data:(\[.*\]), sideChannel",
    re.DOTALL,
)


def _parse(html):
    m = DATA_RE.search(html)
    if not m:
        return [], 0, None
    data = json.loads(m.group(1))
    jobs_raw = data[0]       # list of jobs on this page
    total    = data[2]       # total result count
    next_off = data[3]       # next page offset (int), None when done
    return jobs_raw, total, next_off


def fetch(company="google"):
    all_jobs = []
    page_id = "none"

    try:
        while True:
            params = {**PARAMS, "pageId": page_id}
            resp = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
            resp.raise_for_status()

            jobs_raw, total, next_off = _parse(resp.text)
            all_jobs.extend(jobs_raw)

            if not jobs_raw or next_off is None or len(all_jobs) >= total:
                break
            page_id = next_off

    except Exception as e:
        print(f"[ERROR] google: {e}")

    return [
        {
            "id": str(job[0]),
            "role": "",
            "title": job[1],
            "company": company,
            "location": job[9][0][0] if job[9] else "",
            "link": f"https://www.google.com/about/careers/applications/jobs/results/{job[0]}",
        }
        for job in all_jobs
    ]
