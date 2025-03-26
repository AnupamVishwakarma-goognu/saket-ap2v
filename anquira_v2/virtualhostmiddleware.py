virtual_hosts = {
    "anquira.ap2v.com": "anquira_v2.urls",
    "beta-anquira.ap2v.com": "anquira_v2.urls",
    "127.0.0.1:8000": "anquira_v2.urls",
    "dj3.ap2v.com": "anquira_v2.ap2v_urls",
    "127.0.0.1:8001": "anquira_v2.ap2v_urls",
    "www.ap2v.com": "anquira_v2.ap2v_urls"
}


class VirtualHostMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # let's configure the root urlconf
        host = request.get_host()
        request.urlconf = virtual_hosts.get(host)
        # order matters!
        response = self.get_response(request)
        return response
