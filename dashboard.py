import fetch
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from dash import Dash, dash_table, html, dcc, Input, Output, callback
import warnings
warnings.filterwarnings('ignore')

def dashboard(ticker, date):
    stock = yf.Ticker(ticker)
    fin = fetch.financials(ticker)
    fin["Earnings %"] = (fin["Net Income"]/fin["Total Revenue"])*100
    fin["Debt to Equity"] = (fin["Total Debt"]/fin["Total Equity Gross Minority Interest"])*100
    price_act = stock.history(period="3y", interval="1wk")
    price_act = price_act.reset_index()

    # print(stock.info["shortName"])
    # print(stock.info["website"])
    # print(stock.info["longBusinessSummary"])

    price = go.Figure()
    # Price range
    price.add_trace(go.Scatter(x=price_act["Date"], y=price_act["Close"],
                                    line = dict(color='white', width=1), 
                                    name="Close"))
    price.add_trace(go.Scatter(x=price_act["Date"], y=price_act["Low"],
                                    line = dict(color='crimson', width=1),
                                    # fill='toself',
                                    fillcolor='silver',
                                    name="Low",
                                    opacity=0.5))
    price.add_trace(go.Scatter(x=price_act["Date"], y=price_act["High"],
                                    line = dict(color='darkolivegreen', width=1),
                                    # fill='toself',
                                    fillcolor='silver',
                                    name="High",
                                    opacity=1))
    # EPS
    price.add_trace(go.Scatter(x=fin["Date"], y=fin["Diluted EPS"],
                                    mode="lines+markers",
                                    line = dict(color='white', width=1, dash='dash'),
                                    name="EPS", yaxis="y2",
                                    connectgaps=True))
    # Volume
    price.add_trace(go.Bar(x=price_act["Date"], y=price_act["Volume"], 
                                    name="Volume", 
                                    yaxis="y3",
                                    opacity=0.6,
                                    marker_color="silver"))
    price.update_layout(
        yaxis=dict(
            title="$",
            range=[0, price_act["Close"].max() + price_act["Close"].max()*0.05]
        ),
        yaxis2=dict(
            title="EPS",
            overlaying="y",
            side="right",
            range=[fin["Diluted EPS"].min() - abs(fin["Diluted EPS"].min()*0.1), fin["Diluted EPS"].max() + abs(fin["Diluted EPS"].max()*0.1)]
        ),
        yaxis3=dict(
            title="Volume",
            overlaying="y",
            anchor="free",
            range=[0, price_act["Volume"].max()*5],
            autoshift=True,
            shift=-25
        ),
        template="plotly_dark",
        hovermode="x"
    )
    price.update_layout(autosize=True, height=750)
    price.show()

    # profit breakdown
    profit = go.Figure()
    profit.add_trace(go.Bar(x=fin["Date"], y=fin["Gross Profit"],
                                name="Gross Profit",
                                marker_color="midnightblue",
                                text=fin["Gross Profit"]))
    profit.add_trace(go.Bar(x=fin["Date"], y=fin["Free Cash Flow"],
                                name="Free Cash Flow",
                                marker_color="darkorange",
                                text=fin["Free Cash Flow"]))
    profit.add_trace(go.Bar(x=fin["Date"], y=fin["Operating Income"],
                                name="Operating Income",
                                marker_color="indianred",
                                text=fin["Operating Income"]))
    profit.add_trace(go.Bar(x=fin["Date"], y=fin["Net Income"],
                                name="Net Income",
                                marker_color="goldenrod",
                                text=fin["Net Income"]))
    # profit.add_trace(go.Bar(x=fin["Date"], y=fin["Repayment Of Debt"],
    #                             opacity=0.6,
    #                             name="Debt Repayments",
    #                             marker_color="red",
    #                             text=fin["Repayment Of Debt"]))
    profit.update_traces(
        texttemplate='%{text:.2s}', textposition='outside'
    )
    profit.update_layout(
        title="Profit Breakdown", 
        yaxis_zeroline=True,
        autosize=True, 
        height=750,
        template="plotly_dark",
        # hovermode="y"
    )
    profit.show()
    print(" ====================================================================================================================================")
    print("Investopedia: https://www.investopedia.com/ask/answers/031015/what-difference-between-gross-profit-operating-profit-and-net-income.asp")
    print("              https://www.investopedia.com/terms/f/freecashflow.asp")
    print(" ====================================================================================================================================")
    print()
    print("> \033[4m\033[1mGross profit\033[0m is total revenue minus the expenses directly related to the production of goods or the cost of goods sold (COGS).")
    print()
    print("> Derived from gross profit, \033[4m\033[1moperating profit\033[0m is the residual income after accounting for all costs.")
    print()
    print("> \033[4m\033[1mNet income\033[0m reflects the total residual income after accounting for all cash flows, both positive and negative.")
    print()
    print("> \033[4m\033[1mFree cash flow\033[0m (FCF) represents the cash that a company generates after accounting for cash outflows to support operations and maintain its capital assets. Unlike earnings or net income, \033[4m\033[1mfree cash flow\033[0m is a measure of profitability that excludes the non-cash expenses of the income statement and includes spending on equipment and assets as well as changes in working capital from the balance sheet. ")

    # revenue breakdown
    revenue = go.Figure()
    revenue.add_trace(go.Scatter(x=fin["Date"], y=fin["Total Revenue"],
                                name="Gross Profit",
                                fill='tozeroy',
                                mode="lines+markers",
                                marker_color="grey",
                                yaxis="y"))
    revenue.add_trace(go.Scatter(x=fin["Date"], y=fin["Net Income"],
                                name="Net Income",
                                fill='tozeroy',
                                mode="lines+markers",
                                marker_color="darkseagreen",
                                yaxis="y"))
    revenue.add_trace(go.Scatter(x=fin["Date"], y=fin["Earnings %"],
                                name="Earnings %",
                                line = dict(color='white', width=2, dash='dash'),
                                yaxis="y2"))
    revenue.update_layout(
        title="Revenue Breakdown", 
        yaxis_zeroline=True,
        autosize=True, 
        height=600,
        template="plotly_dark",
        hovermode="x unified",
        yaxis=dict(
            title="$",
            range=[0, fin["Total Revenue"].max() + fin["Total Revenue"].max()*0.5]
        ),
        yaxis2=dict(
            title="Earnings (%)",
            overlaying="y",
            side="right",
            range=[0, fin["Earnings %"].max() + abs(fin["Earnings %"].max()*0.1)]
        ),
    )
    revenue.show()

    # Debt:Equity
    debt = go.Figure()
    debt.add_trace(go.Scatter(x=fin["Date"], y=fin["Total Equity Gross Minority Interest"], 
                                fill='tonexty',
                                mode="lines+markers",
                                marker_color="grey",
                                name="Equity",
                                yaxis="y"))
    debt.add_trace(go.Scatter(x=fin["Date"], y=fin["Total Debt"], 
                                fill='tozeroy',
                                mode="lines+markers",
                                marker_color="indianred",
                                name="Debt",
                                yaxis="y"))
    debt.add_trace(go.Scatter(x=fin["Date"], y=fin["Debt to Equity"],
                                name="Debt to Equity %",
                                line = dict(color='white', width=2, dash='dash'),
                                yaxis="y2"))
    debt.update_layout(
        title="Debt & Equity", 
        yaxis_zeroline=True,
        autosize=True, 
        height=600,
        template="plotly_dark",
        hovermode="x unified",
        yaxis=dict(
            title="$",
            range=[0, fin[["Total Debt", "Total Equity Gross Minority Interest"]].max(axis=None) + fin[["Total Debt", "Total Equity Gross Minority Interest"]].max(axis=None)*0.5]
        ),
        yaxis2=dict(
            title="Debt to Equity (%)",
            overlaying="y",
            side="right",
            range=[0, fin["Debt to Equity"].max() + abs(fin["Debt to Equity"].max()*0.1)]
        ),
    )
    debt.show()

    # buybacks
    buybacks = go.Figure()
    buybacks.add_trace(go.Scatter(x=fin["Date"], y=abs(fin["Repurchase Of Capital Stock"]), 
                                fill='tonexty',
                                mode="lines+markers",
                                marker_color="green",
                                name="Buybacks",
                                yaxis="y"))
    buybacks.update_layout(
        title="Stock Buybacks", 
        yaxis_zeroline=True,
        autosize=True, 
        height=600,
        template="plotly_dark",
        hovermode="x unified",
        yaxis=dict(
            title="$",
            # range=[0, abs(fin["Repurchase Of Capital Stock"]).max()*1.05]
        ),
    )
    buybacks.show()

    # buybacks
    try:
        dvd_df = pd.DataFrame(stock.dividends).reset_index()
        dvds = go.Figure()
        dvds.add_trace(go.Scatter(x=dvd_df["Date"], y=abs(dvd_df["Dividends"]), 
                                    fill='tonexty',
                                    mode="lines+markers",
                                    marker_color="hotpink",
                                    name="Buybacks",
                                    yaxis="y"))
        dvds.update_layout(
            title="Dividends", 
            yaxis_zeroline=True,
            autosize=True, 
            height=600,
            template="plotly_dark",
            hovermode="x unified",
        )
        dvds.show()
    except ValueError:
        print("NO DIVIDEND DATA")

    print(stock.major_holders)
    print(stock.institutional_holders)
    print(stock.mutualfund_holders)

    try:
        df = fetch.patents(ticker, date)
        fig = go.Figure(data=[go.Table(
            header=dict(values=['companyFilingName', 'description', 'filingDate', 'filingStatus', 'patentType', 'url'],
                        line_color='darkslategray',
                        fill_color='gray',
                        align='left',
                        font=dict(color='black', size=14)),
            cells=dict(values=[df.companyFilingName, df.description, df.filingDate, df.filingStatus, df.patentType, df.url],
                    line_color='darkslategray',
                    fill_color='lightgray',
                    align='left',
                    font=dict(color='black', size=12)))
        ])
        fig.update_layout(
            width=2000,
            template='plotly_dark'
        )
        fig.show()
    except AttributeError:
        print("NO PATENT DATA")

    try:
        df = fetch.visa_applications(ticker, date)
        fig = go.Figure(data=[go.Table(
            header=dict(values=['jobTitle', 'fullTimePosition', 'beginDate', 'endDate', 'workSiteCity', 'wageRangeFrom', 'wageRangeTo'],
                        line_color='darkslategray',
                        fill_color='gray',
                        align='left',
                        font=dict(color='black', size=14)),
            cells=dict(values=[df.jobTitle, df.fullTimePosition, df.beginDate, df.endDate, df.worksiteCity, df.wageRangeFrom, df.wageRangeTo],
                    line_color='darkslategray',
                    fill_color='lightgray',
                    align='left',
                    font=dict(color='black', size=12)))
        ])
        fig.update_layout(
            width=2000,
            template='plotly_dark'
        )
        fig.show()
    except AttributeError:
        print("NO VISA DATA")