#import pandas as pd
#import numpy as np

#from bokeh.models import ColumnDataSource, Panel
#from bokeh.models.widgets import TableColumn, DataTable, Div
#from bokeh.plotting import figure

from os.path import dirname, join

import pandas as pd
import datetime

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Paragraph, Div
from bokeh.plotting import figure
import numpy as np

def datetime(x):
    return np.array(x, dtype=np.datetime64)

# AttributeError: unexpected attribute 'responsive' to Figure, possible attributes are above, align, aspect_ratio, aspect_scale, background, background_fill_alpha, background_fill_color, below, border_fill_alpha, border_fill_color, center, css_classes, disabled, extra_x_ranges, extra_y_ranges, frame_height, frame_width, height, height_policy, hidpi, inner_height, inner_width, js_event_callbacks, js_property_callbacks, left, lod_factor, lod_interval, lod_threshold, lod_timeout, margin, match_aspect, max_height, max_width, min_border, min_border_bottom, min_border_left, min_border_right, min_border_top, min_height, min_width, name, outer_height, outer_width, outline_line_alpha, outline_line_cap, outline_line_color, outline_line_dash, outline_line_dash_offset, outline_line_join, outline_line_width, output_backend, plot_height, plot_width, renderers, reset_policy, right, sizing_mode, subscribed_events, tags, title, title_location, toolbar, toolbar_location, toolbar_sticky, visible, width, width_policy, x_range, x_scale, y_range or y_scale

def plot_stocks(ticker_tuples):
    palette = ['#33A02C', '#FB9A99', '#A6CEE3', '#B2DF8A']
    color_index = 0

    hover = HoverTool(
        tooltips=[
            ( 'fecha',   '@Date{%F}'            ),
            ( 'cierre',  '@adj_close{%0.2f}'    ), # use @{ } for field names with spaces
            ( 'volumen', '@volume{0.00 a}'      ),
        ],

        formatters={
            'Date'      : 'datetime', # use 'datetime' formatter for 'date' field
            'adj_close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                      # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p = figure(x_axis_type="datetime", title="Precio ajustado al cierre de la acción",
               align='center', toolbar_location="above", width_policy="max")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Fecha'
    p.yaxis.axis_label = 'Precio'
    p.add_tools(hover)
    p.toolbar.autohide = True

    for (tick, data) in ticker_tuples:
        # print("adding tick {}".format(tick))
        p.line('Date', 'adj_close', line_width=4, legend="{} ".format(tick),
               color=palette[color_index], source=ColumnDataSource(data))
        color_index += 1

    p.legend.location = "top_left"
    p.legend.click_policy="hide"
    #p.min_border_left = 160
    return p


def render_company_info(nticks, tick, info):
    text="""
      <div class="card">
        <div class="card-body">
          <img src="app/static/data/{tick}/{logo}" class="float-right" height="150px" width="150px">
          <h1 class="display-4">{name}</h1>
          <h5 class="card-title"><a href="{website}">{website}</a></h5>
          <hr class="my-4">
          <p class="card-text">{description}</p>
        </div>
      </div>
    """.format(name=info['name'], tick=tick, logo=info['logo'],
               website=info['website'],description=info['description'])
    div = Div(text=text, width_policy='max')

    # return column(children=[div, p], width_policy='max', css_classes=["col-sm-12"])
    return div

def company_info_tab(nticks, datasets):
    ticker_columns = []
    render_tickets = []
    for tick in datasets:
        if not datasets[tick]["render"]:
            continue
        ticker_columns.append(render_company_info(nticks, tick, datasets[tick]))
        render_tickets.append((tick, datasets[tick]["stock_data"]))
    return  column(
              row(children=ticker_columns),
              row(plot_stocks(render_tickets)),
              name="empresas", width_policy='max', min_width=1024
            )
