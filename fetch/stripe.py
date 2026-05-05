import re

from adapters.ats import greenhouse

_NA_RE = re.compile(
    r'\bus\b|\busa\b|u\.s\.|united states|north america'
    r'|us.?remote|remote.?us|remote in the us'
    r'|canada|toronto|vancouver|montreal'
    r'|mexico|mexico city'
    r'|\bsf\b|\bsfo\b|san francisco|south san francisco'
    r'|\bnyc\b|\bny\b|new york|\bsea\b|seattle'
    r'|\bchi\b|chicago|atlanta|\bdc\b|washington'
    r'|boston|austin|los angeles|privy',
    re.IGNORECASE,
)
_NA_SKIP = {'n/a', 'location', '', 'remote', 'na'}


def _is_na(job):
    loc = job.get('location', '').strip()
    return loc.lower() not in _NA_SKIP and bool(_NA_RE.search(loc))


def fetch():
    return [j for j in greenhouse.fetch("stripe") if _is_na(j)]
