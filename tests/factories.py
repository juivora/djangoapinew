# factories.py
import factory
from account.models import Blog


class BlogFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Blog

    title = factory.faker.Faker('name')
    description = factory.faker.Faker('text')
    image = factory.Faker("slug")
    user_id = 67