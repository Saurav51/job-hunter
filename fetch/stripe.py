from adapters.ats import greenhouse

_NA_PREFIXES = ("US", "Canada", "Mexico")


def _is_na(job):
    return any(o.startswith(_NA_PREFIXES) for o in job.get("offices", []))


def fetch():
    return [j for j in greenhouse.fetch("stripe") if _is_na(j)]
