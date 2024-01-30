"""
Generating Event Data.

This module provides a management command to generate random
event data built with factory boy and the faker libary.
"""

import random
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from events.factories import CategoryFactory
from events.factories import EventFactory
from events.models import Category
from events.models import Event


CATEGORIES = 4
EVENTS = 20


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        num_events = 1000
        num_categories = 10

        print(
            f"Generating {num_events=} {num_categories=} "
        )
   

        print("Lösche Model Data...")
        for m in [Event, Category]:
            m.objects.all().delete()

        print("Erstelle Kategorien...")

        categories = CategoryFactory.create_batch(num_categories)

        print("Erstelle Events...")
        for _ in range(num_events):
            event = EventFactory(
                category=random.choice(categories),
             )