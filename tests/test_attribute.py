import pytest
from productsimporter.parser.attribute import Attribute


class TestAttributes:
    def test_attributes_multilingual_true(self):
        attribute = Attribute('key', 'key2', '1', '0', '0')
        assert attribute.is_multilingual() is True

    def test_attributes_multilingual_false(self):
        attribute = Attribute('key', 'key2', '0', '0', '0')
        assert attribute.is_multilingual() is False
