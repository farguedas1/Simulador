import pandas as pd

from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, Panel
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import figure

def get_data(t1, t2, df1, df2):
    data = pd.concat([df1, df2], axis=1)
    data = data.dropna()
    data['t1'] = data[t1]
    data['t2'] = data[t2]
    data['t1_returns'] = data[t1+'_returns']
    data['t2_returns'] = data[t2+'_returns']
    return data


def stock_tab(dataset):
    t1 = "PG"
    t2 = "UL"
    df = get_data(t1, t2, dataset[t1]["stock_data"], dataset[t2]["stock_data"])
    data = df[['t1', 't2', 't1_returns', 't2_returns']]

    stats = PreText(text='', width=500)
    stats.text = str(df[[t1, t2, t1+'_returns', t2+'_returns']].describe())

    # set up plots

    source = ColumnDataSource(data)
    source_static = ColumnDataSource(data)
    tools = 'pan,wheel_zoom,xbox_select,reset'

    corr = figure(plot_width=350, plot_height=350,
                  tools='pan,wheel_zoom,box_select,reset')
    corr.title.text = '%s returns vs. %s returns' % (t1, t2)
    corr.circle('t1_returns', 't2_returns', size=2, source=source,
                selection_color="orange", alpha=0.6, nonselection_alpha=0.1, selection_alpha=0.4)

    ts1 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
    ts1.line('Date', 't1', source=source_static)
    ts1.circle('Date', 't1', size=1, source=source, color=None, selection_color="orange")
    ts1.title.text = t1

    ts2 = figure(plot_width=900, plot_height=200, tools=tools, x_axis_type='datetime', active_drag="xbox_select")
    ts2.x_range = ts1.x_range
    ts2.line('Date', 't2', source=source_static)
    ts2.circle('Date', 't2', size=1, source=source, color=None, selection_color="orange")
    ts2.title.text = t2

    # set up layout
    main_row = row(corr, stats)
    series = column(ts1, ts2)
    layout = column(main_row, series)

    # initialize
    #update()

    return Panel(child = layout, title = 'Stock')
