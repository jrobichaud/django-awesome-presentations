import factory
from django.db import IntegrityError
from django_migration_testcase import MigrationTest
from django_migration_testcase.base import idempotent_transaction


class Test0002AwesomeModelUniqueName(MigrationTest):
    app_name = 'testing_migrations'
    before = '0001_initial'
    after = '0002_awesome_model_unique_name'

    def setUp(self):
        super().setUp()

        class AwesomeModelFactory(factory.DjangoModelFactory):
            name = factory.Faker('pystr')

            class Meta:
                model = self.get_model_before('testing_migrations.AwesomeModel')

        self.awesome_model_factory = AwesomeModelFactory

    @idempotent_transaction
    def test_migration(self):
        self.awesome_model_factory(name="foo")
        self.awesome_model_factory(name="foo")
        with self.assertRaisesMessage(IntegrityError, "UNIQUE constraint failed: testing_migrations_awesomemodel.name"):
            self.run_migration()


