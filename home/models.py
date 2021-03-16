from django.db import models

# Create your models here.
class VoitureModel(models.Model):

    id = models.IntegerField(primary_key=True, default=False)
    name_car = models.CharField(max_length=50, default=False)
    type_car = models.CharField(max_length=50, default=False)
    price = models.IntegerField()
    ville = models.CharField(max_length=50, default=False)
    time = models.CharField(max_length=50, default=False)
    carburant = models.CharField(max_length=50, default=False)
    puissance = models.IntegerField()
    boite_a_vitesse = models.CharField(max_length=50, default=False)
    kilometrage = models.CharField(max_length=50, default=False)
    annee = models.IntegerField()
    marque = models.CharField(max_length=50, default=False)
    model = models.CharField(max_length=50, default=False)
    description = models.TextField()

    def __str__(self): # dunder function
        return self.name_car

    class Meta:
        db_table = "car"

        

