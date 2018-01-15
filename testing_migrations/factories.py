import factory
from . import models


class AwesomeModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')

    class Meta:
        model = models.AwesomeModel


class KittenFactory(factory.DjangoModelFactory):

    class Meta:
        model = models.Kitten


class KittenName(factory.DjangoModelFactory):
    name = factory.Faker('pystr')
    kitten = factory.SubFactory(KittenFactory)

    class Meta:
        model = models.KittenName
