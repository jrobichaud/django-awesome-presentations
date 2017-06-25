from django.contrib.auth.models import User
from django.test import TestCase

from my_app import models
from tests import factories


class TestUserFactory(TestCase):

    def test_create_user(self):
        user = factories.UserFactory()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_can_still_override_fields(self):
        user = factories.UserFactory(username='foo')
        self.assertEqual('foo', user.username)

    def test_username_is_unique(self):
        user1 = factories.UserFactory()
        user2 = factories.UserFactory()
        self.assertNotEqual(user1.username, user2.username)


class TestEntryFactory(TestCase):

    def test_can_create_blog_entry(self):
        with self.subTest('Entry values are already filled'):
            entry = factories.EntryFactory()
            self.assertTrue(models.Entry.objects.filter(pk=entry.pk).exists())
            self.assertTrue(models.Blog.objects.filter(pk=entry.blog.pk).exists())

        with self.subTest('Entry generated is already full_clean'):
            entry.full_clean()

    def test_can_override_values_of_foreign_keys(self):
        entry = factories.EntryFactory(blog__name='Awesome blog')
        self.assertEqual('Awesome blog', entry.blog.name)

    def test_factory_can_create_many_to_many(self):
        with self.subTest('Can add authors to the factory'):
            author = factories.AuthorFactory()
            entry = factories.EntryFactory(
                authors=(author,)
            )
            self.assertEqual(1, entry.authors.count())

        with self.subTest('Traits can simplify greatly some usage'):
            entry = factories.EntryFactory(
                with_authors=True
            )
            self.assertTrue(entry.authors.exists())


class TestRelatedFactory(TestCase):

    def test_can_create_blog_with_existing_entry(self):
        blog = factories.BlogWithEntryFactory()

        self.assertTrue(blog.entry_set.exists())
