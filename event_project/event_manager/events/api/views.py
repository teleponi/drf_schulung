""" 
Views

Create, List => keine ID mit mitsenden
Update, Delete, Get => ID

"""
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework.authentication  import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from .serializers import EventSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly
from events.models import Category, Event, ErrorLog


# generische VIEWS:
class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.prefetch_related("category")
    filter_backends = [OrderingFilter, SearchFilter]
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAdminOrReadOnly]

    # http://127.0.0.1:8000/api/event/?ordering=category__name&name=history
    ordering_fields = ["name", "min_group", "category__name"]

    # http://127.0.0.1:8000/api/event/?ordering=name&search=xyz
    # search_fields = ["name", "category__name"]
    search_fields = ["=category__name"]  # exakte Suche

    # Modus Dach: search_fields = ["^name"]  # Muss mit Suchwort stasrten
    # Modus Regex: search_fields = ["$name"] # Regex-Suche für User ermöglichen
    # Exakter match. search_fields = ["=name"]

    def get_queryset(self):
        # hole erstmal das definierte Queryset
        qs = super().get_queryset()
        
        # wenn ?name=XY&author=thomas, dann filtere Queryset
        anfrage = self.request.GET.get("name")
        if anfrage:
            qs = qs.filter(name__contains=anfrage)
        return qs

    # @method_decorator(cache_page(60 * 2))  # 2 Minuten caching
    def get(self, *args, **kwargs):
        print(self.request.GET.get("name"))
        return super().get(*args, **kwargs)


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Event.objects.all()
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)  # serializer.save()
        except:
            ErrorLog.objects.create(json_object=request.data,
                                    http_status=status.HTTP_400_BAD_REQUEST,
                                    error_msg=serializer.errors)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryDetailUpdateAPIView(APIView):
    """eine Instanz einer Categorie holen, löschen oder updaten. 
    (erscheint in der Browsable API von DRF)."""

    def get_object(self, pk):
        """Hole Instanz und werfe einen 404-Fehler, falls Instanz
        nicht existiert."""
        instance = get_object_or_404(Category, pk=pk)  # hole Objekt oder 404 Fehler
        return instance

    def get(self, request, pk):
        """Hole eine Instanz. pk kommt von path(category/<int:pk>)"""
        instance = self.get_object(pk)
        serializer = CategorySerializer(instance)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        """Hole eine Instanz. pk kommt von path(category/<int:pk>)"""
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk):
        """Vollständiger Update einer Resource."""
        instance = self.get_object(pk)
        serializer = CategorySerializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        """Partieller Update einer Resource."""
        instance = self.get_object(pk)

        # bei patch partial
        serializer = CategorySerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryListCreateAPIView(APIView):
    """List (get) and create (post) Categories."""

    def get(self, request):
        """Wird aufgerufen über http get.
        
        api/category
        """

        # Request-Objekt
        print(request.method)
        print(request.user)
        print(request.headers)

        items = Category.objects.all()
        # many = True, wenn ein items ein Queryset ist
        serializer = CategorySerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        POST Request
        """
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)