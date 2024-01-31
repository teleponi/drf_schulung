"""
PROJEKT URLS
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

from rest_framework.authtoken.views import obtain_auth_token

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth-token Erhalten
    path('api/token', obtain_auth_token, name='api_token_auth'),

    path('api/', include("events.api.urls")),

    # über browsable API authentifizieren:
    path('api-auth/', include("rest_framework.urls")),

    path(
        "schema/",
        SpectacularAPIView.as_view(api_version="v2"),
        name="schema",
    ),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),

   
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns