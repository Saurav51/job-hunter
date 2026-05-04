import re

from adapters.ats import greenhouse, ashby
from adapters.companies import uber, google, netflix


def _is_doordash_engineering(job):
    # DoorDash uses 31x (310-319) and 34x (341-349) for Engineering departments
    return bool(re.match(r'^3[14][0-9] ', job['role'])) or 'engineering' in job['role'].lower()


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    doordash = greenhouse.fetch("doordashusa", name="doordash")
    jobs += [j for j in doordash if _is_doordash_engineering(j)]
    jobs += ashby.fetch("perplexity")
    jobs += ashby.fetch("openai")
    jobs += ashby.fetch("ramp")
    jobs += uber.fetch("uber")
    jobs += google.fetch("google")
    jobs += netflix.fetch("netflix")
    return jobs
