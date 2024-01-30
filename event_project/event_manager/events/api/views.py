""" 
Views

Create, List => keine ID mit mitsenden
Update, Delete, Get => ID

"""
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from .serializers import EventSerializer, CategorySerializer
from events.models import Category, Event, ErrorLog


# generische VIEWS:
class EventListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class EventRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Event.objects.all()

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