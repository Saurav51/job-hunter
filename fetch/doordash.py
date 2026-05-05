import re

from adapters.ats import greenhouse


def _is_engineering(job):
    # DoorDash uses 31x (310-319) and 34x (341-349) for Engineering departments
    return bool(re.match(r'^3[14][0-9] ', job['role'])) or 'engineering' in job['role'].lower()


def fetch():
    return [j for j in greenhouse.fetch("doordashusa", name="doordash") if _is_engineering(j)]
