import json
import UserDict
from urllib2 import HTTPError

from github3 import request


def _resource_factory(client, data):
  """Helper function for mapping responses into Resources."""
  return Resource(client, data.get('url'), data)


class Client(request.Request):
  BASE_URL = "https://api.github.com/user"

  def list_repo(self, **kw):
    """Return a PaginatedResourceList of all of the authenticated user's repos"""
    url = "%s/repos" % (self.BASE_URL)
    resp = self.get(url, **kw)
    return PaginatedResourceList.FromResponse(self, resp)

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

  def commits(self, **kw):
    """Return a PaginatedResourceList of commits for a repo"""
    url = '%s/%s/%s/commits' % (
            self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def pull_requests(self, id = None, **kw):
    """Return a PaginatedResourceList of pull requests for a repo"""
    if id:
        url = '%s/%s/%s/pulls/%s' % (
            self.BASE_URL, self.user, self.repo, id)
    else:
         url = '%s/%s/%s/pulls' % (
            self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def forks(self, **kw):
    """Return a Paginated ResourceList of forks for a repo"""
    url = '%s/%s/%s/forks' % (
            self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

  def branches(self, **kw):
    """Return a ResourceList of Branches for a repo"""
    url = '%s/%s/%s/branches' % (
            self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)

  def trees(self, sha, **kw):
    """Return a ResourceList of Trees for a repo"""
    url = '%s/%s/%s/git/trees/%s' % (
            self.BASE_URL, self.user, self.repo, sha)
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)

  def refs(self, ref, **kw):
    """Return a ResourceList of Refs for a repo"""
    url = '%s/%s/%s/git/refs/%s' % (
            self.BASE_URL, self.user, self.repo, ref)
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)


class User(object):
  BASE_URL = "https://api.github.com/user"

  def __init__(self, client):
    self.client = client

  def user_info(self, **kw):
    """Returns a ResourceList of a user's information"""
    url = self.BASE_URL
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)

  def user_emails(self, **kw):
    """Returns a SimpleList of a user's email addresses. Email addresses don't
    return in a usual format, thus the need for a simple list."""
    url = "%s/emails" %self.BASE_URL
    resp = self.client.get(url, **kw)
    return SimpleList.FromResponse(self.client, resp)

  def user_issues(self, **kw):
    """Returns a PaginatedResourceList of the authenticated user's issues"""
    url = "https://api.github.com/issues"
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)

class ResourceList(object):
  def __init__(self, client, url, datalist=None):
    self.client = client
    self.url = url
    self.datalist = datalist

  @classmethod
  def FromResponse(cls, client, response):
      j = json.load(response)
      if type(j) is list:
        return cls(client,
               response.geturl(),
               [_resource_factory(client, x) for x in j])
      else:
        return cls(client,
               response.geturl(),
               _resource_factory(client, j))


  def append(self, **kw):
    rv = self.client.post(self.url, **kw)
    return json.loads(rv.read())

  def __iter__(self):
    return iter(self.datalist)


class SimpleList(ResourceList):

    @classmethod
    def FromResponse(cls, client, response):
      j = json.load(response)
      return cls(client, response.geturl(), j)



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
    page = 2
    while True:
      try:
        yield self.datalist[i]
      except IndexError:
        if json.load(self.client.get(self.url.split("?")[0], page=page)):
          response = self.client.get(self.url.split("?")[0], page=page)
          self.datalist.extend(
              [_resource_factory(self.client, x) for x in json.load(response)])
          page += 1
          yield self.datalist[i]
        else:
          raise StopIteration
      except HTTPError:
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
