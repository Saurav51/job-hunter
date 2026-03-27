import json
import os

DATA_DIR = "data"


def _company_file(company):
    return os.path.join(DATA_DIR, f"{company}.json")


def load_jobs():
    if not os.path.exists(DATA_DIR):
        return set()
    keys = set()
    for filename in os.listdir(DATA_DIR):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(DATA_DIR, filename)) as f:
            for job in json.load(f):
                keys.add(f"{job['company']}:{job['id']}")
    return keys


def save_jobs(jobs):
    os.makedirs(DATA_DIR, exist_ok=True)
    by_company = {}
    for job in jobs:
        by_company.setdefault(job["company"], []).append(job)
    for company, company_jobs in by_company.items():
        with open(_company_file(company), "w") as f:
            json.dump(company_jobs, f, indent=2)
