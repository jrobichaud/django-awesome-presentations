from datetime import timezone, datetime

import factory
import faker
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.test import TestCase

from tests import factories

fake = faker.Faker()


class TestUserChangeForm(TestCase):

    def test_form_can_change_username(self):
        username = fake.user_name()

        User.objects.create(
            username=fake.user_name()
        )
        user = User.objects.create()
        form_data = dict(
            username=username,
            first_name='foo',
            last_name='bar',
            date_joined=datetime.now(),
        )
        form = UserChangeForm(
            instance=user,
            data=form_data
        )

        with self.subTest('Form is valid'):
            self.assertTrue(form.is_valid(), form.errors)

        with self.subTest('Form updates username'):
            form.save()
            updated_user = User.objects.get(id=user.id)
            self.assertEqual(username, updated_user.username)

    def test_cannot_change_to_an_existing_username(self):
        username = fake.user_name()
        User.objects.create(
            username=username
        )
        user = User.objects.create()
        form_data = dict(
            username=username,
            first_name='foo',
            last_name='bar',
            date_joined=datetime.now(),
        )
        form = UserChangeForm(
            instance=user,
            data=form_data
        )
        self.assertFalse(form.is_valid())
        self.assertIn('A user with that username already exists.', form.errors['username'])


class TestUserChangeFormWithFactory(TestCase):

    class UserChangeFormFactory(factory.DictFactory):
        username = factory.Faker('user_name')
        first_name = factory.Faker('first_name')
        last_name = factory.Faker('last_name')
        date_joined = factory.Faker('past_date', tzinfo=timezone.utc)

    def test_form_can_change_username(self):
        username = fake.user_name()
        factories.UserFactory()
        user = factories.UserFactory()

        form_data = self.UserChangeFormFactory(
            username=username
        )
        form = UserChangeForm(
            instance=user,
            data=form_data
        )

        with self.subTest('Form is valid'):
            self.assertTrue(form.is_valid())

        with self.subTest('Form updates username'):
            form.save()
            updated_user = User.objects.get(id=user.id)
            self.assertEqual(username, updated_user.username)

    def test_cannot_change_to_an_existing_username(self):
        username = fake.user_name()
        factories.UserFactory(
            username=username
        )
        user = factories.UserFactory()
        form_data = self.UserChangeFormFactory(
            username=username
        )
        form = UserChangeForm(
            instance=user,
            data=form_data
        )
        self.assertFalse(form.is_valid())
        self.assertIn('A user with that username already exists.', form.errors['username'])
