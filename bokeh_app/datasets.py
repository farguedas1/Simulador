import pandas as pd
from os.path import dirname, join, isfile, isdir
from os import listdir
import yaml, io

def load_cash_flow(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'data/%s/cash-flow.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]
    return data

def load_balance_sheet(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'data/%s/balance-sheet.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]

    # Calculate some extra columns
    data['RC'] = data['Total current assets'] / data['Total current liabilities']
    data['PA'] = (data['Total current assets'] - data['Inventories']) / data['Total current liabilities']
    return data

def load_income_statement(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'data/%s/income-statement.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]

    # Calculate some extra columns
    data['Sales Expenses'] = data['R&D Expenses'] + data['Operating Expenses']
    return data

def load_stock_data(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'data/%s/stock.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]
    data = data.set_index('Date')
    return pd.DataFrame({ticker: data.Close, ticker+'_returns': data.Close.diff()})

def load_datasets():
    ticks = []
    dataset = {}
    start_date = '2014-01-01'
    end_date = '2019-09-01'
    data_folder = join(dirname(__file__), 'data')

    ticks_with_info = [f for f in listdir(data_folder) if isfile(join(data_folder, f, "info.yaml"))]
    for tick in ticks_with_info:
        with open(join(data_folder, tick, "info.yaml"), 'r') as stream:
            info = yaml.safe_load(stream)
            ticks.append((tick, info["name"]))

    for (tick, name) in ticks:
        dataset[tick] = {
            "render": True,
            "name": name,
    		"income_statement_data" : load_income_statement(tick, start_date, end_date),
    		#"cash_flow_data" : load_cash_flow(tick, start_date, end_date),
    		"balance_sheet_data" : load_balance_sheet(tick, start_date, end_date),
    		"stock_data" : load_stock_data(tick, start_date, end_date),
        }

    dataset["^GSPC"] = {
        "render": False,
        "stock_data" : load_stock_data("^GSPC", start_date, end_date),
    }

    return dataset
