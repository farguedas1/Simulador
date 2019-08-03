from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.layouts import row

from datasets import load_datasets
from scripts.intro import intro_tab
from scripts.stock import stock_tab
from scripts.resultados import resultados_tab

# Load the datasets and perform any processing on them
datasets = load_datasets()

# Put all the tabs into one application
tabs = Tabs(tabs = [intro_tab(),
                    stock_tab(datasets),
					resultados_tab(datasets)
					])

# Put the tabs in the current document for display
curdoc().add_root(row(tabs, sizing_mode="stretch_width"))
curdoc().title = "Analizador"
