#import pandas as pd
#import numpy as np

#from bokeh.models import ColumnDataSource, Panel
#from bokeh.models.widgets import TableColumn, DataTable, Div
#from bokeh.plotting import figure

from os.path import dirname, join

import pandas as pd
import datetime

from bokeh.layouts import row, column, WidgetBox, layout, Spacer
from bokeh.models import ColumnDataSource, Panel, BoxAnnotation
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import Paragraph, CheckboxGroup
from bokeh.plotting import figure
import numpy as np


def plot_metric(title, yaxis_title, metric, ticker_tuple_list, ticker_lines, y_format='{%0.2f}'):
    palette = ['#33A02C', '#FB9A99', '#A6CEE3', '#B2DF8A']
    color_index = 0

    p = figure(x_axis_type="datetime", title=title, plot_height=300,
               align='center', toolbar_location="above", width_policy="max")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Fecha'
    p.yaxis.axis_label = yaxis_title
    p.toolbar.autohide = True

    for (ticker, metric_df) in ticker_tuple_list:
        line = p.line('Date', metric, legend=ticker, color=palette[color_index],
                      source=ColumnDataSource(metric_df))
        ticker_lines[ticker].append(line)
        color_index += 1

    p.legend.location = "top_left"
    p.legend.click_policy="hide"

    hover = HoverTool(
        tooltips=[
            ( 'fecha',      '@Date{%F}'         ),
            ( yaxis_title,  '@' + metric + y_format ),
        ],

        formatters={
            'Date'        : 'datetime', # use 'datetime' formatter for 'date' field
            yaxis_title   : 'printf',   # use 'printf' formatter
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p.add_tools(hover)

    return p

def metricas_tab(nticks, datasets):
    available_tickers = []
    ticker_data_tuple_list = []
    ticker_lines = dict()
    for ticker in datasets:
        if not datasets[ticker]["render"]:
            continue
        available_tickers.append(ticker)
        ticker_lines[ticker] = []
        ticker_data_tuple_list.append((ticker, datasets[ticker]["global_metrics"]["metrics"]))

    def update(attr, old, new):
        # tickers_innactive = available_tickers
        # for i in ticker_selection.active:
        #     ticker = ticker_selection.labels[i]
        #     tickers_innactive.remove(ticker)
        #     for line in ticker_lines[ticker]:
        #         line.visible = True
        # for ticker in tickers_innactive:
        #     for line in ticker_lines[ticker]:
        #         line.visible = False
        pass

    ticker_selection = CheckboxGroup(labels=available_tickers, active = [0, 1])
    ticker_selection.on_change('active', update)
    controls = WidgetBox(
       Paragraph(text="Seleccione los simbolos a desplegar:"),
       ticker_selection, )

    # Plot the metrics with all the tickers
    metric_plots = dict()
    metric_plots["ROE"] = plot_metric("Retorno sobre el Patrimonio RSP",
                                      "Porcentaje", "ROE", ticker_data_tuple_list,
                                      ticker_lines)
    metric_plots["ROA"] = plot_metric("Rendimiento de Operación sobre Activos",
                                      "Porcentaje", "ROA", ticker_data_tuple_list,
                                      ticker_lines)
    metric_plots["MUN"] = plot_metric("Mergen de Utilidad Neta",
                                      "Porcentaje", "MUN", ticker_data_tuple_list,
                                      ticker_lines)
    metric_plots["EBITDA"] = plot_metric("EBITDA",
                                      "Millones USD", "EBITDA", ticker_data_tuple_list,
                                      ticker_lines, '{0.2f}')
    metric_plots["EVA"] = plot_metric("EVA",
                                      "Millones USD", "EVA", ticker_data_tuple_list,
                                      ticker_lines, '{0.2f}')
    metric_plots["CPPC"] = plot_metric("CPPC",
                                      "Porcentaje", "CPPC", ticker_data_tuple_list,
                                      ticker_lines)
    z_altman_plot = plot_metric("Z Altman", "Indice", "Z_ALTMAN", ticker_data_tuple_list,
                               ticker_lines, '{0.2f}')
    z_altman_plot.y_range.start = 0
    z_altman_plot.add_layout(BoxAnnotation(top=1.81, fill_alpha=0.1, fill_color='red'))
    z_altman_plot.add_layout(BoxAnnotation(top=2.99, bottom=1.81, fill_alpha=0.1, fill_color='yellow'))
    z_altman_plot.add_layout(BoxAnnotation(bottom=2.99, fill_alpha=0.1, fill_color='green'))
    metric_plots["Z_ALTMAN"] = z_altman_plot

    return layout([
      [metric_plots["ROE"], metric_plots["ROA"], metric_plots["MUN"], metric_plots["EBITDA"]],
      [metric_plots["EVA"], metric_plots["CPPC"], metric_plots["Z_ALTMAN"], Spacer()],
    ], sizing_mode='stretch_both', name="metricas", width_policy='max', min_width=1024)
