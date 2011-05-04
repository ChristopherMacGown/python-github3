from github3.api import handler
from github3.api.core import attribute
from github3.api.core import base
from github3.api.core import request


class Issue(base.APIBase):
    """Class representation of the github3 api issues json."""

    title = attribute.Attribute("The title of the Issue.", class_id=True)
    assignee = attribute.Attribute("The user assigned this Issue.")
    body = attribute.Attribute("The body of the Issue.")
    closed_at = attribute.Attribute("The time this Issue was closed.")
    comments = attribute.Attribute("The count of comments on this Issue.")
    created_at = attribute.Attribute("The time this Issue was created.")
    html_url = attribute.Attribute("The non-API HTML URL of this Issue.")
    labels = attribute.Attribute("Any labels this Issue is tagged with.")
    milestone = attribute.MilestoneAttribute("Any milestones this Issue is tagged with")
    number = attribute.Attribute("The numeric ID of this Issue.")
    pull_request = attribute.PullRequestAttribute("The URLs for this pull req")
    state = attribute.Attribute("The state of the Issue: open or closed")
    updated_at = attribute.Attribute("The time this Issue was last updated")
    url = attribute.Attribute("The API URL of this Issue")
    user = attribute.UserAttribute("The user who created this Issue.")


class Issues(request.Request):
    """Wrapper around the HTTP verbs for an Issue or collection thereof."""
    __datatype__ = Issue


handler.register_api_handler("issues", Issues)
