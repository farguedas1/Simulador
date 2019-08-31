import pandas as pd
from os.path import dirname, join, isfile, isdir
from os import listdir
import yaml, io
from scipy import stats

def load_cash_flow(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/cash-flow.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return data

def load_balance_sheet(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/balance-sheet.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Calculate some extra columns
    data['RC'] = data['Total current assets'] / data['Total current liabilities']
    data['PA'] = (data['Total current assets'] - data['Inventories']) / data['Total current liabilities']
    return data

def load_income_statement(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/income-statement.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]

    # Calculate some extra columns
    data['Sales Expenses'] = data['R&D Expenses'] + data['Operating Expenses']
    return data

def load_stock_data(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/stock-monthly.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    data = data.set_index('Date')
#    return pd.DataFrame({ticker: data.Close, ticker+'_returns': data.Close.diff()})
    return pd.DataFrame({ticker: data.Close,
                         'adj_close': data["Adj Close"],
                         'volume': data["Volume"],
                         ticker+'_returns': data.Close.pct_change(1)})

def calculate_global_metrics(dataset, ticker, start_date, end_date):
    gspc_stock_data = dataset["^GSPC"]["stock_data"]
    ticker_stock_data = dataset[ticker]["stock_data"]

    beta, alpha, r_value, p_value, std_err = stats.linregress(
        gspc_stock_data['^GSPC_returns'].dropna(),
        ticker_stock_data[ticker+'_returns'].dropna()
    )

    #print(ticker_stock_data[ticker+'_returns'].dropna())
    #print(gspc_stock_data['^GSPC_returns'].dropna())

    print("beta {}, alpha {}, r {}, p {}, std_err {}".format(
        beta, alpha, r_value, p_value, std_err
    ))

    return {
        "beta": beta
    }

def load_datasets():
    ticks = []
    dataset = {}
    start_date = '2014-08-01'
    end_date = '2019-08-01'
    data_folder = join(dirname(__file__), 'static/data')
    number_ticks = 0

    tickers_with_info = [f for f in listdir(data_folder) if isfile(join(data_folder, f, "info.yaml"))]
    for ticker in tickers_with_info:
        with open(join(data_folder, ticker, "info.yaml"), 'r') as stream:
            info = yaml.safe_load(stream)
            ticks.append((ticker, info))
            number_ticks += 1
            # print(ticker, info)

    dataset["^GSPC"] = {
        "render": False,
        "stock_data" : load_stock_data("^GSPC", start_date, end_date),
    }

    for (ticker, info) in ticks:
        dataset[ticker] = {
            "render": True,
    		"income_statement_data" : load_income_statement(ticker, start_date, end_date),
    		#"cash_flow_data" : load_cash_flow(ticker, start_date, end_date),
    		"balance_sheet_data" : load_balance_sheet(ticker, start_date, end_date),
    		"stock_data" : load_stock_data(ticker, start_date, end_date),
        }
        # Add this later since we need the ticker info already set
        dataset[ticker]["global_metrics"] = calculate_global_metrics(dataset, ticker, start_date, end_date)
        dataset[ticker].update(info)

    return (number_ticks, dataset)
