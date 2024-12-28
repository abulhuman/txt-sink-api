"""Middleware to add dynamic hosts to ALLOWED_HOSTS from our alb subnet"""

from django.conf import settings

TXT_SINK_APP_SUBNET_A_CIDR_PREFIX = "10.0.10."
TXT_SINK_APP_SUBNET_B_CIDR_PREFIX = "10.0.11."


class ALBSubnetDynamicAllowedHostsMiddleware:
    """ Middleware to add dynamic hosts to ALLOWED_HOSTS from our alb subnet """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        for key in dir(settings):
            value = getattr(settings, key)
            if key.isupper():
                print("[DEBUG][__call__]: " + key + " = " + value)

        host = request.get_host().split(":")[0]
        if (
            host.startswith(TXT_SINK_APP_SUBNET_A_CIDR_PREFIX) or host.startswith(TXT_SINK_APP_SUBNET_B_CIDR_PREFIX)
        ) and host not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host)
        return self.get_response(request)
