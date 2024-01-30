import random
from datetime import timedelta

import factory
import faker

from django.contrib.auth import get_user_model


from . import models

User = get_user_model()
categories = [
    "Sports",
    "Talk",
    "Cooking",
    "Freetime",
    "Hiking",
    "Movies",
    "Travelling",
    "Science",
    "Arts",
    "Pets",
    "Music",
    "Wellness",
]


class CategoryFactory(factory.django.DjangoModelFactory):
    """Erstellt eine Kategorie aus einer vorgegebenen Liste."""

    class Meta:
        model = models.Category

    name = factory.Iterator(categories)
    sub_title = factory.Faker("sentence", locale="de_DE")
    description = factory.Faker("paragraph", nb_sentences=20, locale="de_DE")


class EventFactory(factory.django.DjangoModelFactory):
    """Event Fabrik zum Erstellen eines neuen Events."""

    class Meta:
        model = models.Event

    # falls EventFactory(author=xx, category=y)auferufen,
    # werden diese beiden ignoiert. ansosnten wird erzeugt und genommen
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker("sentence")
    description = factory.Faker("paragraph", nb_sentences=20, locale="de_DE")
    min_group = factory.LazyAttribute(lambda _: random.choice(list(models.Event.MinGroup)))
    is_active = factory.Faker("boolean", chance_of_getting_true=50)



