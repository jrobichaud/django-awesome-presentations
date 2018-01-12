from django.db import IntegrityError
from django.test import TestCase

from . import factories


class TestAwesomeModelFactory(TestCase):
    factory = factories.AwesomeModelFactory

    def test_create(self):
        instance = self.factory(name='foo')
        self.assertEqual('foo', instance.name)

    def test_unique(self):
        self.factory(name='foo')

        with self.assertRaisesMessage(IntegrityError, 'UNIQUE constraint failed: testing_migrations_awesomemodel.name'):
            self.factory(name='foo')
