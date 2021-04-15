from django.shortcuts import render, redirect
import statistics
import pandas as pd


from .form import TestingForm
from .models import VoitureModel, Fact_car
from django.http import HttpResponseRedirect
from .templates.bokeh_chart.bar_chart import bar_chart
from .templates.bokeh_chart.line_chart import line_chart
from .templates.bokeh_chart.pie_chart import pie_chart
from .templates.bokeh_chart.scatter_chart import scatter_chart
from django.db import connection

def home(request):
    return render(request, 'pages/login.html')

def chart(request):
    if request.method == "POST":
        # create des list
        name_car1 = []
        price = []
        annee = []
        marque = []
        model = []
        boite_a_vitesse = []
        carburant = []
        puissance = []
        ville = []
        time = []
        kilometrage = []
        descriptions = []
        ville_pie = []
        # test
        name = request.POST.get('name_car') # dacia logan
        model_display = request.POST.get('model') # dacia logan

        showsearch = VoitureModel.objects.all()
        city_for_pie_chart = VoitureModel.objects.all()

        # search name
        if 'name_car' in request.POST:
            name_car = request.POST['name_car']
            if name_car:
                print('------------------name_car---------------')
                print('name = ', name_car)
                if showsearch.filter(name_car__icontains=name_car) is None:
                    pass
                else:
                    city_for_pie_chart = city_for_pie_chart.filter(name_car__icontains=name_car)
                    showsearch = showsearch.filter(name_car__icontains=name_car)
        # if name not exist in database
        n = 'name'
        if not showsearch:
            return render(request, 'home/error.html', {'name': name_car, 'input': n})#
        # search with model
        if 'model' in request.POST:
            model_1 = request.POST['model']
            if model_1:
                print('-----------------model---------------')
                print('model = ', model_1, '\n')
                city_for_pie_chart = city_for_pie_chart.filter(model__iexact=model_1)
                showsearch = showsearch.filter(model__iexact=model_1)#
        # if model not exist in database
        n = 'model'
        if not showsearch:
            return render(request, 'home/error.html', {'name': model_1, 'input': n})#
        # search with city
        if 'city' in request.POST:
            city_1 = request.POST['city']
            if city_1:
                print('-----------------city---------------')
                print('city = ', city_1, '\n')
                showsearch = showsearch.filter(ville__iexact=city_1)#
        # if city not exist in database
        n = 'ville'
        if not showsearch:
            return render(request, 'home/error.html', {'name': city_1, 'input': n})##
        # search with 'boite a vitesse'
        if 'boite_a_vitesse' in request.POST:
            boite_a_vitesse_1 = request.POST['boite_a_vitesse']
            if boite_a_vitesse_1:
                print('-------------------boite_a_vitesse_1---------------')
                print('boite_a_vitesse = ', boite_a_vitesse_1, '\n')
                city_for_pie_chart = city_for_pie_chart.filter(boite_a_vitesse__iexact=boite_a_vitesse_1)
                showsearch = showsearch.filter(boite_a_vitesse__iexact=boite_a_vitesse_1)
        # if boite_a_vitesse not exist in database
        n = 'boite a vitesse'
        if not showsearch:
            return render(request, 'home/error.html', {'name': boite_a_vitesse_1, 'input': n})#
        # search with min & max price
        if 'min_price' in request.POST:
            min_price = request.POST['min_price']
            max_price = request.POST['max_price']
            if max_price:
                print('---------------------min price & max price---------------')
                print('min_price = ', min_price)
                print('max_price = ', max_price, '\n')
                city_for_pie_chart = city_for_pie_chart.filter(price__gte=min_price, price__lte=max_price)
                showsearch = showsearch.filter(price__gte=min_price, price__lte=max_price)
        # if min_price and max_price not exist in database
        p = 'does not exist'
        n = 'min and max price'
        if not showsearch:
            return render(request, 'home/error_price.html', {'name': p, 'input': n})

        # append data to list
        for i in showsearch:
            name_car1.append(i.name_car)
            price.append(i.price)
            annee.append(i.annee)
            marque.append(i.marque)
            model.append(i.model)
            boite_a_vitesse.append(i.boite_a_vitesse)
            carburant.append(i.carburant)
            puissance.append(i.puissance)
            ville.append(i.ville)
            time.append(i.day)
            kilometrage.append(i.kilometrage)
            descriptions.append(i.description)

        # hadi bnsba l pie chart bach ibano lmodon kamlin f pie chart
        for i in city_for_pie_chart:
            ville_pie.append(i.ville)

        # insert data to dataframe
        df = pd.DataFrame({
            'name_car': name_car1,
            'price': price,
            'annee': annee,
            'marque': marque,
            'model': model,
            'boite_a_vitesse': boite_a_vitesse,
            'carburant': carburant,
            'puissance': puissance,
            'ville': ville,
            'time': time,
            'kilometrage': kilometrage,
            'descriptions': descriptions
        })

        print('df = ', df.shape)

        # calcul statsics
        try:
            max = df['price'].max()
            min = df['price'].min()
        except:
            max = '----'
            min = '----'
        try:
            mean = round(df['price'].mean(), 1)
        except:
            mean = '----'
        try:
            mediane = round(statistics.median(df['price']), 1)
        except:
            mediane = '----'
        try:
            variance = round(statistics.variance(df['price']), 1)
        except:
            variance = '----'
        try:
            ecart_type = round(df['price'].std(), 1)
        except:
            ecart_type = '----'

        number_of_car = df['name_car'].count()

        TOOLS = 'box_select,reset,wheel_zoom, pan, save'

        # making chart scatter
        scatter_div, scatter_script = scatter_chart(df, name, TOOLS, model_display)

        # making pie chart
        # algorithme for count  ville
        count_ville = []
        villeL = list(set(ville_pie))
        for i in villeL:
            count_ville.append(ville_pie.count(i))
        # ---------end algorithme ----------------

        p = []
        percentage = [d / sum(count_ville) * 100 for d in count_ville]

        # ------ % this for one number after comma -------
        for i in percentage:
            p.append(str(round(i, 1)))
        # ------------------------------------------------

        df_for_pie_char = pd.DataFrame({
            'villeL': villeL,
            'count_ville': count_ville,
            'percentage': p,
        })
        # making pie chart
        pie_script, pie_div = pie_chart(name, TOOLS, df_for_pie_char)

        # making bar chart
        bar_script, bar_div = bar_chart(carburant, name, TOOLS)

        # making line chart
        # algorithm for count price
        count_price = []
        priceL = list(set(price))
        for i in priceL:
            count_price.append(price.count(i))

        df_for_line_char = pd.DataFrame({
            'priceL': priceL,
            'count_price': count_price
        })
        df_for_line_char = df_for_line_char.reset_index(drop=False)
        df_for_line_char = df_for_line_char.sort_values(by=['priceL'], ascending=True)

        line_script, line_div = line_chart(name, model_display, TOOLS, df_for_line_char)

        context = {
                'showsearch': showsearch,

                'name': name,
                'model_display': model_display,
                'number_of_car': number_of_car,
                'max': max,
                'min': min,
                'mean': mean,
                'mediane': mediane,
                'variance': variance,
                'ecart_type': ecart_type,

                'scatter_script': scatter_script, 'scatter_div': scatter_div,
                'pie_script': pie_script, 'pie_div': pie_div,
                'bar_script': bar_script, 'bar_div': bar_div,
                'line_script': line_script, 'line_div': line_div
        }
        return render(request, 'home/chart.html', context)
    else:
        return render(request, 'form/no_form.html')

