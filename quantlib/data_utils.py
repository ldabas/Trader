import numpy as np
import datetime
import pandas as pd
import requests
import yfinance as yf
import datetime
from bs4 import BeautifulSoup

res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0] 
df = pd.read_html(str(table))
#print(df[0].to_json(orient='records'))
symbols = df[0].Symbol

def get_sp500_instruments():
    res = requests.get("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    df = pd.read_html(str(table))
    #print(df[0].to_json(orient='records'))
    symbols = df[0].Symbol

    return list(symbols)

symbols = get_sp500_instruments()

def get_sp500_df():
    symbols = get_sp500_instruments()
    symbols = symbols[:30]
    ohlcvs = {}
    for symbol in symbols:
        symbol_df = yf.Ticker(symbol).history(period="10y")
        ohlcvs[symbol] = symbol_df[["Open", "High", "Low", "Close", "Volume"]].rename(
            columns = {
                "Open":"open", "High":"high", "Low":"low", "Close":"close", "Volume":"volume"
            }
        )

    df = pd.DataFrame(index=ohlcvs["AMZN"].index)
    df.index.name = "date"
    instruments = list(ohlcvs.keys())
    for inst in instruments:
        inst_df = ohlcvs[inst]
        columns=list(map(lambda x:"{} {}".format(inst,x), inst_df.columns))
        df[columns] = inst_df

    return df,instruments

def extend_dataframe(traded,df):
    df.index = pd.Series(df.index).apply(lambda x:format_date(x))
    open_cols = list(map(lambda x:str(x) + " open", traded))
    high_cols = list(map(lambda x:str(x) + " high", traded))
    low_cols = list(map(lambda x:str(x) + " low", traded))
    close_cols = list(map(lambda x:str(x) + " close", traded))
    volume_cols = list(map(lambda x:str(x) + " volume", traded))

    historical_data = df.copy()
    historical_data = historical_data[open_cols+high_cols+low_cols+close_cols+volume_cols]
    #print(historical_data)
    historical_data.fillna(method="ffill", inplace=True)


    for inst in traded:
        historical_data["{} % ret".format(inst)] = historical_data["{} close".format(inst)] \
            / historical_data["{} close".format(inst)].shift(1) -1

        historical_data["{} % ret vol".format(inst)] = historical_data["{} % ret".format(inst)].rolling(25).std()
        historical_data["{} active".format(inst)] = historical_data["{} close".format(inst)] \
            != historical_data["{} close".format(inst)].shift(1)

    historical_data.fillna(method="bfill", inplace=True)
    return historical_data



""" df, instruments = get_sp500_df()
historical_data = extend_dataframe(instruments, df)
print(historical_data)
historical_data.to_excel("hist.xlsx") """

def format_date(dates):
    yymmdd = list(map(lambda x: int(x), str(dates).split(" ")[0].split("-")))
    return datetime.date(yymmdd[0], yymmdd[1], yymmdd[2])