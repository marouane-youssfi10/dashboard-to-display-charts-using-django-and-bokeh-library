from rest_framework import serializers
from .models import VoitureModel

class VoitureModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoitureModel
        fields = ('id', 'name_car', 'model', 'price', 'ville', 'annee')
