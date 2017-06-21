from datetime import datetime, timezone

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from my_app import models
from tests import factories


class TestUser(TestCase):

    def test_create_user(self):
        with self.subTest('It is possible to create a user without parameters'):
            user = User.objects.create()
            self.assertEqual('', user.username, 'By default the username is an empty string')

        with self.subTest('A created user can be fetched with the ORM'):
            self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_username_is_unique(self):
        with self.subTest('Creating a user with the same username is'):
            User.objects.create(username='foo')
            with self.assertRaises(IntegrityError), transaction.atomic():
                User.objects.create(username='foo')

        User.objects.create(username='bar')
        self.assertTrue(User.objects.filter(username='bar').exists())


class TestUserFactory(TestCase):

    def test_create_user(self):
        user = factories.UserFactory()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_username_is_unique(self):
        user1 = factories.UserFactory()
        user2 = factories.UserFactory()
        self.assertNotEqual(user1.username, user2.username)


class TestEntryModel(TestCase):

    def test_create_instance(self):
        blog = models.Blog.objects.create()

        entry = models.Entry.objects.create(
            pub_date=datetime.now(timezone.utc),
            mod_date=datetime.now(timezone.utc),
            n_comments=0,
            n_pingbacks=0,
            rating=0,
            blog=blog,
        )
        self.assertTrue(models.Entry.objects.filter(pk=entry.pk).exists())

    def test_create_instance_with_full_clean(self):
        blog = models.Blog.objects.create()

        entry = models.Entry.objects.create(
            pub_date=datetime.now(timezone.utc),
            mod_date=datetime.now(timezone.utc),
            n_comments=0,
            n_pingbacks=0,
            rating=0,
            blog=blog,
            headline='Lorem ipsum',
            body_text='Lorem ipsum',
        )
        entry.full_clean()
        self.assertTrue(models.Entry.objects.filter(pk=entry.pk).exists())

    def test_can_add_to_related(self):
        blog = models.Blog.objects.create()

        entry = models.Entry.objects.create(
            pub_date=datetime.now(timezone.utc),
            mod_date=datetime.now(timezone.utc),
            n_comments=0,
            n_pingbacks=0,
            rating=0,
            blog=blog,
        )
        author = models.Author.objects.create()
        entry.authors.add(author)
        self.assertTrue(entry.authors.exists())


class TestEntryFactory(TestCase):

    def test_can_create_blog_entry(self):
        with self.subTest('Entry values are already filled'):
            entry = factories.EntryFactory()
            self.assertTrue(models.Entry.objects.filter(pk=entry.pk).exists())
            self.assertTrue(models.Blog.objects.filter(pk=entry.blog.pk).exists())

        with self.subTest('Entry generated is already full_clean'):
            entry.full_clean()

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
