from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import NumeralTickFormatter
import pandas as pd

def bar_chart(carburant, name, TOOLS):
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

    bar_chart.yaxis.formatter = NumeralTickFormatter(format="0,0") # space betwen 000 000

    bar_script, bar_div = components(bar_chart)
    return bar_script, bar_div