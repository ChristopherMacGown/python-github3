from github3.api.core import request

GITHUB_API_HANDLERS = {}

def get_handler(key):
    return GITHUB_API_HANDLERS[key]


def register_api_handler(token, handler):
    """Register api handler with handlers dictionary."""
    GITHUB_API_HANDLERS[token] = handler


def registered_api_handlers():
    """Return the github api handlers."""
    return (name for name, handler
                 in GITHUB_API_HANDLERS.items()
                 if not request.NullOpRequest in handler.__bases__)
