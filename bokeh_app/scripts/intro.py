import pandas as pd
import numpy as np

from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import TableColumn, DataTable, Div

def intro_tab():
    div = Div(text="""Your <a href="https://en.wikipedia.org/wiki/HTML">HTML</a>-supported text is initialized with the <b>text</b> argument.  The
        remaining div arguments are <b>width</b> and <b>height</b>. For this example, those values
        are <i>200</i> and <i>100</i> respectively.""")

    tab = Panel(child = div, title = 'Introducción')

    return tab
