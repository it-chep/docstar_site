import re


class DataMixin:
    @staticmethod
    def get_user_context(**kwargs):
        context = kwargs
        return context


def get_site_url():
    from django.contrib.sites.models import Site

    scheme = "https"
    domain = Site.objects.get_current().domain
    return "{}://{}".format(scheme, domain)


def validate_tg_channel_url(url: str) -> str:
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

def validate_inst_url(url: str) -> str:
    """
    Извлекает username из URL INSTAGRAM
    """
    if not url:
        return ''

    # Удаляем параметры запроса (все что после ?)
    base_url = url.split('?')[0].strip()

    patterns = [
        r'https?://(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?',  # https://instagram.com/username/
        r'(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)/?',  # instagram.com/username
        r'@?([a-zA-Z0-9_.]+)',  # @username или username
        r'([a-zA-Z0-9_.]+)'  # username как последний fallback
    ]

    for pattern in patterns:
        match = re.fullmatch(pattern, base_url)
        if match:
            username = match.group(1)
            # Удаляем возможные слеши в конце
            return username.rstrip('/')

    return base_url
