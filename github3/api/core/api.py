GITHUB_API_HANDLERS = {}

def register_api_handler(token, handler):
    GITHUB_API_HANDLERS[token] = handler


def registered_api_handlers():
    return GITHUB_API_HANDLERS
