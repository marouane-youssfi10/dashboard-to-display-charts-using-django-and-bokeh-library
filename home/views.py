from home.models import VoitureModel
from django.shortcuts import render, redirect
from bokeh.plotting import figure
from bokeh.transform import cumsum
from bokeh.embed import components
from bokeh.models import ColumnDataSource
from math import pi
from bokeh.models import HoverTool
from bokeh.models import Legend
from bokeh.models import NumeralTickFormatter
import statistics
import pandas as pd
import json
from .form import TestingForm
from .models import VoitureModel
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponseRedirect

def home(request):
    return render(request, 'pages/login.html')

def chart(request):
    if request.method == "POST":
        # try:
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

        name = request.POST.get('name_car') # dacia logan
        model_display = request.POST.get('model') # dacia logan

        showsearch = VoitureModel.objects.all()
        city_for_pie_chart = VoitureModel.objects.all()

        # search name
        if 'name_car' in request.POST:
            name_car = request.POST['name_car']
            if name_car:
                print('---------------------name_car---------------')
                print('name = ', name_car)
                if showsearch.filter(name_car__icontains=name_car) is None:
                    pass
                else:
                    city_for_pie_chart = city_for_pie_chart.filter(name_car__icontains=name_car)
                    showsearch = showsearch.filter(name_car__icontains=name_car)

        # if name not exist in database
        n = 'name'
        if not showsearch:
            return render(request, 'home/error.html', {'name': name_car, 'input': n})

        # search with model
        if 'model' in request.POST:
            model_1 = request.POST['model']
            if model_1:
                print('---------------------model---------------')
                print('model = ', model_1, '\n')
                city_for_pie_chart = city_for_pie_chart.filter(model__iexact=model_1)
                showsearch = showsearch.filter(model__iexact=model_1)

        # if model not exist in database
        n = 'model'
        if not showsearch:
            return render(request, 'home/error.html', {'name': model_1, 'input': n})

        # search with city
        if 'city' in request.POST:
            city_1 = request.POST['city']
            if city_1:
                print('---------------------model---------------')
                print('city = ', city_1, '\n')
                showsearch = showsearch.filter(ville__iexact=city_1)

        # if city not exist in database
        n = 'ville'
        if not showsearch:
            return render(request, 'home/error.html', {'name': city_1, 'input': n})


        # search with 'boite a vitesse'
        if 'boite_a_vitesse' in request.POST:
            boite_a_vitesse_1 = request.POST['boite_a_vitesse']
            if boite_a_vitesse_1:
                print('---------------------boite_a_vitesse_1---------------')
                print('boite_a_vitesse = ', boite_a_vitesse_1, '\n')
                city_for_pie_chart = city_for_pie_chart.filter(boite_a_vitesse__iexact=boite_a_vitesse_1)
                showsearch = showsearch.filter(boite_a_vitesse__iexact=boite_a_vitesse_1)

        # if boite_a_vitesse not exist in database
        n = 'boite a vitesse'
        if not showsearch:
            return render(request, 'home/error.html', {'name': boite_a_vitesse_1, 'input': n})

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
            time.append(i.time)
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

        # ---------------making chart scatter-----------------------------------------
        TOOLTIPS = """<table>
                           <tr>
                                <td style="color:blue;"> nom   <td>
                                <td>: @name_car   </td>
                           </tr>
                           <tr>
                                <td style="color:blue;"> Price   <td>
                                <td>: @price DH  </td>
                           </tr>
                           <tr>
                                <td style="color:blue;"> Année  <td>
                                <td>: @annee   </td>
                           </tr>
                           <tr>
                                <td style="color:blue;"> Ville  <td>
                                <td>: @ville   </td>
                           </tr>
                           <tr>
                                <td colspan="2" height="10px"></td>
                                <td colspan="2"></td>
                           </tr>
                      </table>"""

        scatter_chart = figure(plot_width=530, plot_height=337,
                               toolbar_location='above', # title='scatter chart'
                               x_axis_label='année de voiture', y_axis_label='Price(DH)', tools=TOOLS,
                               x_range=(df['annee'].min() - 1, df['annee'].max() + 5))

        scatter_chart.circle(x='annee', y='price', source=df, size=11, color='#4e73df', legend_label=name + ' ' + model_display,
                             hover_color="#D8D8D8")
        scatter_chart.add_layout(Legend(), 'center')
        scatter_chart.add_tools(HoverTool(tooltips=TOOLTIPS))
        scatter_chart.legend.background_fill_alpha = 1  # bach tban chafafa

        scatter_chart.yaxis[0].formatter = NumeralTickFormatter(format="0")  # bach matbanh 3la ckll 3.500e+5

        # legend
        # scatter_chart.legend.label_text_font = "times"
        # scatter_chart.legend.label_text_color = "#224abe"
        # scatter_chart.legend.label_text_font_size = "10pt"
        # scatter_chart.legend.background_fill_color = "#f8f9fc"
        # scatter_chart.legend.background_fill_color = "#ebefff" background d legend

        # x-axis & y-axis
        scatter_chart.xaxis.axis_label_text_font_size = "12pt"
        scatter_chart.yaxis.axis_label_text_font_size = "12pt"
        scatter_chart.xaxis.axis_label_text_font = "Calibri"
        scatter_chart.yaxis.axis_label_text_font = "Calibri"
        scatter_chart.yaxis.minor_tick_line_color = None
        scatter_chart.xgrid.grid_line_color = None

        # Title
        scatter_chart.title.text_font_size = '13pt'
        scatter_chart.title.text_font = 'Arial'
        scatter_chart.title.text_color = "#224abe"

        # border
        scatter_chart.outline_line_width = 2
        scatter_chart.outline_line_alpha = 0.1
        # scatter_chart.outline_line_color = "#4e73df"

        # change just some things about the x-axis
        scatter_chart.xaxis.axis_line_width = 1.5
        scatter_chart.xaxis.axis_line_color = "#99b0ff"

        # change just some things about the y-axis
        scatter_chart.yaxis.axis_line_color = None # "#99b0ff"
        scatter_chart.yaxis.axis_line_width = 1.5

        scatter_script, scatter_div = components(scatter_chart)
        # ----------------------------------------------------------------------------------------


        # ------------------------------------- pie chart ------------------------------------------

        # algorithme for calcul count of ville
        count_ville = []
        villeL = list(set(ville_pie))
        for i in villeL:
            count_ville.append(ville_pie.count(i))
        # -------------------------------------------

        p = []
        percentage = [d / sum(count_ville) * 100 for d in count_ville]
        # ----------- % ra9m wahd mour lfasila ------------
        for i in percentage:
            p.append(str(round(i, 1)))
        # ------------------------------------------------
        df_for_pie_char = pd.DataFrame({
            'villeL': villeL,
            'count_ville': count_ville,
            'percentage': p,
        })

        df_for_pie_char = df_for_pie_char.sort_values(['count_ville'], ascending=False)

        color = [
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9 '
            '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9 '
            '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
            '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d', '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
            '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc', '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9'
        ]

        df_for_pie_char['angle'] = df_for_pie_char['count_ville'] / df_for_pie_char['count_ville'].sum() * 2 * pi
        colors = []
        for i in range(len(df_for_pie_char['count_ville'])):
            colors.append(color[i])
        df_for_pie_char['color'] = colors

        TOOLTIPS_pie = """<table>
                                <tr>
                                     <td style="color:blue;"> Ville   <td>
                                     <td>: @villeL   </td>
                                </tr>
                                <tr>
                                     <td style="color:blue;"> Percentage  <td>
                                     <td>: @percentage %   </td>
                                </tr>
                          </table>"""

        title = 'le nombre de voiture"' + name + '"dans chaque ville'
        pie_chart = figure(plot_height=400, # title=title,
                           toolbar_location='above', tools=TOOLS, tooltips=TOOLTIPS_pie, x_range=(-0.5, 1.1))

        pie_chart.wedge(x=0.1, y=1.3, radius=0.4, hover_color="#94afff",
                        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
                        line_color="white", fill_color='color', legend_field='villeL', source=df_for_pie_char)

        # axis
        pie_chart.axis.axis_label = None
        pie_chart.axis.visible = False
        pie_chart.grid.grid_line_color = None

        # legend
        # pie_chart.legend.label_text_font = "times"
        # pie_chart.legend.label_text_color = "black"
        # pie_chart.legend.label_text_font_size = "10pt"

        # title
        pie_chart.title.text_font_size = '11pt'
        pie_chart.title.text_font = 'Arial'
        pie_chart.title.text_color = "#224abe"

        # border
        pie_chart.outline_line_width = 2
        pie_chart.outline_line_alpha = 0.1
        pie_chart.outline_line_color = "#4e73df"

        pie_script, pie_div = components(pie_chart)
        # -------------------------------------------------------------------------------------------------

        # ------------------------------------- bar chart ------------------------------------------------
        diesel = carburant.count('Diesel')
        essence = carburant.count('Essence')

        carb = pd.DataFrame({
            'carburant': ['Essence', 'Diesel'],
            'counts': [essence, diesel]
        })
        source = ColumnDataSource(data=dict(carb_x=carb['carburant'], counts=carb['counts']))

        # plot_height=337, plot_width=465
        title_bar = 'presenté le carburant de voiture ' + name
        bar_chart = figure(x_range=carb['carburant'], plot_height=337, plot_width=350, # title="Carburants",
                           toolbar_location='above', tools=TOOLS, x_axis_label=title_bar, y_axis_label='Le nombre de fois')

        bar_chart.vbar(x='carb_x', top='counts', width=0.4, color="#4e73df", source=source, hover_color="#819ff7")

        bar_chart.add_tools(HoverTool(tooltips="""<table>
                                                        <tr>
                                                             <td style="color:blue;"> le nombre de fois   <td>
                                                             <td>                    : @counts            </td>
                                                        </tr>
                                                </table>"""))
        # legend
        # bar_chart.legend.label_text_font = "times"
        # bar_chart.legend.label_text_color = "black"
        # bar_chart.legend.label_text_font_size = "10pt"

        # x-axis & y-axis
        bar_chart.xaxis.axis_label_text_font_size = "12pt"
        bar_chart.yaxis.axis_label_text_font_size = "12pt"
        bar_chart.xaxis.axis_label_text_font = "Calibri"
        bar_chart.yaxis.axis_label_text_font = "Calibri"
        bar_chart.yaxis.minor_tick_line_color = None # bach t7iyd douk l5touta li kaybano mabin l5touta ra2isiiyin like 0,5,10
        bar_chart.xgrid.grid_line_color = None # to move line in axis inside chart

        # Title
        bar_chart.title.text_font_size = '13pt'
        bar_chart.title.text_font = 'Arial'
        bar_chart.title.text_color = "#224abe"

        # border
        bar_chart.outline_line_width = 2
        bar_chart.outline_line_alpha = 0.1
        # bar_chart.outline_line_color = "#4e73df"

        # change just some things about the x-axis
        bar_chart.xaxis.axis_line_width = 1.5
        bar_chart.xaxis.axis_line_color = "#99b0ff"

        # change just some things about the y-axis
        bar_chart.yaxis.axis_line_color = None # "#99b0ff"
        bar_chart.yaxis.axis_line_width = 1.5

        bar_chart.y_range.start = 0  # bach tjnb tkoun chart b3ida chwia 3la mi7war afasil

        bar_script, bar_div = components(bar_chart)
        # -------------------------------------------------------------------------------------------

        # ------------------------------------- line chart -----------------------------------------

        # algorithm for calcul count of price
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

        line_chart = figure(plot_height=430, plot_width=977, toolbar_location='above', # title='Line chart',
                            y_axis_label='Le nombre de fois', x_axis_label='Price(DH)', tools=TOOLS)

        line_chart.line(x='priceL', y='count_price', line_width=1.7, color="#4e73df", legend_label=name + ' ' + model_display,
                        source=df_for_line_char)

        line_chart.circle(x='priceL', y='count_price', size=5, color='blue', hover_color="#D8D8D8",
                          source=df_for_line_char)

        line_chart.xaxis[0].formatter = NumeralTickFormatter(format="0")

        TOOLTIPS_LINE = """<table>
                                        <tr>
                                             <td style="color:blue;">  le nombre de fois  <td>
                                             <td>: @count_price   </td>
                                        </tr>
                                        <tr>
                                             <td style="color:blue;"> Price <td>
                                             <td>: @priceL DH   </td>
                                        </tr>
                                        <tr>
                                             <center> 
                                                <td colspan = "2" height="10px"></td>
                                             </center>
                                        </tr>
                                </table>"""
        line_chart.add_tools(HoverTool(tooltips=TOOLTIPS_LINE))

        line_chart.legend.background_fill_alpha = 0.0
        # legend
        # line_chart.legend.label_text_font = "times"
        # line_chart.legend.label_text_color = "black"
        # line_chart.legend.label_text_font_size = "10pt"
        # line_chart.legend.background_fill_color = "#f8f9fc"
        # line_chart.legend.background_fill_color = "#ebefff" # background d legend


        # x-axis & y-axis
        line_chart.xaxis.axis_label_text_font_size = "12pt"
        line_chart.yaxis.axis_label_text_font_size = "12pt"
        line_chart.xaxis.axis_label_text_font = "Calibri"
        line_chart.yaxis.axis_label_text_font = "Calibri"
        line_chart.yaxis.minor_tick_line_color = None
        line_chart.xgrid.grid_line_color = None

        # Title
        line_chart.title.text_font_size = '13pt'
        line_chart.title.text_font = 'Arial'
        line_chart.title.text_color = "#224abe"

        # border
        line_chart.outline_line_width = 2
        line_chart.outline_line_alpha = 0.1
        # line_chart.outline_line_color = "#4e73df"

        # change just some things about the x-axis
        line_chart.xaxis.axis_line_width = 1.5
        line_chart.xaxis.axis_line_color = "#99b0ff"

        # change just some things about the y-axis
        line_chart.yaxis.axis_line_color = None # "#99b0ff"
        line_chart.yaxis.axis_line_width = 1.5

        line_chart.xaxis.major_label_orientation = pi / 4
        line_script, line_div = components(line_chart)

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
    # print('---------------------------\n', 'id = ', pk)
    order = VoitureModel.objects.get(id=pk)
    # print('---------------------------\n\n', 'name = ', order, '\n\n---------------------------')
    form = TestingForm(instance=order)

    if request.method == 'POST':
        # print('---------------------------- Printing POST:\n', request.POST, '\n--------------------------------------')
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
        # print('---------------------------- Printing POST:\n', request.POST, '\n--------------------------------------')
        order.delete()
        return redirect('/')

    context = {'item': order}

    return render(request, 'editing/delete_order.html', context)

