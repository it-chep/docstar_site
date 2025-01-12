class DataMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        return context


def get_site_url():
    from django.contrib.sites.models import Site

    scheme = "https"
    domain = Site.objects.get_current().domain
    return "{}://{}".format(scheme, domain)
