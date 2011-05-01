from github3.api import core
from github3.api import handler


class Issue(core.base.APIBase):
    title = core.attribute.Attribute("The title of the Issue.", repr=True)


class Issues(core.request.Request):
    __datatype__ = Issue

handler.register_api_handler("issues", Issues)
