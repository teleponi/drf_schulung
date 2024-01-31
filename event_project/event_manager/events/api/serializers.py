from rest_framework import serializers
import re 

from events import models 


class EventInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Event
        fields = ["id", "name"]


class CategorySerializer(serializers.ModelSerializer):
    """Einfacher Serializer für das Category Model."""

    # nested Serializer (events muss als related_name im Event-Model angegeben sein!)
    events = EventInlineSerializer(many=True, read_only=True)

    class Meta:
        model = models.Category
        fields = "__all__"  # alle Felder!
    
    def validate_name(self, current_value):
        """Prüfe, ob XY im Namen vorkommt.
        
        Django sucht nach validate_FELDNAME - Methoden, und führt diese aus.
        (siehe Folie validators.pdf)
        
        """
        if not re.match("[a-zA-Z].*", current_value):
            raise serializers.ValidationError("Kategorie muss mit einem Buchstaben anfangen")

        return current_value


class EventSerializer(serializers.ModelSerializer):
    """Einfacher Serializer für das Event Model."""

    # category = serializers.StringRelatedField()


    class Meta:
        model = models.Event
        fields = "__all__"  # alle Felder!

        extra_kwargs = {
            'description': {'max_length': 10, 'error_messages': {'max_length': 'Description is too long.'}},
        }
    
    def validate(self, data):
        """Cross Field Validation"""
        if data["is_active"] and data["category"].name == "Sports":
            raise serializers.ValidationError("Sport kann nicht aktiv sein!")

        return data
    
    def to_representation(self, instance):
        repr = super().to_representation(instance)
        repr["category_name"] = instance.category.name
        return repr