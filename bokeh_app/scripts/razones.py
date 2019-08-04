#import pandas as pd
#import numpy as np

#from bokeh.models import ColumnDataSource, Panel
#from bokeh.models.widgets import TableColumn, DataTable, Div
#from bokeh.plotting import figure

from os.path import dirname, join

import pandas as pd
from datetime import date, datetime

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Dropdown
from bokeh.plotting import figure

def render_razones_financieras(tick, name, balance_sheet_data):
    data = balance_sheet_data
    menu = [(ts.strftime('%Y'), str(idx)) for idx, ts in data['Date'].iteritems()]

#    balance_sheet_data['index'] = balance_sheet_data.index
#    menu = [(balance_sheet_data.loc[idx, ['Date']].strftime('%Y'), idx) for idx in balance_sheet_data.index]

#    dropdown = Dropdown(label="Year for {}".format(tick), button_type="primary", menu=menu)
    dropdown = Dropdown(button_type="primary", menu=menu)
    factors = ["RC", "PA"]

    def make_dataset(idx, factors, balance_sheet_data):
        #x = [balance_sheet_data[factor] for factor in factors]
        #LineColor = ["green" if a>=0 else "red" for a in x]
        #LineColor = ["green" for factor in factors]
        data = balance_sheet_data.iloc[int(idx), :]

        arr_df = pd.DataFrame(
             {'factor': [factor for factor in factors],
              'x1': [data[factor] for factor in factors],
              'line_color': "green"
             })

        #print(arr_df)

        return ColumnDataSource(arr_df)

    def update(attr, old, new):
        (year, idx) = menu[int(dropdown.value)];
        dropdown.label = year
        new_src = make_dataset(idx, factors, balance_sheet_data)
        datasrc.data.update(new_src.data)

    (year, idx) = menu[0];
    dropdown.value = year
    dropdown.label = dropdown.value
    dropdown.on_change('value', update)

    datasrc = make_dataset(idx, factors, balance_sheet_data)
    dot = figure(title="Razones Financieras {}".format(tick),y_range=factors, x_range=[-20,20])
    dot.segment(0, 'factor', 'x1', 'factor', line_width=2, line_color='line_color', source=datasrc)
    dot.circle(0, 'factor', size=15, fill_color="orange", line_width=3, line_color='line_color', source=datasrc)

    return column(dropdown, dot)

def razones_tab(datasets):
    tick_widgets = []
    for tick in datasets:
        tick_widgets.append(render_razones_financieras(
            tick, datasets[tick]["name"], datasets[tick]["balance_sheet_data"]))

    return Panel(child = row(children=tick_widgets), title = 'Razones Financieras')
