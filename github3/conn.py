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


class ConnectionException(Exception):
    pass


class Connection(object):
    def __init__(self, username=None, auth_token=None, opener=None):
        self.rate_limit_limit = 5000 # Assume we're normal.
        self.rate_limit_remaining = 5000 # Assume we have all our reqs.
        self.opener = opener or urllib2.urlopen # Use a test opener or urllib2
        self.headers = {"Accept": "text/json",
                        "Accept-Encoding": "application/json",
                        "User-Agent": "python-github3",
                       }
        self.auth()

    def auth(self):
        pass

    def post(self, url, data, params={}):
        return self.raw(url, data, method="POST")

    def get(self, url, params={}):
        return self.raw(url, (), params=params)

    def raw(self, url, data, method="GET", decode=True, params={}):
        """Make a raw request to the URL."""

        params = urllib.urlencode(params)
        url = str.join("?", (url, params))

        req = HTTPMethodRequest(url=url, method=method)
        req.headers = self.headers
        print self.opener
        res = self.opener(req)

        try:
            self.rate_limit_limit = int(res.headers["X-RateLimit-Limit"])
            self.rate_limit_remaining = int(res.headers["X-RateLimit-Remaining"])
        except KeyError:
            raise ConnectionException(
                "No rate-limit headers, are we even talking to github???")

        res = res.read()
        if decode:
            res = json.loads(res)
        return res
