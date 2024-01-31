""" 
API URLs
"""
from django.views.decorators.cache import cache_page

from django.urls import path
from .views import CategoryListCreateAPIView
from .views import CategoryDetailUpdateAPIView
from .views import EventListCreateAPIView, EventRetrieveUpdateDestroyAPIView
from .views import CategoryListCreateView

urlpatterns = [
    # api/category
    path(
        "category/",
        CategoryListCreateAPIView.as_view(),
        name="category-list-create"
    ),
    # api/category/3
    path("category/<int:pk>", CategoryDetailUpdateAPIView.as_view(), name="detail-update-delete"),
    path("event/", EventListCreateAPIView.as_view(), name="event-list-create"),
    path("event/<int:pk>", EventRetrieveUpdateDestroyAPIView.as_view(), name="event-retrieve-update-destroy"),

    # Kategorie anlegen und im Fehlerfall im Errorlog eintragen
    # CACHING kann man in den urlpatterns setzen (oder in der View (siehe views.py))
    path("category2/", cache_page(60 * 15)(CategoryListCreateView.as_view()), name="category-error-log"),
]
