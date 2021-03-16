from django.contrib import admin
from .models import VoitureModel
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name_car', 'marque', 'model', 'price')
    list_display = ('id', 'name_car', 'type_car', 'price', 'ville', 'time',  'carburant', 'puissance', 'boite_a_vitesse', 'kilometrage', 'annee', 'marque', 'model', 'description')
    # list_filter = ('marque', 'ville')

admin.site.register(VoitureModel, CarAdmin)
