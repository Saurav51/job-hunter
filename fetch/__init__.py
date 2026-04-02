from adapters import greenhouse, ashby


def fetch_all():
    jobs = []
    jobs += greenhouse.fetch("anthropic")
    jobs += ashby.fetch("perplexity")
    jobs += ashby.fetch("openai")
    jobs += ashby.fetch("ramp")
    return jobs
