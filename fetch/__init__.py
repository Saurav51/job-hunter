from adapters.ats import greenhouse, ashby
from adapters.companies import uber, google, netflix


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    jobs += ashby.fetch("perplexity")
    jobs += ashby.fetch("openai")
    jobs += ashby.fetch("ramp")
    jobs += uber.fetch("uber")
    jobs += google.fetch("google")
    jobs += netflix.fetch("netflix")
    return jobs
