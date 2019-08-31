from bokeh.io import curdoc
from bokeh.models.widgets import Tabs
from bokeh.layouts import row

from datasets import load_datasets
from scripts.empresa import company_info_tab

# Load the datasets and perform any processing on them
(number_ticks, datasets) = load_datasets()


curdoc().add_root(company_info_tab(number_ticks, datasets))
curdoc().title = "Plantilla Estados Financieros Comparativo para Empresas"
