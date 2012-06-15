import json
from urllib2 import HTTPError
import base64

from github3 import request
from github3.link_parser import parse_link_value


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

  def list_orgs(self, **kw):
    """Return user's organizations"""
    url = "%s/orgs" % self.BASE_URL
    resp = self.get(url, **kw)
    return PaginatedResourceList.FromResponse(self, resp)


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

  def commit(self, sha, **kw):
    """Return a single commit in a repo."""
    url = '%s/%s/%s/commits/%s' % (
            self.BASE_URL, self.user, self.repo, sha)
    resp = self.client.get(url, **kw)
    return Resource(self.client, url, json.loads(resp.read()))

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

  def refs(self, ref=None, **kw):
    """Return a ResourceList of Refs for a repo"""
    url = '%s/%s/%s/git/refs' % (
            self.BASE_URL, self.user, self.repo)
    if ref:
        url += "/%s" % ref
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)

  def blobs(self, sha, **kw):
    """Return a ResourceList for a single Blob"""
    url = '%s/%s/%s/git/blobs/%s' % (
            self.BASE_URL, self.user, self.repo, sha)
    resp = self.client.get(url, **kw)

    blob = ResourceList.FromResponse(self.client, resp)

    if blob["encoding"] == "base64":
        blob["content"] = base64.b64decode(blob["content"])

    return blob

  def collaborators(self, **kw):
    """Return a ResourceList of Collaborators for a repo"""
    url = '%s/%s/%s/collaborators' % (
            self.BASE_URL, self.user, self.repo)
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)


class User(object):
  BASE_USER_URL = "https://api.github.com/user"
  BASE_USERS_URL = "https://api.github.com/users"

  def __init__(self, client):
    self.client = client

  def user_info(self, login=None, **kw):
    """Returns a ResourceList of a user's information"""
    if login is None:
      url = self.BASE_USER_URL
    else:
      url = '%s/%s' % (self.BASE_USERS_URL, login)
    resp = self.client.get(url, **kw)
    return ResourceList.FromResponse(self.client, resp)

  def user_emails(self, **kw):
    """Returns a SimpleList of a user's email addresses. Email addresses don't
    return in a usual format, thus the need for a simple list."""
    url = "%s/emails" %self.BASE_USER_URL
    resp = self.client.get(url, **kw)
    return SimpleList.FromResponse(self.client, resp)

  def user_issues(self, **kw):
    """Returns a PaginatedResourceList of the authenticated user's issues"""
    url = "https://api.github.com/issues"
    resp = self.client.get(url, **kw)
    return PaginatedResourceList.FromResponse(self.client, resp)


class Organization(object):
  BASE_URL = "https://api.github.com/orgs"

  def __init__(self, client, org):
    self.client = client
    self.org = org

  def repos(self, **kw):
    """List repositories in a given organization"""
    url = "%s/%s/repos" % (self.BASE_URL, self.org)
    resp = self.client.get(url, **kw)
    return SimpleList.FromResponse(self.client, resp)


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
        return Resource(client, response.geturl(), j)


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

  @staticmethod
  def get_next_link(response):
    """Extract the link to the next page from the 'Link' header.
    """
    next_links = [link[0] for link
                  in parse_link_value(response.info().get('Link')).items()
                  if link[1]['rel'] == 'next']
    if next_links:
        return next_links[0]
    return None

  @classmethod
  def FromResponse(cls, client, response):
    next_page = PaginatedResourceList.get_next_link(response)
    j = json.load(response)
    if type(j) is list:
      return cls(client,
                 response.geturl(),
                 [_resource_factory(client, x) for x in j],
                 next_page=next_page)
    else:
      return Resource(client, response.geturl(), j)

  def __iter__(self):
    i = 0
    page = 2
    while True:
      try:
        yield self.datalist[i]
      except IndexError:
        if not self.next_page:
          raise StopIteration
        response = self.client.get(self.next_page)
        resources = json.load(response)
        if resources:
          self.next_page = PaginatedResourceList.get_next_link(response)
          self.datalist.extend(
              [_resource_factory(self.client, x) for x in resources])
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

  def update(self, kw):
    rv = self.client.patch(self.url, **kw)
    dict.update(self, kw)
    return json.loads(rv.read())

  def delete(self):
    self.client.delete(self.url)

  @classmethod
  def create(cls, repo, resource_type, data):
    """Create a resource.

    `resource_type` takes values such as 'issues', or 'git/commits'
    """
    url = '%s/%s/%s/%s' % (Repo.BASE_URL, repo.user, repo.repo, resource_type)
    resp = repo.client.post(url, **data)

    return json.load(resp)
