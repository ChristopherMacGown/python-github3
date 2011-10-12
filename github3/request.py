import base64
import json
import urllib
import urllib2


class Request(object):
  def __init__(self, username=None, password=None, oauth_token=None):
    self._username = username
    self._password = password
    self._oauth_token = oauth_token
    self._opener = urllib2.build_opener()

  def _authenticate(self, req):
    if self._oauth_token:
      req.add_header('Authorization', 'token %s' % self._oauth_token)
    elif self._username is not None and self._password is not None:
      b64_userpass = base64.b64encode(
          '%s:%s' % (self._username, self._password))
      b64_userpass = b64_userpass.replace('\n', '')
      req.add_header('Authorization', 'Basic %s' % b64_userpass)
    return req

  # TODO(termie): There is probably a simple way to refactor this all
  #               but it doesn't seem worth the effort yet.
  def head(self, url, **kw):
    url = '%s?%s' % (url, urllib.urlencode(kw))
    req = HTTPMethodRequest('HEAD', url)
    req = self._authenticate(req)
    return self._opener.open(req)

  def get(self, url, **kw):
    sha = kw.pop("sha", "")
    if sha:
      url += "/%s" % sha
    url = '%s?%s' % (url, urllib.urlencode(kw))
    req = HTTPMethodRequest('GET', url)
    req = self._authenticate(req)
    return self._opener.open(req)

  def post(self, url, **kw):
    req = HTTPMethodRequest('POST', url, json.dumps(kw))
    req = self._authenticate(req)
    return self._opener.open(req)

  def patch(self, url, **kw):
    req = HTTPMethodRequest('PATCH', url, json.dumps(kw))
    req = self._authenticate(req)
    return self._opener.open(req)

  def put(self, url, **kw):
    req = HTTPMethodRequest('PATCH', url, json.dumps(kw))
    req = self._authenticate(req)
    return self._opener.open(req)

  def delete(self, url, **kw):
    url = '%s?%s' % (url, urllib.urlencode(kw))
    req = HTTPMethodRequest('DELETE', url)
    req = self._authenticate(req)
    return self._opener.open(req)


class HTTPMethodRequest(urllib2.Request):
  def __init__(self, method, *args, **kw):
    self._method = method
    urllib2.Request.__init__(self, *args, **kw)

  def get_method(self):
    return self._method
