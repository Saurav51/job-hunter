from adapters.companies import netflix as _netflix


def fetch():
    return _netflix.fetch("netflix")
