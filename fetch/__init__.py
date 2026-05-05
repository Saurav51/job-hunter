import re

from adapters.ats import greenhouse, ashby
from adapters.companies import uber, google, netflix


_US_RE = re.compile(
    r'\bus\b|\busa\b|u\.s\.|united states'
    r'|us.?remote|remote.?us|remote in the us'
    r'|\bsf\b|\bsfo\b|san francisco|south san francisco'
    r'|\bnyc\b|\bny\b|new york|\bsea\b|seattle'
    r'|\bchi\b|chicago|atlanta|\bdc\b|washington'
    r'|boston|austin|los angeles|privy',
    re.IGNORECASE,
)
_NON_US_RE = re.compile(
    r'bengaluru|bangalore|\bindia\b|\bin\s*-'
    r'|dublin|ireland|luxembourg'
    r'|\blondon\b|united kingdom|\buk\b'
    r'|\bsingapore\b|\btokyo\b|\bjapan\b'
    r'|\bsydney\b|\bmelbourne\b|\baustralia\b'
    r'|\bberlin\b|\bgermany\b|\bspain\b|barcelona|madrid'
    r'|milan|\brome\b|\bparis\b|\bfrance\b'
    r'|\bdubai\b|\buae\b|emea|apac'
    r'|stockholm|sweden|amsterdam|brussels|belgium'
    r'|toronto|vancouver|\bcanada\b|ca-toronto|british columbia'
    r'|mexico|\bdubin\b|\bmea\b|northern europe',
    re.IGNORECASE,
)
_LOC_SKIP = {'n/a', 'location', '', 'remote', 'na'}

def _is_us(job):
    loc = job.get('location', '').strip()
    if loc.lower() in _LOC_SKIP:
        return False
    if _US_RE.search(loc):
        return True       # explicitly US
    if _NON_US_RE.search(loc):
        return False      # explicitly non-US
    return True           # unknown → include so US cities are never silently dropped


def _is_doordash_engineering(job):
    # DoorDash uses 31x (310-319) and 34x (341-349) for Engineering departments
    return bool(re.match(r'^3[14][0-9] ', job['role'])) or 'engineering' in job['role'].lower()


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    stripe = greenhouse.fetch("stripe")
    jobs += [j for j in stripe if _is_us(j)]
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
