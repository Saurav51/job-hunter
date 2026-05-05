from adapters.companies import uber as _uber


def fetch():
    return _uber.fetch("uber")
