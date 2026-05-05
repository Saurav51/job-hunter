import re

from adapters.ats import greenhouse, ashby
from adapters.companies import uber, google, netflix


_NA_PATTERNS = re.compile(
    r'\bus\b|\busa\b|u\.s\.|united states|north america'
    r'|us.?remote|remote.?us|remote in the us'
    r'|canada|toronto|vancouver|montreal'
    r'|mexico'
    r'|\bsf\b|\bsfo\b|san francisco|south san francisco'
    r'|\bnyc\b|\bny\b|new york'
    r'|\bsea\b|seattle'
    r'|\bchi\b|chicago'
    r'|atlanta|\bdc\b|washington dc'
    r'|boston|austin|los angeles|privy',
    re.IGNORECASE,
)
_NA_SKIP = {'n/a', 'location', '', 'remote', 'na'}

def _is_na(job):
    loc = job.get('location', '').strip()
    return loc.lower() not in _NA_SKIP and bool(_NA_PATTERNS.search(loc))


def _is_doordash_engineering(job):
    # DoorDash uses 31x (310-319) and 34x (341-349) for Engineering departments
    return bool(re.match(r'^3[14][0-9] ', job['role'])) or 'engineering' in job['role'].lower()


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    stripe = greenhouse.fetch("stripe")
    jobs += [j for j in stripe if _is_na(j)]
    doordash = greenhouse.fetch("doordashusa", name="doordash")
    jobs += [j for j in doordash if _is_doordash_engineering(j)]
    jobs += ashby.fetch("perplexity")
    jobs += ashby.fetch("openai")
    jobs += ashby.fetch("ramp")
    snowflake = ashby.fetch("snowflake")
    jobs += [j for j in snowflake if j['role'] in ('Engineering', 'Data Analytics and AI')]
    jobs += uber.fetch("uber")
    jobs += google.fetch("google")
    jobs += netflix.fetch("netflix")
    return jobs
