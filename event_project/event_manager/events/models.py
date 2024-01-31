from django.db import models
from django.core.validators import MinLengthValidator

from .validators import contains_xy


class ErrorLog(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    json_object = models.TextField(null=True, blank=True)
    error_msg = models.TextField(null=True, blank=True)
    http_status = models.PositiveSmallIntegerField(null=True, blank=True)


# Create your models here.
class Category(models.Model):
    """Model für eine Kategorie. Jedes Model muss von models.Model erben."""

    class Meta:
        # Meta-Informationen über das Model
        verbose_name_plural = "Kategorien"
        verbose_name = "Kategorie"

    created_at = models.DateTimeField(auto_now_add=True)  # Zeitstempel bei Anlegen setzen

    # immer, wenn Datensatz geändert wird, wird updated_at auf den Zeitstempel gesetzt
    updated_at = models.DateTimeField(auto_now=True) 

    name = models.CharField(max_length=100, 
                            validators=[MinLengthValidator(3)]
                            )  # mandatory, VARCHAR 100
    # null=True => darf in der DB NULL sein
    # blank=True => darf im Formular leer sein
    sub_title = models.CharField(max_length=100, null=True, blank=True)

    # mehrzeiliges Eingabefeld
    description = models.TextField(null=True, 
                                   blank=True, 
                                   validators=[contains_xy])

    def __str__(self) -> str:
        """String Repräsentation einer Python Classe. Die Kategorie soll
        mit ihrem Namen ausgegeben werden."""
        return self.name


class Event(models.Model):

    class MinGroup(models.IntegerChoices):
        """Select-Box in der Adminoberfläche"""
        SMALL = 2
        MEDIUM = 5
        BIG = 10

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    min_group = models.IntegerField(choices=MinGroup.choices)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="events"
    )
    
    is_active = models.BooleanField(default=True)
     

    def __str__(self) -> str:
        return self.name

