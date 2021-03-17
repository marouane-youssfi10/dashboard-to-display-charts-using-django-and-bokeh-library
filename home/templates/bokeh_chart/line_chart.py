from bokeh.embed import components
from bokeh.models import HoverTool
from bokeh.models import NumeralTickFormatter
from bokeh.plotting import figure
from math import pi

def line_chart(name, model_display, TOOLS, df_for_line_char):
    line_chart = figure(plot_height=430, plot_width=977, toolbar_location='above',  # title='Line chart',
                        y_axis_label='Le nombre de fois', x_axis_label='Price(DH)', tools=TOOLS)

    line_chart.line(x='priceL', y='count_price', line_width=1.7, color="#4e73df",
                    legend_label=name + ' ' + model_display,
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
    line_chart.yaxis.axis_line_color = None  # "#99b0ff"
    line_chart.yaxis.axis_line_width = 1.5

    line_chart.yaxis.formatter = NumeralTickFormatter(format="0,0")

    line_chart.xaxis.major_label_orientation = pi / 4
    line_script, line_div = components(line_chart)
    return line_script, line_div