from django.test import TestCase

from . import factories


class TestAwesomeModelFactory(TestCase):
    factory = factories.AwesomeModelFactory

    def test_create(self):
        instance = self.factory(name='foo')
        self.assertEqual('foo', instance.name)