def about(request):
    return render(request, 'pages/about.html')

# create function 'create, update, delete'
def create_order(request):
    form = TestingForm()
    last_id = VoitureModel.objects.order_by('id').last()
    print('last_id = ', last_id.id)
    # print('form = ', form)
    if request.method == 'POST':
        # print('---------------- Printing POST:', request.POST)
        form = TestingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        else:
            exist = 'this id already exist'
            return render(request, 'editing/already.html', {'already': exist})

    print('form = ', form)
    print('-----------------------------------------------')
    # print('form.name_car = ', form.name_car)
    context = {
        'form': form,
        'last_id': last_id.id + 1
    }
    return render(request, 'editing/create_order.html', context)

def update_order(request, pk):
    # print('id = ', pk)
    order = VoitureModel.objects.get(id=pk)
    # print('name = ', order)
    form = TestingForm(instance=order)
    if request.method == 'POST':
        form = TestingForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            print('save_update')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {'form': form}
    return render(request, 'editing/update_order.html', context)

def delete_order(request, pk):
    order = VoitureModel.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')

    context = {'item': order}

    return render(request, 'editing/delete_order.html', context)
# end create update delete

# API

from rest_framework import viewsets
from .serializers import VoitureModelSerializer
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

# libary for Authentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly, DjangoModelPermissions

