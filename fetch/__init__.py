from adapters import greenhouse, ashby, uber


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    jobs += ashby.fetch("perplexity")
    jobs += ashby.fetch("openai")
    jobs += ashby.fetch("ramp")
    jobs += uber.fetch("uber")
    return jobs
