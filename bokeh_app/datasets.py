import pandas as pd
from os.path import dirname, join

def load_cash_flow(ticker, start_date, end_date):
    fname = join(join(dirname(__file__), 'data/cash-flow'), '%s.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]
    return data

def load_balance_sheet(ticker, start_date, end_date):
    fname = join(join(dirname(__file__), 'data/balance-sheet'), '%s.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]
    return data

def load_income_statement(ticker, start_date, end_date):
    fname = join(join(dirname(__file__), 'data/income-statement'), '%s.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]

    # Calculate some extra columns
    data['Sales Expenses'] = data['R&D Expenses'] + data['Operating Expenses']
    return data

def load_stock_data(ticker, start_date, end_date):
    fname = join(join(dirname(__file__), 'data/stock'), '%s.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] > start_date) & (data['Date'] < end_date)]
    data = data.set_index('Date')
    return pd.DataFrame({ticker: data.Close, ticker+'_returns': data.Close.diff()})

def load_datasets():
    ticks = [("PG", "P&G"), ("UL", "Unilever")]
    dataset = {}
    start_date = '2014-01-01'
    end_date = '2019-09-01'

    for (tick, name) in ticks:
        dataset[tick] = {
            "name": name,
    		"income_statement_data" : load_income_statement(tick, start_date, end_date),
    		#"cash_flow_data" : load_cash_flow(tick, start_date, end_date),
    		"balance_sheet_data" : load_balance_sheet(tick, start_date, end_date),
    		"stock_data" : load_stock_data(tick, start_date, end_date),
        }

    return dataset
