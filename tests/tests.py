from django.contrib.auth.models import User
from django.test import TestCase

from tests import factories


class TestUserFactory(TestCase):

    def test_create_user(self):
        user = factories.UserFactory()
        self.assertTrue(User.objects.filter(pk=user.pk).exists())

    def test_create_user_emails(self):
        users = factories.UserFactory.create_batch(2)
        self.assertNotEqual(users[0].email, users[1].email)