class VoitureModelViewSet(viewsets.ModelViewSet):
    print('\n', '----- class CLientVIewSet ------', '\n')
    filter_backends = (SearchFilter, )
    # queryset = VoitureModel.objects.filter(name_car__icontains='dacia logan')
    serializer_class = VoitureModelSerializer
    search_fields = ('name_car', 'price')
    filter_fields = ('id', 'name_car', 'price') # /?name_car=dacia logan&price=20 000

    # katsift request f headers postman like Authorization : Token code 3ad atjik response
    authentication_classes = [TokenAuthentication]

    # hadi kanst3mloha ila brit tjik response bla matsift Authorization fl header d postman oula chi haja f body.
    # permission_classes = [AllowAny]

    # had kanst3mloha bach t3i l7a9 hi l user li 3ndhoum Staff status active.
    # permission_classes = [IsAdminUser]

    # hadi kat3tik l7a9 ta5d data bla matsift l Authorization. wila briti dir update darouri 5ask tsift Authorization
    # permission_classes = [IsAuthenticatedOrReadOnly]

    # hadi kat3tik l7a9 l nass wach imklhoum idiro l update ldata dyalk ou la izido chi item...
    # permission_classes = [DjangoModelPermissions]

    def get_queryset(self):
        print('\n', '---------- get_queryset    -----------', '\n')
        name = self.request.query_params.get('search', None)
        id = self.request.query_params.get('id', None)
        name_car = self.request.query_params.get('name_car', None)
        price = self.request.query_params.get('price', None)
        print('name = ' + str(name) + '...' + 'name_car = ' + str(name_car) + '...' + 'price = ' + str(price), '\n')
        if name:
            print('///////////// if ////////////////', name)
            return VoitureModel.objects.filter(name_car__icontains=str(name))
        elif name_car:
            print('//////////// elif 1 //////////////', name)
            return VoitureModel.objects.filter(name_car__icontains=str(name_car))
        elif name_car and price:
            print('//////////// elif 2 /////////////', name_car, '--', price)
            if VoitureModel.objects.filter(name_car__icontains=str(name_car), price__iexact=price) is None:
                print(" -- None --")
            return VoitureModel.objects.filter(name_car__icontains=str(name_car), price__iexact=price)
        elif id:
            print('//////////// elif 3 /////////////', id)
            return VoitureModel.objects.filter(id=id)
        else:
            print('//////////// else ///////////////', name)
            return VoitureModel.objects.filter(id=5)

    def list(self, request, *args, **kwargs):
        print('\n', '-------------- list ---------------', '\n')
        cars = self.get_queryset()
        serializer = VoitureModelSerializer(cars, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        return Response("Not Allowed Baby")