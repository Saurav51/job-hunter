import requests

API_URL = "https://explore.jobs.netflix.net/api/apply/v2/jobs"

PARAMS = {
    "domain": "netflix.com",
    "location": "United States",
    "num": 100,
}


def fetch(company="netflix"):
    all_positions = []
    start = 0

    try:
        while True:
            resp = requests.get(API_URL, params={**PARAMS, "start": start}, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            positions = data.get("positions", [])
            if not positions:
                break
            all_positions.extend(positions)
            if len(all_positions) >= data.get("count", 0):
                break
            start += len(positions)
    except Exception as e:
        print(f"[ERROR] netflix: {e}")

    return [
        {
            "id": str(p["id"]),
            "role": p.get("department", ""),
            "title": p["name"],
            "company": company,
            "location": p.get("location", ""),
            "link": p.get("canonicalPositionUrl", f"https://explore.jobs.netflix.net/careers/job/{p['id']}"),
        }
        for p in all_positions
    ]
