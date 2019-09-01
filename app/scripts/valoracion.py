from os.path import dirname, join

import pandas as pd
import datetime

from bokeh.layouts import row, column, Spacer, WidgetBox, layout
from bokeh.models import ColumnDataSource, Panel, Slider, Label
from bokeh.models.tools import HoverTool
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Paragraph, Div, Markup
from bokeh.plotting import figure
import numpy as np


def render_valuation(tick, info):
    metrics_df = info["global_metrics"]["metrics"]
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
        # source.data = data_df
        # print("NPV with {} and".format(cppc))
        # print(data_df["Net Income from Continuing Operations"])
        van = np.npv(cppc, data_df["Net Income from Continuing Operations"])
        van_label.text = "VAN: {:,.2f}".format(van)

        net_in_5 = data_df["Net Income from Continuing Operations"].iloc[4]
        residual_in_5 = (net_in_5 * (1.0 + profit_grow_rate_slider.value) /
                             (cppc - market_grow_rate_slider.value))
        # print("residual = {} = {} * {} / ({} - {}) ".format(residual_in_5, net_in_5, 1.0 + profit_grow_rate_slider.value, cppc,market_grow_rate_slider.value))
        van_residual = np.npv(cppc, [0, 0, 0, 0, residual_in_5])
        van_residual_label.text = "VAN de valor residual: {:,.2f}".format(van_residual)
        valor_label.text = "Valor de Mercado: {:,.2f}".format(van + van_residual)


    profit_grow_rate_slider = Slider(start=0, end=max, format="0.00%",
                                     value=avg_grow, step=0.0001, title="Tasa de crecimiento de ganancias anual:")
    profit_grow_rate_slider.on_change('value', update_data)

    market_grow_rate_slider = Slider(start=0, end=max, format="0.00%",
                                     value=market_avg_grow, step=0.0001, title="Tasa de crecimiento (g) para flujos posteriores a 5 años:")
    market_grow_rate_slider.on_change('value', update_data)

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
    # print(income_df[["Date","Net Income from Continuing Operations"]])
    data_df = income_df[["Date"]].join(
      income_df['Net Income from Continuing Operations'] * (1.0 + profit_grow_rate_slider.value))
    data_df.Date += pd.Timedelta(days=(365 * 5)+1)
    # print(data_df)
    # source = ColumnDataSource(data=data_df)

    # p = figure(x_axis_type="datetime", title="Proyección de crecimiento de ganancias",
    #            align='center', toolbar_location="above", plot_height=300, width_policy="max")
    # p.grid.grid_line_alpha=0.3
    # p.xaxis.axis_label = 'Fecha'
    # p.yaxis.axis_label = 'Utilidad Neta'
    # # p.add_tools(hover)
    # p.toolbar.autohide = True
    #
    # p.line('Date', 'Net Income from Continuing Operations', color='#A6CEE3', source=source)

    d = figure(width_policy="max", plot_height=200, title="Resultados de Valoración",
           y_range=(0, 5), x_range=(0, 20), toolbar_location=None)
    d.outline_line_color = None
    d.grid.grid_line_color = None
    d.axis.axis_line_color = None
    d.axis.axis_label_text_color = None
    d.axis.minor_tick_line_color = None
    d.axis.major_tick_line_color = None
    d.axis.major_label_text_color = None
    # print(metrics_df["CPPC"].iloc[-1])

    cppc = metrics_df["CPPC"].iloc[-1]
    label = Label(x=1, y=4, text="CPPC: {:.2%}".format(cppc), text_font_size='18pt')
    d.add_layout(label)

    # print("NPV with {} and".format(cppc))
    print(data_df["Net Income from Continuing Operations"])

    van = np.npv(cppc, data_df["Net Income from Continuing Operations"])
    van_label = Label(x=1, y=3, text="VAN: {:,.2f}".format(van), text_font_size='18pt')
    d.add_layout(van_label)

    net_in_5 = data_df["Net Income from Continuing Operations"].iloc[4]
    residual_in_5 = (net_in_5 * (1.0 + profit_grow_rate_slider.value) /
                         (cppc - market_grow_rate_slider.value))
    # print("residual = {} = {} * {} / ({} - {}) ".format(residual_in_5, net_in_5, 1.0 + profit_grow_rate_slider.value, cppc,market_grow_rate_slider.value))
    van_residual = np.npv(cppc, [0, 0, 0, 0, residual_in_5])
    van_residual_label = Label(x=1, y=2, text="VAN de valor residual: {:,.2f}".format(van_residual), text_font_size='18pt')
    d.add_layout(van_residual_label)

    valor_label = Label(x=1, y=0, text="Valor de Mercado: {:,.2f}".format(van + van_residual),
                        text_font_style='bold', text_font_size='20pt')
    d.add_layout(valor_label)

    return column(div, row(controls,d), width_policy='max')


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
