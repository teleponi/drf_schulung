from rest_framework.test import APIClient, APITestCase
from rest_framework import status 

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

from events.models import Category 

# Create your tests here. category-list-create

URL_CREATE_CATEGORY = reverse("category-list-create")


class CategoryApiTest(APITestCase):

    def setUp(self):
        """Vor jeder Test-Methode wird diese Funktion ausgeführt."""

        self.payload = {
            "name": "Test cat",
            "sub_title": "test sub",
            "description": "test xy desc"  # Validierung im models.py
        }
        
    
    def test_category_liste_available(self):
        """TEsten, ob die Kategorie-Übersicht public verfügbar ist."""

        Category.objects.create(name="Test1 xxx")
        Category.objects.create(name="Test2")
        Category.objects.create(name="Test3")

        response = self.client.get(reverse("category-list-create"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, text="Test1 xxx")

    def test_create_category(self):
        """Testen, ob ein eingeloggter User eine Kategorie anlegen kann."""
        
        get_user_model().objects.create_superuser(username="bob2", email="xxxx@web.de", password="abcd1234")
        self.client.login(username="bob2", password="abcd1234")

        response = self.client.post(URL_CREATE_CATEGORY, data=self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Category.objects.count())  # 1 objekt wurde eingetragen

    def test_anonym_create_category(self):
        """Testen, ob ein nicht eingeloggter User eine Kategorie anlegen kann."""
        response = self.client.post(URL_CREATE_CATEGORY, data=self.payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)