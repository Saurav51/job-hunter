import requests

GRAPHQL_URL = "https://jobs.ashbyhq.com/api/non-user-graphql"

QUERY = """
{
  jobBoardWithTeams(organizationHostedJobsPageName: "%s") {
    teams { id name }
    jobPostings { id title teamId }
  }
}
"""


def fetch(company):
    try:
        resp = requests.post(
            GRAPHQL_URL,
            json={"query": QUERY % company},
            timeout=10,
        )
        resp.raise_for_status()
        board = resp.json().get("data", {}).get("jobBoardWithTeams") or {}
        team_map = {t["id"]: t["name"] for t in board.get("teams", [])}
        return [
            {
                "id": job["id"],
                "role": team_map.get(job["teamId"], ""),
                "title": job["title"],
                "company": company,
                "link": f"https://jobs.ashbyhq.com/{company}/{job['id']}",
            }
            for job in board.get("jobPostings", [])
        ]
    except Exception as e:
        print(f"[ERROR] ashby/{company}: {e}")
        return []
