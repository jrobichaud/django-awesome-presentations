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


class Test0005MigrateToKittenName(MigrationTest):
    app_name = 'testing_migrations'
    before = '0004_kittenname'
    after = '0007_remove_kitten_name'

    def setUp(self):
        super().setUp()

        # It is fine to shamelessly copy and paste factories in order to simplify testing
        # You have to copy and paste to avoid potential code paradoxes
        class KittenFactory(factory.DjangoModelFactory):
            name = factory.Faker('pystr')

            class Meta:
                model = self.get_model_before('testing_migrations.Kitten')

        self.kitten_factory = KittenFactory

    def test_name_is_properly_transferred_through_migrations(self):
        expected_kitten_name = 'Soft Kitty'
        kitten = self.kitten_factory(name=expected_kitten_name)

        with self.subTest("Forward migrations work"):
            self.run_migration()

            kitten_model = self.get_model_after('testing_migrations.Kitten')

            updated_kitten = kitten_model.objects.get(pk=kitten.pk)

            self.assertFalse(hasattr(updated_kitten, 'name'), "Kitten model instance no longer have its name.")

            kitten_name_model_after = self.get_model_after('testing_migrations.KittenName')
            kitten_name_query = kitten_name_model_after.objects.filter(kitten=updated_kitten)

            self.assertEqual(kitten_name_query.count(), 1, "Only 1 kitten name instance should be created per kitten.")

            kitten_name_instance = kitten_name_query.get()

            self.assertEqual(kitten_name_instance.name, expected_kitten_name)

        with self.subTest("It is possible to revert back the migration and recover the name"):
            kitten_name_model_after = self.get_model_after('testing_migrations.KittenName')

            updated_kitten = kitten_model.objects.get(pk=kitten.pk)
            kitten_name_model_after.objects.create(
                kitten=updated_kitten,
                name="foo",
            )

            self.run_reverse_migration()

            kitten_model = self.get_model_before('testing_migrations.Kitten')

            reverted_kitten = kitten_model.objects.get(pk=kitten.pk)

            self.assertEqual(reverted_kitten.name, expected_kitten_name, "Expects to have the first name given.")
