import json
import os
from datetime import datetime

from fetch import fetch_all
from storage import load_jobs, save_jobs

RESULTS_DIR = "results"


def next_run_number():
    if not os.path.exists(RESULTS_DIR):
        return 1
    files = [f for f in os.listdir(RESULTS_DIR) if f.endswith(".json")]
    if not files:
        return 1
    nums = [int(f.split("_")[0]) for f in files if f.split("_")[0].isdigit()]
    return max(nums) + 1 if nums else 1


def save_results(new_jobs):
    os.makedirs(RESULTS_DIR, exist_ok=True)
    n = next_run_number()
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(RESULTS_DIR, f"{n}_{ts}.json")

    by_company = {}
    for job in new_jobs:
        by_company.setdefault(job["company"], []).append(job)

    with open(path, "w") as f:
        json.dump(by_company, f, indent=2)

    print(f"Results saved to {path}")


def main():
    current_jobs = fetch_all()
    current_keys = {f"{job['company']}:{job['id']}" for job in current_jobs}
    previous_keys = load_jobs()
    new_keys = current_keys - previous_keys
    new_jobs = [job for job in current_jobs if f"{job['company']}:{job['id']}" in new_keys]

    if new_jobs:
        print(f"Found {len(new_jobs)} new job(s):\n")
        for job in new_jobs:
            loc = f" · {job['location']}" if job.get('location') else ""
            print(f"  [{job['company']}] {job['title']}{loc}")
            print(f"  {job['link']}\n")
    else:
        print("No new jobs.")

    save_results(new_jobs)

    save_jobs(current_jobs)


if __name__ == "__main__":
    main()
