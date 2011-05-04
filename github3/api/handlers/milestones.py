from github3.api import handler
from github3.api.core import attribute
from github3.api.core import base
from github3.api.core import request


class Milestone(base.APIBase):
    """Class representation of the github3 api issues json."""

    title = attribute.Attribute("The title of the Milestone.", class_id=True)
    closed_issues = attribute.Attribute("The count of closed issues associated with this milestone.")
    created_at  = attribute.Attribute("The time this Milestone was created.")
    creator = attribute.UserAttribute("The user who created this Milestone.")
    due_on = attribute.Attribute("The time this Milestone is due.")
    number  = attribute.Attribute("The numeric ID of this Milestone.")
    open_issues = attribute.Attribute("The count of open issues associated with this milestone.")
    state  = attribute.Attribute("The state of the Milestone: open or closed")
    url  = attribute.Attribute("The API URL of this Milestone")


class Milestones(request.Request):
    """Wrapper around the HTTP verbs for an Milestone or collection thereof."""
    __datatype__ = Milestone


handler.register_api_handler("milestones", Milestones)
