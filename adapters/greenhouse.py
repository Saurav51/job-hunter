import requests


def fetch(company):
    url = f"https://boards-api.greenhouse.io/v1/boards/{company}/jobs?content=true"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        return [
            {
                "id": str(job["id"]),
                "role": job["departments"][0]["name"] if job.get("departments") else "",
                "title": job["title"],
                "company": company,
                "link": job["absolute_url"],
            }
            for job in jobs
        ]
    except Exception as e:
        print(f"[ERROR] greenhouse/{company}: {e}")
        return []
