import json
import urllib
import urllib2


class HTTPMethodRequest(urllib2.Request):
    # todo(chris): Move me
    def __init__(self, method, *args, **kwargs):
        self._method = method
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        if self._method:
            return self._method
        elif self.has_data():
            return "POST"


class RequestException(Exception):
    pass


class Request(object):
    def __init__(self, opener=None):
        self.rate_limit_limit = 5000 # Assume we're normal.
        self.rate_limit_remaining = 5000 # Assume we have all our reqs.
        self.opener = opener or urllib2.urlopen # Use a test opener or urllib2
        self.headers = {"Accept": "text/json",
                        "Accept-Encoding": "application/json",
                        "User-Agent": "python-github3",
                       }

    def post(self, url, data, params={}):
        return self.raw(url, data, method="POST")

    def get(self, url, params={}):
        return self.raw(url, (), params=params)

    def raw(self, url, data, method="GET", decode=True, params={}):
        """Make a raw request to the URL.
        """

        params = urllib.urlencode(params)
        url = str.join("?", (url, params))

        req = HTTPMethodRequest(url=url, method=method)
        req.headers = self.headers
        res = self.opener(req)

        self.rate_limit_limit = int(res.headers["X-RateLimit-Limit"])
        self.rate_limit_remaining = int(res.headers["X-RateLimit-Remaining"])

        res = res.read()
        if decode:
            res = json.loads(res)
        return res
