import factory
from . import models


class AwesomeModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')

    class Meta:
        model = models.AwesomeModel


class KittenFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')

    class Meta:
        model = models.Kitten

