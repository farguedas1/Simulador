#import pandas as pd
#import numpy as np

#from bokeh.models import ColumnDataSource, Panel
#from bokeh.models.widgets import TableColumn, DataTable, Div
#from bokeh.plotting import figure

from os.path import dirname, join

import pandas as pd
import datetime

from bokeh.layouts import row, column, Spacer, WidgetBox, layout
from bokeh.models import ColumnDataSource, Panel, Slider
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Paragraph, Div, Markup
from bokeh.plotting import figure
import numpy as np

def plot_projection(tick, stock_data):
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

    p.line('Date', 'adj_close', color='#A6CEE3', source=ColumnDataSource(stock_data))

    #p.min_border_left = 160
    return p

def render_valuation(tick, info):
    avg_grow = info["valuation"]["profit_grow_rate"]["average"]
    optimist_grow = info["valuation"]["profit_grow_rate"]["optimist"]
    pesimist_grow = info["valuation"]["profit_grow_rate"]["pesimist"]

    market_avg_grow = info["valuation"]["market_grow_rate"]["average"]
    market_optimist_grow = info["valuation"]["market_grow_rate"]["optimist"]
    market_pesimist_grow = info["valuation"]["market_grow_rate"]["pesimist"]
    if market_optimist_grow > optimist_grow :
        max = market_optimist_grow
    else:
        max = optimist_grow

    div = Div(text="""
            <img src="app/static/data/{tick}/{logo}" class="float-right" height="150px" width="150px">
            <hr class="my-4">
           """.format(tick=tick, logo=info['logo']))

    def update_data(attrname, old, new):
        data_df = income_df[["Date"]].join(
          income_df['Net Income from Continuing Operations'] * (1.0 + profit_grow_rate_slider.value))
        data_df.Date += pd.Timedelta(days=(365 * 5)+1)
        source.data = data_df

    profit_grow_rate_slider = Slider(start=0, end=max, format="0.00%",
                                     value=avg_grow, step=0.0001, title="Tasa de crecimiento de ganancias anual:")
    profit_grow_rate_slider.on_change('value', update_data)

    market_grow_rate_slider = Slider(start=0, end=max, format="0.00%",
                                     value=market_avg_grow, step=0.0001, title="Tasa de crecimiento (g) para flujos posteriores a 5 años:")
    # market_grow_rate_slider.on_change('value', update_data)

    controls = WidgetBox(
       Div(text="<hr class='my-4'>Tasas de crecimiento de ganancias anual:"),
       row(
           Div(text="<b>Pesimista:</b> {}%".format(pesimist_grow * 100)),
           Div(text="<b>Promedio:</b> {}%".format(avg_grow * 100)),
           Div(text="<b>Optimista:</b> {}%".format(optimist_grow * 100)),
       ),
       profit_grow_rate_slider,
       Div(text="<hr class='my-4'>Tasa de crecimiento (g) para flujos posteriores a 5 años:"),
       row(
           Div(text="<b>Pesimista:</b> {}%".format(market_pesimist_grow * 100)),
           Div(text="<b>Promedio:</b> {}%".format(market_avg_grow * 100)),
           Div(text="<b>Optimista:</b> {}%".format(market_optimist_grow * 100)),
       ),
       market_grow_rate_slider)

    income_df = info["income_statement_data"]
    print(income_df[["Date","Net Income from Continuing Operations"]])
    data_df = income_df[["Date"]].join(
      income_df['Net Income from Continuing Operations'] * (1.0 + profit_grow_rate_slider.value))
    data_df.Date += pd.Timedelta(days=(365 * 5)+1)
    # print(data_df)
    source = ColumnDataSource(data=data_df)

    p = figure(x_axis_type="datetime", title="Proyección de crecimiento de ganancias",
               align='center', toolbar_location="above", plot_height=300, width_policy="max")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Fecha'
    p.yaxis.axis_label = 'Utilidad Neta'
    # p.add_tools(hover)
    p.toolbar.autohide = True

    p.line('Date', 'Net Income from Continuing Operations', color='#A6CEE3', source=source)


    return column(div, row(controls,p), width_policy='max')


def render_company_info(nticks, tick, info):
    p = render_valuation(tick, info)

    # text="""
    #   <div class="card">
    #     <div class="card-body">
    #       <img src="app/static/data/{tick}/{logo}" class="float-right" height="150px" width="150px">
    #       <h1 class="display-4">{name}</h1>
    #       <hr class="my-4">
    #     </div>
    #   </div>
    # """.format(name=info['name'], tick=tick, logo=info['logo'])
    # div = Div(text=text)

    return column(children=[p], width_policy='max', css_classes=["col-sm-12"])

def valoracion_tab(nticks, datasets):
    ticker_columns = []
    for tick in datasets:
        if not datasets[tick]["render"]:
            continue
        ticker_columns.append(render_company_info(nticks, tick, datasets[tick]))
    return row(children=ticker_columns, name="valoracion", width_policy='max', min_width=1024)
