from github3.api import handler
from github3.api.core import attribute

from tests import utils


class AttributeTestCase(utils.TestHelper):
    def setUp(self):
        self.test_data = {'a': 1, 'b': 2, 'c': 3}

    def test_instantiate_datatype(self):
        builder = attribute.instantiate_datatype

        self.assertEqual(None, builder(object, None))
        self.assertEqual(self.test_data, builder(dict, self.test_data))

        def raising_caller(**kwargs):
            raise TypeError

        self.assertRaises(TypeError, builder, raising_caller, self.test_data)

    def test_instantiate_datatype_collection(self):
        builder = attribute.instantiate_datatype_collection
        self.assertEqual([], builder(object, []))
        self.assertEqual([self.test_data], builder(dict, [self.test_data]))

        def raising_caller(**kwargs):
            raise TypeError

        self.assertRaises(TypeError, builder, raising_caller, [self.test_data])

    def test_creating_an_arbitrary_attribute(self):
        docstring = """This is some attribute."""
        docstring2 = """This is some other attribute."""

        attr = attribute.Attribute(docstring)
        attr2 = attribute.Attribute(docstring2, class_id=True)

        self.assertEqual(docstring, attr.docstring)
        self.assertFalse(attr.class_identifier)

        self.assertEqual(docstring2, attr2.docstring)
        self.assertTrue(attr2.class_identifier)

    def test_attribute_to_python(self):
        self.assertEqual(None, attribute.Attribute("").to_python(None))


class HandlerAttributeTestCase(utils.TestHelper):
    def setUp(self):
        class MockObject(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        class RaisingMockObject(object):
            def __init__(self, **kwargs):
                raise TypeError

        class MockedHandler(object):
            __datatype__ = MockObject

        class RaisingMockHandler(object):
            __datatype__ = RaisingMockObject

        self.mock_object = MockObject
        handler.register_api_handler("mock", MockedHandler)
        handler.register_api_handler("raising", RaisingMockHandler)

    def test_create_handler_attribute(self):
        class HandlerAttribute(attribute.HandlerAttribute):
            __handler__ = "mock"

        docstring = """This is some attribute."""
        docstring2 = """This is some other attribute."""

        attr = HandlerAttribute(docstring)
        attr2 = HandlerAttribute(docstring2, class_id=True)

        self.assertEqual(docstring, attr.docstring)
        self.assertFalse(attr.class_identifier)

        self.assertEqual(docstring2, attr2.docstring)
        self.assertTrue(attr2.class_identifier)

    def test_handler_attribute_to_python(self):
        class HandlerAttribute(attribute.HandlerAttribute):
            __handler__ = "mock"

        test_data = {'a': 1, 'b': 2, 'c': 3}
        h = HandlerAttribute("Mock")

        self.assertTrue(isinstance(h.to_python(test_data), self.mock_object))
        self.assertEqual(test_data["a"], h.to_python(test_data).a)
        self.assertEqual(test_data["b"], h.to_python(test_data).b)
        self.assertEqual(test_data["c"], h.to_python(test_data).c)

    def test_handler_attribute_that_raises_to_python(self):
        class HandlerAttribute(attribute.HandlerAttribute):
            __handler__ = "raising"

        test_data = {'a': 1, 'b': 2, 'c': 3}
        h = HandlerAttribute("Mock")
        self.assertRaises(TypeError, h.to_python, test_data)
