import json
import UserDict

from github3 import request


def _resource_factory(client, data):
  """Helper function for mapping responses into Resources."""
  return Resource(client, data.get('url'), data)


class Client(request.Request):
  def repo(self, user, repo_):
    return Repo(client=self, user=user, repo=repo_)


class Repo(object):
  BASE_URL = "https://api.github.com/repos"

  def __init__(self, client, user, repo):
    self.client = client
    self.user = user
    self.repo = repo

  def issues(self, **kw):
    """Return a PaginatedResourceList of issues."""
    url = '%s/%s/%s/issues' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def issue(self, id_):
    """Return a Resource of an issue."""
    url = '%s/%s/%s/issues/%s' % (self.BASE_URL, self.user, self.repo, id_)
    resp = self.client.get(url)
    return Resource(self.client, url, json.loads(resp.read()))

  def milestones(self, **kw):
    """Return a PaginatedResourceList of milestones."""
    url = '%s/%s/%s/milestones' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def labels(self, **kw):
    """Return a PaginatedResourceList of labels."""
    url = '%s/%s/%s/labels' % (self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def comments(self, issue, **kw):
    """Return a PaginatedResourceList of comments for an issue."""
    url = '%s/%s/%s/issues/%s/comments' % (
        self.BASE_URL, self.user, self.repo, issue)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)


class ResourceList(object):
  def __init__(self, client, url, datalist=None):
    self.client = client
    self.url = url
    self.datalist = datalist

  @classmethod
  def FromResponse(cls, client, response):
    return cls(client,
               response.geturl(),
               [self._resource_factory(x) for x in json.load(response)])

  def append(self, **kw):
    rv = self.client.post(self.url, **kw)
    return json.loads(rv.read())

  def __iter__(self):
    return iter(self.datalist)


class PaginatedResourceList(ResourceList):
  def __init__(self, client, url, datalist=None, next_page=None):
    super(PaginatedResourceList, self).__init__(client, url, datalist)
    self.next_page = next_page

  @classmethod
  def FromResponse(cls, client, response):
    url = response.geturl()
    next_page = response.info().get('X-Next')
    return cls(client,
               response.geturl(),
               [_resource_factory(client, x) for x in json.load(response)],
               next_page=next_page)

  def __iter__(self):
    i = 0
    while True:
      try:
        yield self.datalist[i]
      except IndexError:
        if self.next_page:
          response = self.client.get(self.next_page)
          self.next_page = response.info().get('X-Next')
          self.datalist.extend(
              [_resource_factory(self.client, x) for x in json.load(response)])
          yield self.datalist[i]
        else:
          raise StopIteration

      i += 1


class Resource(dict):
  def __init__(self, client, url, data=None):
    self.client = client
    self.url = url
    dict.__init__(self, **data)

  def __setitem__(self, key, val):
    raise Exception('cannot modify dict')

  def __delitem__(self, key):
    raise Exception('cannot modify dict')

  def update(self, kw):
    rv = self.client.patch(self.url, **kw)
    dict.update(self, kw)
    return json.loads(rv.read())

  def delete(self):
    self.client.delete(self.url)
