"""Middleware to add dynamic hosts to ALLOWED_HOSTS from our alb subnet"""

from django.conf import settings
from django.core.exceptions import DisallowedHost

TXT_SINK_APP_SUBNET_A_CIDR_PREFIX = "10.0.10."
TXT_SINK_APP_SUBNET_B_CIDR_PREFIX = "10.0.11."


class ALBSubnetDynamicAllowedHostsMiddleware:
    """ Middleware to add dynamic hosts to ALLOWED_HOSTS from our alb subnet """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":")[0]
        if not host.startswith(TXT_SINK_APP_SUBNET_A_CIDR_PREFIX
                               ) or not host.startswith(TXT_SINK_APP_SUBNET_B_CIDR_PREFIX):
            raise DisallowedHost("Host not allowed")
        if host and host not in settings.ALLOWED_HOSTS:
            settings.ALLOWED_HOSTS.append(host)
        return self.get_response(request)
