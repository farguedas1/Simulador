from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.layouts import row

from datasets import load_datasets
from scripts.empresa import company_info_tab
from scripts.resultados import resultados_tab
from scripts.razones import razones_tab

# Load the datasets and perform any processing on them
datasets = load_datasets()

# Put all the tabs into one application
# tabs = Tabs(tabs = [intro_tab(),
#                     #stock_tab(datasets),
# 					resultados_tab(datasets),
# 					razones_tab(datasets),
# 					])

# Put the tabs in the current document for display
#curdoc().add_root(row(tabs, sizing_mode="stretch_width", name="panel"))
curdoc().add_root(company_info_tab(datasets))
curdoc().add_root(resultados_tab(datasets))
curdoc().add_root(razones_tab(datasets))
curdoc().title = "Modelo de Diagnóstico y Valoración Financiero para Empresas"
