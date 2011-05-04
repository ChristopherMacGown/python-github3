from github3.api import handler
from github3.api.core import attribute
from github3.api.core import base
from github3.api.core import request


class User(base.APIBase):
    """Class representation of the github3 api users json."""

    login = attribute.Attribute("The User's login", class_id=True)
    blog = attribute.Attribute("The URL of the User's blog.")
    company = attribute.Attribute("The name of the User's company.")
    created_at  = attribute.Attribute("The time this User joined github.")
    email = attribute.Attribute("The public email address of the User.")
    followers = attribute.Attribute("The count of the User's followers.")
    following = attribute.Attribute("The count of people this User follows.")
    gravatar_url = attribute.Attribute("The URL of the User's gravatar.")
    html_url  = attribute.Attribute("The non-API HTML URL of this Issue.")
    location = attribute.Attribute("The User's location.")
    name = attribute.Attribute("The User's public name if any.")
    public_gists = attribute.Attribute("The count of the User's public gists.")
    public_repos = attribute.Attribute("The count of the User's public repos.")
    url  = attribute.Attribute("The API URL of this Issue")


class Users(request.Request):
    """Wrapper around the HTTP verbs for a User or collection thereof."""
    __datatype__ = User


handler.register_api_handler("users", Users)
