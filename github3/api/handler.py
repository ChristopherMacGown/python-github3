GITHUB_API_HANDLERS = {}


def register_api_handler(token, handler):
    """Register api handler with handlers dictionary."""
    GITHUB_API_HANDLERS[token] = handler


def registered_api_handlers():
    """Return the github api handlers."""
    return GITHUB_API_HANDLERS
