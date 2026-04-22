import requests

API_URL = "https://www.uber.com/api/loadSearchJobsResults?localeCode=en"
LIMIT = 100

HEADERS = {
    "content-type": "application/json",
    "origin": "https://www.uber.com",
    "referer": "https://www.uber.com/us/en/careers/list/",
    "x-csrf-token": "x",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/143.0.0.0 Safari/537.36"
    ),
}

PARAMS = {
    "department": ["Engineering", "University"],
    "location": [{"country": "USA"}],
}


def fetch(company="uber"):
    all_jobs = []
    page = 0
    try:
        while True:
            resp = requests.post(
                API_URL,
                headers=HEADERS,
                json={"limit": LIMIT, "page": page, "params": PARAMS},
                timeout=10,
            )
            resp.raise_for_status()
            data = resp.json().get("data", {})
            results = data.get("results", [])
            all_jobs.extend(results)
            total = data.get("totalResults", {}).get("low", 0)
            if len(all_jobs) >= total or not results:
                break
            page += 1
    except Exception as e:
        print(f"[ERROR] uber: {e}")

    return [
        {
            "id": str(job["id"]),
            "role": job.get("team", ""),
            "title": job["title"],
            "company": company,
            "location": ", ".join(filter(None, [
                job.get("location", {}).get("city"),
                job.get("location", {}).get("countryName"),
            ])),
            "link": f"https://www.uber.com/us/en/careers/list/{job['id']}/",
        }
        for job in all_jobs
    ]
