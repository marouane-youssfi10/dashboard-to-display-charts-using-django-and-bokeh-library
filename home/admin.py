from django.contrib import admin
from .models import VoitureModel
from .models import Car, Cpb, Model, Price, Fact_car
# Register your models here.


class CarAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name_car', 'marque', 'model', 'price')
    list_display = ('id', 'name_car', 'type_car', 'price', 'ville', 'day',  'carburant', 'puissance', 'boite_a_vitesse', 'kilometrage', 'annee', 'marque', 'model', 'description')
    # list_filter = ('marque', 'ville')

class CarsAdmin(admin.ModelAdmin):
    search_fields = ('id_car', 'name_car', 'type_car', 'day', 'description')
    list_display = ('id_car', 'name_car', 'type_car', 'day', 'description')
    list_filter = ('name_car',)

class CpbAdmin(admin.ModelAdmin):
    search_fields = ('id_cpb', 'puissance', 'boite_a_vitesse', 'carburant')
    list_display = ('id_cpb', 'puissance', 'boite_a_vitesse', 'carburant')
class ModelAdmin(admin.ModelAdmin):
    search_fields = ('id_model', 'model', 'marque')
    list_display = ('id_model', 'model', 'marque')

class PriceAdmin(admin.ModelAdmin):
    search_fields = ('id_price', 'price', 'annee')
    list_display = ('id_price', 'price', 'annee')

class FactAdmin(admin.ModelAdmin):
    search_fields = ('id_fact', 'id_car_fk', 'id_cpb_fk', 'id_model_fk', 'id_price_fk')
    list_display = ('id_fact', 'id_car_fk', 'id_cpb_fk', 'id_model_fk', 'id_price_fk')

admin.site.register(VoitureModel, CarAdmin)
admin.site.register(Car, CarsAdmin)
admin.site.register(Cpb, CpbAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Fact_car, FactAdmin)