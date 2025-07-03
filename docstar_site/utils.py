import re


class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        return context


def get_site_url():
    from django.contrib.sites.models import Site

    scheme = "https"
    domain = Site.objects.get_current().domain
    return "{}://{}".format(scheme, domain)


def validate_url(url: str) -> str:
    """
    Извлекает username из URL Telegram
    """
    if not url:
        return ''

    if "https://t.me/+" in url:
        return url

    patterns = [
        r'https?://t\.me/([a-zA-Z0-9_]+)',  # https://t.me/username
        r't\.me/([a-zA-Z0-9_]+)',  # t.me/username
        r'@?([a-zA-Z0-9_]+)'  # @username или username
    ]

    for pattern in patterns:
        match = re.fullmatch(pattern, url.strip())
        if match:
            return match.group(1)

    return url.strip()
