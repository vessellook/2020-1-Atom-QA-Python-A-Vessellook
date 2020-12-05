from urllib.parse import urlparse, urlunparse


def change_netloc(url, netloc):
    parsed = urlparse(url)
    changed = parsed._replace(netloc=netloc)  # noqa:
    return urlunparse(changed)
