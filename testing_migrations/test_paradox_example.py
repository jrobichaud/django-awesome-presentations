from unittest import skipIf

import os
from django_migration_testcase import MigrationTest

EXAMPLE_CODE_PARADOX = bool(os.environ.get('EXAMPLE_CODE_PARADOX', False))


class Test0005MigrateToKittenName(MigrationTest):
    app_name = 'testing_migrations'
    before = '0004_kittenname'
    after = '0007_remove_kitten_name'

    @skipIf(not EXAMPLE_CODE_PARADOX, "This test fails due to space-time paradox.")
    def test_name_is_properly_transferred_through_migrations(self):
        expected_kitten_name = 'Soft Kitty'
        from .factories import KittenFactory

        # This is an example of a space-time paradox. the factory at the "time" of the migration there was a name in the
        # factory but it was removed
        KittenFactory(name=expected_kitten_name)