import json

from github3 import request

from tests import utils


class FakeGithubAPIOpener(object):
    def __init__(self, *args):
        self.body = self.__returns__["body"]
        self.headers = self.__returns__["headers"]

    def read(self):
        return json.dumps(self.body)


class RequestTestCase(utils.TestHelper):
    def setUp(self):
        self.req = request.Request()
        self.rate_limit_limit = self.req.rate_limit_limit
        self.rate_limit_remaining = self.req.rate_limit_remaining

    def test_rate_limits_update_after_req(self):
        class FakeRawOpener(FakeGithubAPIOpener):
            __returns__ = {"headers": {
                                "X-RateLimit-Limit": 5000,
                                "X-RateLimit-Remaining": 4999,
                                },
                           "body": {}
                          }

        req = request.Request(opener=FakeRawOpener)
        self.assertEqual(self.rate_limit_limit, self.req.rate_limit_limit)
        self.assertEqual(5000, self.req.rate_limit_remaining)
        req.raw("https://fake_req.uest.url", ())
        self.assertEqual(self.rate_limit_limit, self.req.rate_limit_limit)
        self.assertNotEqual(FakeRawOpener().headers["X-RateLimit-Remaining"],
                            self.req.rate_limit_remaining)

    def test_raw_reqs(self):
        class FakeRawOpener(FakeGithubAPIOpener):
            __returns__ = {"headers": {
                                "X-RateLimit-Limit": 5000,
                                "X-RateLimit-Remaining": 4999,
                                },
                           "body": {}
                          }

        req = request.Request(opener=FakeRawOpener)
        self.assertEqual({}, req.raw("https://fake_req.uest.url", ()))
        self.assertEqual("{}", req.raw("https://fake_req.uest.url", (), 
                                       decode=False))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="HEAD"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="HEAD"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="PATCH"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="POST"))
        self.assertEqual({}, req.raw("https://fake_req.uest.url", (), 
                                     method="PUT"))
