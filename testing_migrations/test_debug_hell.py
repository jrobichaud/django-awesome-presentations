from unittest import skipIf

import os
from django.db import IntegrityError
from django.test import TransactionTestCase
from django_migration_testcase import MigrationTest

EXAMPLE_CORRUPTION = bool(os.environ.get('EXAMPLE_CORRUPTION', False))


class Test0002AwesomeModelUniqueName(MigrationTest):
    app_name = 'testing_migrations'
    before = '0001_initial'
    after = '0002_awesome_model_unique_name'

    @skipIf(not EXAMPLE_CORRUPTION, "This test corrupts the migration state of the tests.")
    def test_migration(self):
        awesome_model_model = self.get_model_before('testing_migrations.AwesomeModel')
        awesome_model_model.objects.create(name="foo")
        awesome_model_model.objects.create(name="foo")
        with self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: testing_migrations_awesomemodel.name"):
            self.run_migration()


class Test9999AnotherTransactionTest(TransactionTestCase):
    """
    This test use an `TransactionTestCase` for this demo since they are run at the same time as `MigrationTestCase`.
    This test will fail if the other test is run.
    """
    def test_this_factory_is_supposed_to_work(self):
        from .factories import KittenNameFactory
        kitten = KittenNameFactory(name="foo")
        self.assertTrue(kitten.name, "foo")
