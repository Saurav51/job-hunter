import requests


def fetch(company, name=None):
    board = company
    name = name or company
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
        return [
            {
                "id": str(job["id"]),
                "role": job["departments"][0]["name"] if job.get("departments") else "",
                "title": job["title"],
                "company": name,
                "location": job.get("location", {}).get("name", ""),
                "link": job["absolute_url"],
            }
            for job in jobs
        ]
    except Exception as e:
        print(f"[ERROR] greenhouse/{board}: {e}")
        return []
