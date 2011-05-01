class Attribute(object):
    """ Base Github Attribute """
    def __init__(self, doc_string, repr=False):
        self.doc_string = doc_string
        self.repr = repr

    def to_python(self, value):
        return value

    from_python = to_python
