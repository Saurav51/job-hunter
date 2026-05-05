from adapters.ats import ashby

_DEPARTMENTS = {'Engineering', 'Data Analytics and AI'}


def fetch():
    return [j for j in ashby.fetch("snowflake") if j['role'] in _DEPARTMENTS]
