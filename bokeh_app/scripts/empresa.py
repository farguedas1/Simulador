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
from bokeh.models.widgets import DataTable, TableColumn, NumberFormatter, DateFormatter, Paragraph, Div
from bokeh.plotting import figure

def render_company_info(tick, info):
    text="""
        <div class="col-sm-6">
          <div class="card">
            <div class="card-body">
              <img src="bokeh_app/static/data/{tick}/{logo}" class="float-right" height="150px" width="150px">
              <h1 class="display-4">{name}</h1>
              <h5 class="card-title"><a href="{website}">{website}</a></h5>
              <hr class="my-4">
              <p class="card-text">{description}</p>
            </div>
          </div>
        </div>
    """.format(name=info['name'], tick=tick, logo=info['logo'],
               website=info['website'],description=info['description'])

    return text

def company_info_tab(datasets):
    tick_widgets_text = '<div class="row">'
    tick_widgets = []
    for tick in datasets:
        if not datasets[tick]["render"]:
            continue
        tick_widgets_text += render_company_info(tick, datasets[tick])
    tick_widgets_text += '</div>'

    return Div(text=tick_widgets_text, name="empresas", width_policy='max', min_width=1900, style={"display":"none", "foo" : "bar"})
