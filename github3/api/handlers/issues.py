from github3.api import core
from github3.api import handler


class Issue(core.base.APIBase):
    assignee  = core.attribute.Attribute("The user assigned this Issue.")
    body  = core.attribute.Attribute("The body of the Issue.")
    closed_at  = core.attribute.Attribute("The time this Issue was closed.")
    comments  = core.attribute.Attribute("The count of comments on this Issue.")
    created_at  = core.attribute.Attribute("The time this Issue was created.")
    html_url  = core.attribute.Attribute("The non-API HTML URL of this Issue.")
    user  = core.attribute.Attribute("The user who created this Issue.")
    labels  = core.attribute.Attribute("Any labels this Issue is tagged with.")
    milestone  = core.attribute.Attribute(
                    "Any milestones this Issue is associated with")
    number  = core.attribute.Attribute("The numeric ID of this Issue.")
    updated_at  = core.attribute.Attribute("The time this Issue was last updated")
    state  = core.attribute.Attribute("The state of the Issue: open or closed")
    title = core.attribute.Attribute("The title of the Issue.", class_id=True)
    url  = core.attribute.Attribute("The API URL of this Issue")


class Issues(core.request.Request):
    __datatype__ = Issue

handler.register_api_handler("issues", Issues)
