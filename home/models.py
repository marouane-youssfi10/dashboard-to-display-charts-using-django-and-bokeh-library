from django.db import models

# Create your models here.
class VoitureModel(models.Model):

    id = models.IntegerField(primary_key=True, default=False)
    name_car = models.CharField(max_length=50, default=False)
    type_car = models.CharField(max_length=50, default=False)
    price = models.IntegerField()
    ville = models.CharField(max_length=50, default=False)
    day = models.CharField(max_length=50, default=False)
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


# conseption
class Car(models.Model):
    id_car = models.IntegerField(primary_key=True, null=False)
    name_car = models.CharField(max_length=50)
    type_car = models.CharField(max_length=50)
    day = models.CharField(max_length=50)
    kilometrage = models.CharField(max_length=50)
    description = models.TextField()

    def __int__(self):
        return self.id_car

    class Meta:
        db_table = "cars"

class Model(models.Model):
    id_model = models.IntegerField(primary_key=True, null=False)
    model = models.CharField(max_length=50)
    marque = models.CharField(max_length=50)

    def __int__(self):
        return self.id_model

    class Meta:
        db_table = "model"

class Cpb(models.Model):
    id_cpb = models.IntegerField(primary_key=True, null=False)
    puissance = models.CharField(max_length=50)
    boite_a_vitesse = models.CharField(max_length=50)
    carburant = models.CharField(max_length=50)
    def __int__(self):
        return self.id_cpb

    class Meta:
        db_table = "cpb"

class Price(models.Model):
    id_price = models.IntegerField(primary_key=True, null=False)
    price = models.CharField(max_length=50)
    annee = models.CharField(max_length=50)
    def __int__(self):
        return self.id_price

    class Meta:
        db_table = "price"

class Fact_car(models.Model):
    id_fact = models.IntegerField(primary_key=True, null=False)
    id_car_fk = models.ForeignKey(Car, db_column="id_car", null=True, on_delete=models.SET_NULL)
    id_cpb_fk = models.ForeignKey(Cpb, db_column="id_cpb", null=True, on_delete=models.SET_NULL)
    id_model_fk = models.ForeignKey(Model, db_column="id_model", null=True, on_delete=models.SET_NULL)
    id_price_fk = models.ForeignKey(Price, db_column="id_price", null=True, on_delete=models.SET_NULL)

    def __int__(self):
        return self.id_fact
    class Meta:
        db_table = "fact_car"