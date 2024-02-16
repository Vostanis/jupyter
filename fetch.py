from vault import FHB_KEY

import yfinance as yf
import pandas as pd
import requests as r

BASE = "https://finnhub.io/api/v1"
HDRS = {"X-Finnhub-Token":FHB_KEY}

def GET(endpoint):
    return r.get(BASE + endpoint, headers = HDRS)

# mechanic
def json_nest(df_col):
    dfs = []
    for entry in df_col:
        try:
            df = pd.DataFrame(entry)
        except ValueError:
            df = pd.DataFrame(entry, index=[0])
        dfs.append(df)

    try:
        df = pd.concat(dfs, ignore_index=True)
    except ValueError:
        return pd.DataFrame()
    return df

# yahoo datasets
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

# finnhub datasets
def search_ticker(ticker):
    rsp = GET(f"/search?q={ticker}")
    df = pd.DataFrame(rsp.json()['result'])
    return df

def sec_filings(ticker):
    rsp = GET(f"/stock/filings?symbol={ticker}")
    df = pd.DataFrame(rsp.json())
    return df

def analyst_recommendations(ticker):
    rsp = GET(f"/stock/recommendation?symbol={ticker}")
    df = pd.DataFrame(rsp.json())
    return df

def eps_surprises(ticker):  
    rsp = GET(f"/stock/earnings?symbol={ticker}")
    df = pd.DataFrame(rsp.json())
    return df

def earnings_calendar(ticker): 
    rsp = GET(f"/calendar/earnings?symbol={ticker}")
    df = pd.DataFrame(rsp.json()["earningsCalendar"])
    return df

def patents(ticker, date):
    rsp = GET(f"/stock/uspto-patent?symbol={ticker}&from={date}")
    df = pd.DataFrame(rsp.json())
    df = json_nest(df.data)
    return df

def visa_applications(ticker, date):
    rsp = GET(f"/stock/visa-application?symbol={ticker}&from={date}")
    df = pd.DataFrame(rsp.json())
    df = pd.DataFrame(df.data)
    df = json_nest(df.data)
    return df

def senate_lobbying(ticker, date):
    rsp = GET(f"/stock/lobbying?symbol={ticker}&from={date}")
    df = pd.DataFrame(rsp.json())
    # df = pd.DataFrame(df)
    df = json_nest(df.data)
    return df