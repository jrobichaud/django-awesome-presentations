from datetime import datetime, timezone

import factory
from django.contrib.auth.models import User
from faker.generator import random

from my_app import models

from faker import Faker
fake = Faker()


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker('safe_email')
    username = factory.Faker('pystr')


class BlogFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Blog

    name = factory.Faker('sentence', nb_words=4)
    tagline = factory.Faker('sentence', nb_words=10)


class BlogWithEntryFactory(BlogFactory):
    blog = factory.RelatedFactory('tests.factories.EntryFactory', factory_related_name='blog')


class AuthorFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Author

    name = factory.Faker('name')
    email = factory.Faker('safe_email')


class EntryFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Entry

    class Params:
        with_authors = factory.Trait(
            authors=factory.LazyFunction(
                lambda: tuple(
                    AuthorFactory.create_batch(random.randint(1, 10))
                )
            )
        )

    blog = factory.SubFactory(BlogFactory)
    headline = factory.Faker('sentence', nb_words=4)
    body_text = factory.Faker('paragraphs', nb=4)
    pub_date = factory.Faker('past_datetime', start_date="-30d")
    mod_date = factory.LazyAttribute(
        lambda e: fake.date_time_between_dates(
            datetime_start=e.pub_date,
            datetime_end=datetime.now(timezone.utc)
        )
    )

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of authors were passed in, use them
            for author in extracted:
                self.authors.add(author)

    n_comments = factory.Faker('pyint')
    n_pingbacks = factory.Faker('pyint')
    rating = factory.Faker('pyint')


