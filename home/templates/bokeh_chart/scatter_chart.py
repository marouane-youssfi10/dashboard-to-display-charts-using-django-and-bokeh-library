from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models import Legend
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
from bokeh.models import FuncTickFormatter

def scatter_chart(df, name, TOOLS, model_display):
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

    scatter_chart.yaxis.formatter=NumeralTickFormatter(format="0,0")

    scatter_script, scatter_div = components(scatter_chart)

    return scatter_div, scatter_script