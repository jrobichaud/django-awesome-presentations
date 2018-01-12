import factory
from . import models


class AwesomeModelFactory(factory.DjangoModelFactory):
    name = factory.Faker('pystr')

    class Meta:
        model = models.AwesomeModel
