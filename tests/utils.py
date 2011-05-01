import json
import os
import unittest

def testdata(filename):
    return os.path.join(os.path.dirname(__file__), "data", filename)

def load(filename):
    with open(filename) as fp:
        return json.JSONDecoder().decode(fp.read())

class was_called(object):
    def __init__(self, method):
        self.was_called = False
        self.method = method
    
    def __call__(self, *args, **kwargs):
        try:
            self.method(*args, **kwargs)
        finally:
            self.was_called = True

    def __eq__(self):
        return self.was_called

class TestHelper(unittest.TestCase):
    def assertCalled(self, bound_method, caller, *args, **kwargs):
        bound_method = was_called(bound_method)
        caller(*args, **kwargs)
        self.assertTrue(bound_method)

    def assertNothingRaised(self, caller, *args, **kwargs):
        raised=None
        try:
            caller(*args, **kwargs)
        except Exception:
            raised=True

        self.assertFalse(raised)
