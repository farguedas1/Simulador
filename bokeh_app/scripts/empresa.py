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

def stock_plot(tick, stock_data):
    hover = HoverTool(
        tooltips=[
            ( 'date',   '@Date{%F}'            ),
            ( 'close',  '@adj_close{%0.2f}'    ), # use @{ } for field names with spaces
            ( 'volume', '@volume{0.00 a}'      ),
        ],

        formatters={
            'Date'      : 'datetime', # use 'datetime' formatter for 'date' field
            'adj_close' : 'printf',   # use 'printf' formatter for 'adj close' field
                                      # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    p = figure(x_axis_type="datetime", title="Stock Closing Prices",
               align='center', toolbar_location="below", width_policy="max")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Price'
    p.add_tools(hover)

    p.line('Date', 'adj_close', color='#A6CEE3', source=ColumnDataSource(stock_data))

    #p.min_border_left = 160
    return p


def render_company_info(nticks, tick, info):
    p = stock_plot(tick, info["stock_data"])

    text="""
      <div class="card">
        <div class="card-body">
          <img src="bokeh_app/static/data/{tick}/{logo}" class="float-right" height="150px" width="150px">
          <h1 class="display-4">{name}</h1>
          <h5 class="card-title"><a href="{website}">{website}</a></h5>
          <hr class="my-4">
          <p class="card-text">{description}</p>
          <hr class="my-4">
        </div>
      </div>
    """.format(name=info['name'], tick=tick, logo=info['logo'],
               website=info['website'],description=info['description'])
    div = Div(text=text)

    return column(children=[div, p], width_policy='max', css_classes=["col-sm-12"])

def company_info_tab(nticks, datasets):
    ticker_columns = []
    for tick in datasets:
        if not datasets[tick]["render"]:
            continue
        ticker_columns.append(render_company_info(nticks, tick, datasets[tick]))
    return row(children=ticker_columns, name="empresas", width_policy='max', min_width=1024)
