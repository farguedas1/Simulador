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
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Paragraph
from bokeh.plotting import figure

def render_income_statement(tick, name, income_statement_data):
    datasrc = ColumnDataSource(income_statement_data)

    # Columns of table
    columns = [TableColumn(field='Date', title='Año', width=50, formatter=DateFormatter(format="%Y")),
               TableColumn(field='Revenue', title='Ingresos Netos', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Cost of Revenue', title='Costo de Ventas', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Gross Profit', title='Utilidad Bruta', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Sales Expenses', title='Gastos de Ventas', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='SG&A Expense', title='Gastos de Administración', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Operating Expenses', title='Gastos de Operación', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Operating Income', title='Utilidad de Operación', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Interest Expense', title='Gastos Financieros', formatter=NumberFormatter(format="$0,0.00")),
               #TableColumn(field='Operating Income', title='Otros ingresos', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Earnings before Tax', title='Utilidad antes de impuesto', formatter=NumberFormatter(format="$0,0.00")),
               TableColumn(field='Income Tax Expense', title='Impuesto de Renta', formatter=NumberFormatter(format="$0,0.00")),
              ]

    return column(Paragraph(text="Resultados Ingresos Financieros {}".format(name)),
                  DataTable(source=datasrc, index_position=None, columns=columns, width=1800))

def resultados_tab(datasets):
    tick_widgets = []
    for tick in datasets:
        tick_widgets.append(render_income_statement(
            tick, datasets[tick]["name"], datasets[tick]["income_statement_data"]))

    return Panel(child = column(children=tick_widgets), title = 'Resultados')
