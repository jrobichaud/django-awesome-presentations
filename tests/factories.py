
import factory
from django.contrib.auth.models import User


class UserFactory(factory.DjangoModelFactory):
    email = factory.Faker('safe_email')
    username = factory.Faker('pystr')

    class Meta:
        model = User
