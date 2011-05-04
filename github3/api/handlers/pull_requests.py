from github3.api import handler
from github3.api.core import attribute
from github3.api.core import base
from github3.api.core import request


class PullRequest(base.APIBase):
    """Class representation of the github3 api pull_requests json."""

    html_url = attribute.Attribute("The non-API HTML URL of the pull request", 
                                   class_id=True)
    diff_url = attribute.Attribute("The URL of the diff")
    patch_url = attribute.Attribute("The URL of the patch")

    def __nonzero__(self):
        if self.diff_url and self.html_url and self.patch_url:
            return True
        return False


class PullRequests(request.NullOpRequest):
    """Pull Request is a NullOpRequest.

    Since the github v3 API doesn't have pull_requests as first class objects
    it would still be nice to get an object out of the issues JSON. So this
    is registered as a handler so we can use dynamically load it.

    """

    __datatype__ = PullRequest


handler.register_api_handler("pull_requests", PullRequests)
