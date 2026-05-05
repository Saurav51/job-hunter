from adapters.companies import google as _google


def fetch():
    return _google.fetch("google")
