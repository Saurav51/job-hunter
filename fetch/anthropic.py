from adapters.ats import greenhouse


def fetch():
    return greenhouse.fetch("anthropic")
