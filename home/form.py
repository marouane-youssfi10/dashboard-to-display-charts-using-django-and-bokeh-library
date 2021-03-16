from django.forms import ModelForm
from .models import VoitureModel


class TestingForm(ModelForm):
    class Meta:
        model = VoitureModel
        fields = '__all__'
