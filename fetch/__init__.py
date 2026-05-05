from fetch import (
    anthropic, stripe, doordash,
    openai, perplexity, ramp, snowflake,
    uber, google, netflix,
)


def fetch_all():
    jobs = []
    jobs += anthropic.fetch()
    jobs += stripe.fetch()
    jobs += doordash.fetch()
    jobs += perplexity.fetch()
    jobs += openai.fetch()
    jobs += ramp.fetch()
    jobs += snowflake.fetch()
    jobs += uber.fetch()
    jobs += google.fetch()
    jobs += netflix.fetch()
    return jobs
