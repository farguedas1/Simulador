import pandas as pd
import numpy as np
from os.path import dirname, join, isfile, isdir
from os import listdir
import yaml, io
from scipy import stats

def load_cash_flow(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/cash-flow.csv' % ticker.upper())
    data = pd.read_csv(fname, parse_dates=['Date'])
    data = data[(data['Date'] >= start_date) & (data['Date'] <= end_date)]
    return data

def load_balance_sheet(ticker, start_date, end_date, exchange_rates):
    fname = join(dirname(__file__), 'static/data/%s/balance-sheet.csv' % ticker.upper())
    df = pd.read_csv(fname, parse_dates=['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]

    # Normalize data
    # df['Cost of Revenue'] = df['Cost of Revenue'].abs()
    # df['Operating Income/Expenses'] = df['Operating Income/Expenses'].abs()
    # df['Selling, General and Administrative Expenses'] = df['Selling, General and Administrative Expenses'].abs()

    # Calculate some extra columns
    # data['RC'] = data['Total current assets'] / data['Total current liabilities']
    # data['PA'] = (data['Total current assets'] - data['Inventories']) / data['Total current liabilities']
    # # ROA =
    # data['PA'] = (data['Total current assets'] - data['Inventories']) / data['Total current liabilities']
    # # ROE = UAT / PT
    # data['PA'] = (data['Total current assets'] - data['Inventories']) / data['Total current liabilities']

    return df

def load_income_statement(ticker, start_date, end_date, exchange_rates):
    fname = join(dirname(__file__), 'static/data/%s/income-statement.csv' % ticker.upper())
    df = pd.read_csv(fname, parse_dates=['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]


    # Normalize numbers in millions
    for column in df.columns:
        if df[column].dtype == np.object:
          df[column] = df[column].apply(lambda x: str(x).replace(',', '')).astype('float') / 1000000

    # Adjust exchange rates
    if exchange_rates is not None:
        df["exchange_rate"] = np.nan
        df.set_index("Date", inplace=True)

        for year in exchange_rates:
            df.loc[[pd.to_datetime(year, format="%Y")],["exchange_rate"]] = exchange_rates[year]

        df.reset_index(inplace=True)
        columns_to_multiply = []
        other_columns = []
        for column in df.columns:
            if df[column].dtype == np.float64:
                columns_to_multiply.append(column)
            else:
                other_columns.append(column)
        df = df[other_columns].join(df[columns_to_multiply].multiply(df["exchange_rate"], axis="index"))
        print(df[['Date','Pretax Income',"exchange_rate"]])


    #print(df.dtypes)

    # Calculate some extra columns
    #data['Sales Expenses'] = data['R&D Expenses'] + data['Operating Expenses']
    return df

def load_stock_data(ticker, start_date, end_date):
    fname = join(dirname(__file__), 'static/data/%s/stock-monthly.csv' % ticker.upper())
    df = pd.read_csv(fname, parse_dates=['Date'])
    df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
    df = df.set_index('Date')
#    return pd.DataFrame({ticker: data.Close, ticker+'_returns': data.Close.diff()})
    return pd.DataFrame({ticker: df.Close, 'adj_close': df["Adj Close"],
                         'volume': df["Volume"], ticker+'_returns': df.Close.pct_change(1)})

def calculate_global_metrics(dataset, ticker):
    gspc_stock_df = dataset["^GSPC"]["stock_data"]
    ticker_stock_df = dataset[ticker]["stock_data"]
    ticker_income_df = dataset[ticker]["income_statement_data"]

    metrics_df = pd.DataFrame()
    metrics_df['Date'] = ticker_income_df['Date']


    # ROE = Pretax income / total assets
    metrics_df['ROE'] = ticker_income_df['Pretax Income']

    print("Metrics data frame")
    print(metrics_df)

    # beta, alpha, r_value, p_value, std_err = stats.linregress(
    #     gspc_stock_data['^GSPC_returns'].dropna(),
    #     ticker_stock_data[ticker+'_returns'].dropna()
    # )
    #
    # #print(ticker_stock_data[ticker+'_returns'].dropna())
    # #print(gspc_stock_data['^GSPC_returns'].dropna())
    #
    # print("beta {}, alpha {}, r {}, p {}, std_err {}".format(
    #     beta, alpha, r_value, p_value, std_err
    # ))

    return {
        # "beta": beta,
        "metrics": metrics_df
    }

def load_datasets():
    ticks = []
    dataset = {}
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
        "stock_data" : load_stock_data("^GSPC", '2014-08-01', '2019-08-01'),
    }

    for (ticker, info) in ticks:
        exchange_rates = info.get('exchange_rates')
        dataset[ticker] = {
            "render": True,
    		"income_statement_data" : load_income_statement(ticker, '2014', '2018-12-31', exchange_rates),
    		#"cash_flow_data" : load_cash_flow(ticker, start_date, end_date),
    		"balance_sheet_data" : load_balance_sheet(ticker, '2014', '2018-12-31', exchange_rates),
    		"stock_data" : load_stock_data(ticker, '2014', '2018'),
        }
        # Add this later since we need the ticker info already set
        dataset[ticker]["global_metrics"] = calculate_global_metrics(dataset, ticker)
        dataset[ticker].update(info)

    return (number_ticks, dataset)
