import yfinance as yf
import pandas as pd

def financials(ticker):
    data = yf.Ticker(ticker)
    df = pd.concat([ # concat and transpose
        data.quarterly_income_stmt,
        data.quarterly_balance_sheet,
        data.quarterly_cashflow
    ]).T
    df = df.reset_index() # reset index (date) into a column
    df.columns = ['Date', *df.columns[1:]]
    df['Ticker'] = data.ticker # add ticker to dataframe
    return df

def bulkfin(tickers):
    dfs = []
    for ticker in tickers:
        df = financials(ticker)
        dfs.append(df)

    bulkdf = pd.concat(dfs, ignore_index=True)
    bulkdf = bulkdf.set_index(['Ticker','Date'])
    return bulkdf