import json

from github3 import conn

from tests import utils


class FakeGithubAPIOpener(object):
    def __init__(self, *args):
        self.body = self.__returns__["body"]
        self.headers = self.__returns__["headers"]

    def read(self):
        return json.dumps(self.body)


class RequestTestCase(utils.TestHelper):
    class FakeRawOpener(FakeGithubAPIOpener):
        __returns__ = {"headers": {
                            "X-RateLimit-Limit": 5000,
                            "X-RateLimit-Remaining": 4999,
                            },
                       "body": {}
                      }

    def setUp(self):
        self.req = conn.Connection(opener=self.FakeRawOpener)
        self.rate_limit_limit = self.req.rate_limit_limit
        self.rate_limit_remaining = self.req.rate_limit_remaining

    def test_rate_limits_update_after_req(self):
        fake_headers = self.FakeRawOpener().headers
        req = conn.Connection(opener=self.FakeRawOpener)
        self.assertEqual(self.rate_limit_limit, self.req.rate_limit_limit)
        self.assertEqual(5000, self.req.rate_limit_remaining)
        req.raw("https://fake_req.uest.url", ())
        self.assertEqual(self.rate_limit_limit, self.req.rate_limit_limit)
        self.assertNotEqual(fake_headers["X-RateLimit-Remaining"],
                            self.req.rate_limit_remaining)

    def test_raw_reqs(self):
        req = conn.Connection(opener=self.FakeRawOpener)
        self.assertEqual({}, req.raw("https://fake_req.uest.url", ()))
        self.assertEqual("{}", req.raw("https://fake_req.uest.url", (), 
                                       decode=False))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="DELETE"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="HEAD"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="PATCH"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="POST"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="PUT"))


    def test_get_request(self):
        class BadHeaderReq(FakeGithubAPIOpener):
            __returns__ = {"headers": {},
                           "body": {}}

        bad_header_req = conn.Connection(opener=BadHeaderReq)
                           
        self.assertRaises(conn.ConnectionException,
                          bad_header_req.get, "https://fake_req.uest.url")
        self.assertEqual({}, self.req.get("https://fake_req.uest.url"))

    def test_post_request(self):
        self.assertEqual({}, self.req.post("https://fake_req.uest.url", (1,2,)))

    def test_http_requests_with_method(self):
        url = "http://fake_req.uest.url"

        for expectation in ["DELETE", "GET", "HEAD", "PATCH", "POST", "PUT"]:
            req = conn.HTTPMethodRequest(url=url, method=expectation)
            self.assertEqual(expectation, req.get_method())

        req = conn.HTTPMethodRequest(url=url, method=None, data=(1,2,3,))
        self.assertEqual("POST", req.get_method())
